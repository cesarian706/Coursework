import cs50
import sys
# check for correct input
if len(sys.argv) != 2:
    print("Enter non-negative integer!")
    exit(1)
# get original text from user
print("plaintext: ", end= "")
p = cs50.get_string()
# print encoded string
print("ciphertext: ", end= "")
# iterate through string
for c in p:
    # check for letters
    if c.isalpha() == True:
        # check for letter case, implement cipher shift
        if c.isupper() == True:
            print(chr((((ord(c) - 65) + int(sys.argv[1])) % 26) + 65), end= "")

        elif c.islower() == True:
            print(chr((((ord(c) - 97) + int(sys.argv[1])) % 26) + 97), end= "")
    # print original text for non-letters
    else:
        print(c, end= "")
# print newline to keep terminal looking neat
print()
