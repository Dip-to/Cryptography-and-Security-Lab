import operator

# Irreducible polynomial for GF(2^8)
IRREDUCIBLE_POLY = 0x11B

def bitstring_to_int(bitstring):
    return int(bitstring, 2)

def int_to_bitstring(n):
    return bin(n)[2:]

def add_poly(a, b):
    return reduce_poly(a ^ b)

def multiply_poly(a, b):
    result = 0
    while b > 0:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result

# Reduction of a polynomial modulo the irreducible polynomial
def reduce_poly(poly):
    # Degree of the irreducible polynomial
    degree = IRREDUCIBLE_POLY.bit_length() - 1
    poly_degree = poly.bit_length() - 1
    while poly_degree >= degree:
        diff = poly_degree - degree
        poly ^= IRREDUCIBLE_POLY << diff
        poly_degree = poly.bit_length() - 1
    return poly

# Polynomial multiplication with modulo reduction
def multiply_poly_mod(a, b):
    return reduce_poly(multiply_poly(a, b))

# Polynomial division
def divide_poly(dividend, divisor):
    if divisor == 0:
        raise ValueError("Divisor cannot be zero.")

    quotient = 0  # Initialize quotient
    remainder = dividend  # Initialize remainder

    # Loop until the degree of the remainder is less than the degree of the divisor
    while remainder.bit_length() >= divisor.bit_length():
        # Find the degree difference between remainder and divisor
        degree_diff = remainder.bit_length() - divisor.bit_length()
        # Shift the divisor to align with the most significant bit of the remainder
        shifted_divisor = divisor << degree_diff
        # Subtract the shifted divisor from the remainder
        remainder = add_poly(remainder, shifted_divisor)
        # Update the quotient by setting the bit at the appropriate position
        quotient |= (1 << degree_diff)

    print("Quotient (bit string):", int_to_bitstring(quotient))
    print("Remainder (bit string):", int_to_bitstring(remainder))

    return quotient, remainder

# Main calculator function
def polynomial_calculator():
    try:
        # User input
        first_operand = bitstring_to_int(input("Enter the first operand (bit string): "))
        second_operand = bitstring_to_int(input("Enter the second operand (bit string): "))
        operator_input = input("Enter the operator (+, -, *, /): ").strip()

        # Perform operation
        if operator_input == '+':
            result = add_poly(first_operand, second_operand)
        elif operator_input == '-':
            result = add_poly(first_operand, second_operand)  # Same as addition in GF(2^n)
        elif operator_input == '*':
            result = multiply_poly_mod(first_operand, second_operand)
        elif operator_input == '/':
            if second_operand == 0:
                raise ValueError("Division by zero is not allowed.")
            quotient, remainder = divide_poly(first_operand, second_operand)
        else:
                raise ValueError("Invalid operator. Please use +, -, * or /.")
        if operator_input != '/':
            print("Result (bit string):", int_to_bitstring(result))
    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

# Run the calculator
polynomial_calculator()