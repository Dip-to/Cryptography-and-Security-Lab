"use strict";

/********* External Imports ********/

const { stringToBuffer, bufferToString, encodeBuffer, decodeBuffer, getRandomBytes } = require("./lib");
const { subtle } = require('crypto').webcrypto;

/********* Constants ********/

const PBKDF2_ITERATIONS = 100000; // number of iterations for PBKDF2 algorithm
const MAX_PASSWORD_LENGTH = 64;   // we can assume no password is longer than this many characters
const dummyStringArray = [];

/********* Implementation ********/
class Keychain {
  /**
   * Initializes the keychain using the provided information. Note that external
   * users should likely never invoke the constructor directly and instead use
   * either Keychain.init or Keychain.load. 
   * Arguments:
   *  You may design the constructor with any parameters you would like. 
   * Return Type: void
   */

  constructor(data,secrets) {
    this.data = data;
    this.secrets = secrets;
  };
  hash_master_pass=null
  static generateSalt(size) {
    let salt = new Int8Array(size);
    for (let i = 0; i < size; i++) {
      salt[i] = Math.floor(Math.random() * 256); // Generates a random number between 0 and 255
    }
    return salt;
  }

  /** 
    * Creates an empty keychain with the given password.
    *
    * Arguments:
    *   password: string
    * Return Type: void
    */
  static async init(password) {

    //data
    this.hash_master_pass=await subtle.digest("SHA-256", stringToBuffer(password))
    var k=0;
    let salt= this.generateSalt(16);
    let ivsalt=this.generateSalt(16);
    var secrets={};
    var data={};
    data.kvs={};
    data.salt=salt;
    data.ivsalt=ivsalt;

    // add dummy data
    const randomLength = Math.floor(Math.random() * 10) + 1; // Random number between 1 and 10
    for (let i = 0; i <randomLength; i++) {
      const dummyString = this.generateDummyString(randomLength)+"dummy";
      const dummyPass = this.generateDummyPass(randomLength);
      //console.log(decodeBuffer(dummyPass))
      dummyStringArray.push(dummyString);
      data.kvs[dummyString]=encodeBuffer(dummyPass)+dummyString
    }


    //secrets
    let rawKey = await subtle.importKey("raw", stringToBuffer(password), {name: "PBKDF2"}, false, ["deriveKey"]);
    let msgKey = await subtle.importKey("raw", stringToBuffer(password), {name: "HMAC", hash: "SHA-256"}, false, ["sign","verify"]);
    let masterKey=rawKey
    
    // console.log('init')

    // console.log(salt)

    let valueKey = await subtle.deriveKey(
      {
        name: "PBKDF2",
        salt,
        iterations: 100000,
        hash: "SHA-256",
      },
      masterKey,
      { name: "AES-GCM", length: 256 },
      true,
      ["encrypt", "decrypt"]
    );
    secrets.msgKey=msgKey;
    secrets.valuekey=valueKey;



    return new Keychain(data,secrets)

   }

  /**
    * Loads the keychain state from the provided representation (repr). The
    * repr variable will contain a JSON encoded serialization of the contents
    * of the KVS (as returned by the dump function). The trustedDataCheck
    * is an *optional* SHA-256 checksum that can be used to validate the 
    * integrity of the contents of the KVS. If the checksum is provided and the
    * integrity check fails, an exception should be thrown. You can assume that
    * the representation passed to load is well-formed (i.e., it will be
    * a valid JSON object).Returns a Keychain object that contains the data
    * from repr. 
    *
    * Arguments:
    *   password:           string
    *   repr:               string
    *   trustedDataCheck: string
    * Return Type: Keychain
    */
  static async load(password, repr, trustedDataCheck) {

    let current_pass_hash=await subtle.digest("SHA-256", stringToBuffer(password))

    if(encodeBuffer(this.hash_master_pass)!=encodeBuffer(current_pass_hash))
    {
        throw new TypeError('incorrect master password ');
    }
    let shacheck = await subtle.digest("SHA-256", stringToBuffer(repr));
    if(encodeBuffer(shacheck) == encodeBuffer(trustedDataCheck)) {
        var keychainData = JSON.parse(repr);
        // console.log(keychainData)
        //data
        var newdata={}
        newdata.kvs = keychainData.kvs;

        //swap attack check...
        for (let k in  newdata.kvs) 
        {
            console.log(k)
            console.log(newdata.kvs[k])

            let flag=newdata.kvs[k].includes(k)
            if(!flag)
            {
                console.log("Swap Attack Detected")
                throw new Error("Swap Attack Detected");
            }
        }
        newdata.salt = new Int8Array(Object.values( keychainData.salt));
        newdata.ivsalt=new Int8Array(Object.values( keychainData.ivsalt))
        // console.log(newdata)

         //secrets
        let rawKey = await subtle.importKey("raw", stringToBuffer(password), {name: "PBKDF2"}, false, ["deriveKey"]);
        let msgKey = await subtle.importKey("raw", stringToBuffer(password), {name: "HMAC", hash: "SHA-256"}, false, ["sign","verify"]);
        let masterKey=rawKey
        
        // console.log('init')

        // console.log(salt)
        let salt=newdata.salt
        let valueKey = await subtle.deriveKey(
          {
            name: "PBKDF2",
            salt,
            iterations: 100000,
            hash: "SHA-256",
          },
          masterKey,
          { name: "AES-GCM", length: 256 },
          true,
          ["encrypt", "decrypt"]
        );
        var newsecrets={};

        newsecrets.msgKey=msgKey;
        newsecrets.valuekey=valueKey;
            

        
        return new Keychain(newdata, newsecrets);
    }
    else if(encodeBuffer(shacheck) != encodeBuffer(trustedDataCheck)){
        throw new Error("Failed to restore the database: Incorrect checksum");
    }
   
}

