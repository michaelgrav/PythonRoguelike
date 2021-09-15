# A simple Caesar Cipher program
# Written by Michael Graves

# Encryption method
def encrypt(inputtext, shiftamount):
    encrypted_text = ""

    # Loop through each character
    for i in range(len(inputtext)):
        char = inputtext[i]

        # If the character is an uppercase, we treat it differently
        if char.isupper():
            encrypted_text += chr((ord(char) + shiftamount - 65) % 26 + 65)

        # If the character is lowercase
        else:
            encrypted_text += chr((ord(char) + shiftamount - 97) % 26 + 97)

    return encrypted_text


text = input("Enter the phrase to be encoded: ")
shift = int(input("Enter amount to be shifted: "))
print(encrypt(text, shift))
