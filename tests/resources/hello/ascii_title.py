from art import text2art

def generate_ascii_art_program():
    # Generate the ASCII art string using the art library
    ascii_art = text2art("Hello Ublique!", font='block')
    return ascii_art

def main():
    # Generate the program to print the ASCII art
    program = generate_ascii_art_program()
    print("HELLLO")
    # Run the program
    print(program)

main()