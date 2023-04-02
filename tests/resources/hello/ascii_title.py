from art import text2art
import os
def generate_ascii_art_program():
    # check if exists the ART_title environment variable
    if 'ART_TITLE' in os.environ:
        title = os.environ['ART_title']
    else:
        title = "PEMPEM!"
    # Generate the ASCII art string using the art library
    ascii_art = text2art(title, font='block')
    return ascii_art

def main():
    # Generate the program to print the ASCII art
    program = generate_ascii_art_program()
    print("HELLLO")
    # Run the program
    print(program)

main()