  /**
    * Returns a JSON serialization of the contents of the keychain that can be 
    * loaded back using the load function. The return value should consist of
    * an array of two strings:
    *   arr[0] = JSON encoding of password manager
    *   arr[1] = SHA-256 checksum (as a string)
    * As discussed in the handout, the first element of the array should contain
    * all of the data in the password manager. The second element is a SHA-256
    * checksum computed over the password manager to preserve integrity.
    *
    * Return Type: array
    */ 
  async dump() {

    for (let i = 0; i < dummyStringArray.length; i++) {
      delete this.data.kvs[dummyStringArray[i]];
    }

    var store = JSON.stringify(this.data);
    let shacheck=await subtle.digest("SHA-256",stringToBuffer(store));
    return [store,shacheck];

  };
  /**
    * Fetches the data (as a string) corresponding to the given domain from the KVS.
    * If there is no entry in the KVS that matches the given domain, then return
    * null.
    *
    * Arguments:
    *   name: string
    * Return Type: Promise<string>
    */
  async get(name) {
    let nameHash=await subtle.digest("SHA-256", stringToBuffer(name));
    let sign=await subtle.sign("HMAC",this.secrets.msgKey,nameHash);
    let verified=await subtle.verify("HMAC",this.secrets.msgKey,sign,nameHash)
    let domainCrypted=bufferToString(sign);
    if(this.data.kvs[domainCrypted] && verified)
    {
      let iv=new Int8Array(16);
      iv=this.data.ivsalt;
      let encryptedpass=this.data.kvs[domainCrypted].replace(domainCrypted,"")
      let decryptedvalue= await subtle.decrypt({ name: "AES-GCM",iv }, this.secrets.valuekey, decodeBuffer(encryptedpass));
      
      return bufferToString(decryptedvalue);
    }
    else
    {
      return null;
    }
  };
  /** 
  * Inserts the domain and associated data into the KVS. If the domain is
  * already in the password manager, this method should update its value. If
  * not, create a new entry in the password manager.
  *
  * Arguments:
  *   name: string
  *   value: string
  * Return Type: void
  */
  async set(name, value) {
    let nameHash=await subtle.digest("SHA-256", stringToBuffer(name));
    let sign=await subtle.sign("HMAC",this.secrets.msgKey,nameHash);
    let domainCrypted=bufferToString(sign);
    let iv=new Int8Array(16);
    iv=this.data.ivsalt;
    let encryptedValue= await subtle.encrypt({ name: "AES-GCM",iv }, this.secrets.valuekey, stringToBuffer(value));

    // console.log(encryptedValue)
    // console.log(encodeBuffer(encryptedValue))
    // console.log(decodeBuffer(encodeBuffer(encryptedValue)))


    this.data.kvs[domainCrypted]=encodeBuffer(encryptedValue)+domainCrypted;


  };

  /**
    * Removes the record with name from the password manager. Returns true
    * if the record with the specified name is removed, false otherwise.
    *
    * Arguments:
    *   name: string
    * Return Type: Promise<boolean>
  */
  async remove(name) {
    let nameHash=await subtle.digest("SHA-256", stringToBuffer(name));
    let sign=await subtle.sign("HMAC",this.secrets.msgKey,nameHash);
    let verified=await subtle.verify("HMAC",this.secrets.msgKey,sign,nameHash)
    let domainCrypted=bufferToString(sign);
    if (this.data.kvs[domainCrypted] && verified) {
      delete this.data.kvs[domainCrypted];
      return true;
    }
    else {
      return false;
    }
  };
  static generateDummyString(length) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
    let dummyString = '';
    for (let i = 0; i < length; i++) {
      dummyString += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return dummyString;
  }
  
  static generateDummyPass(length) {
    const numbers = '0123456789';
    let dummyPass = '';
    for (let i = 0; i < length; i++) {
      dummyPass += numbers.charAt(Math.floor(Math.random() * numbers.length));
    }
    return dummyPass;
  }
  static get PBKDF2_ITERATIONS() { return 100000; }
};


module.exports = { Keychain }
