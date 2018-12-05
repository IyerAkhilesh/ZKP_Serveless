password_dictionary = \
    {
        "0": 7,
        "1": 8,
        "2": 9,
        "3": 10,
        "4": 11,
        "5": 12,
        "6": 13,
        "7": 14,
        "8": 15,
        "9": 16,
        "s": 17,
        "m": 18,
        "a": 19,
        "j": 20,
        "c": 21,
        "d": 22,
        "b": 23,
        "t": 24,
        "r": 25,
        "p": 26,
        "k": 27,
        "l": 28,
        "g": 29,
        "h": 30,
        "n": 31,
        "e": 32,
        "f": 33,
        "w": 34,
        "i": 35,
        "v": 36,
        "o": 37,
        "y": 38,
        "z": 39,
        "u": 40,
        "x": 41,
        "q": 42,
        "S": -17,
        "M": -18,
        "A": -19,
        "J": -20,
        "C": -21,
        "D": -22,
        "B": -23,
        "T": -24,
        "R": -25,
        "P": -26,
        "K": -27,
        "L": -28,
        "G": -29,
        "H": -30,
        "N": -31,
        "E": -32,
        "F": -33,
        "W": -34,
        "I": -35,
        "V": -36,
        "O": -37,
        "Y": -38,
        "Z": -39,
        "U": -40,
        "X": -41,
        "Q": -42,
        "!": 68,
        "@": 69,
        "#": 70,
        "$": 71,
        "%": 72,
        "^": 73,
        "&": 74,
        "*": 75,
        "(": 76,
        ")": 77,
    }

try:
    def username_processor(username_argument):
        ascii_array = []
        for character_counter in range(0, len(username_argument)):
            ascii_array.append(ord(username_argument[character_counter]))

        binary_ascii_array = []
        for array_counter in range(0, len(ascii_array)):
            binary_ascii_array.append('{0:07b}'.format(ascii_array[array_counter]))

        xored_array = ""
        for binary_counter in range(0, len(binary_ascii_array)):
            b = int(binary_ascii_array[binary_counter][0]) ^ int(binary_ascii_array[binary_counter][1]) ^ int(binary_ascii_array[binary_counter][2]) ^ int(binary_ascii_array[binary_counter][3])
            xored_array += "".join(str(b))
            b = int(binary_ascii_array[binary_counter][4]) ^ int(binary_ascii_array[binary_counter][5]) ^ int(binary_ascii_array[binary_counter][6])
            xored_array += "".join(str(b))
        return int(xored_array, 2)

    def factorizer(composite_number, option):
        factors = []
        for counter in range(2, composite_number):
            if composite_number % counter == 0:
                factors.append(counter)

        number_of_factors = len(factors)
        if number_of_factors > 1:
            if option == 0:
                try:
                    factor_one = factors[int(number_of_factors/2) - 1]
                    factor_two = factors[int(number_of_factors/2)]
                    factors_string = "" + str(factor_one) + "," + str(factor_two)
                    return factors_string
                except:
                    print("Exception: Please enter a different username password pair!")
            # modulus = int(number_of_factors*random())
            # factor_one = str(factors[modulus])
            # factor_two = str(factors[number_of_factors - modulus - 1])
            else:
                try:
                    factor_one = factors[int(number_of_factors/4)]
                    factor_two = factors[number_of_factors - int(number_of_factors/4)]
                    factors_string = "" + str(factor_one) + "," + str(factor_two)
                    return factors_string
                except:
                    print("Exception: Please enter a different username password pair!")
        else:
            print("Else: Please enter a different username password pair!")

    def password_to_number(argument_password):
        masking_sum = 0
        for counter in range(0, len(argument_password)):
            masking_sum = masking_sum + password_dictionary.get(argument_password[counter])
        print("Password: ", masking_sum)
        return masking_sum
except:
    print("Re-enter username and password")