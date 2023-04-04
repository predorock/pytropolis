from art import text2art
import os
import sys
def generate_ascii_art_program():
    output = None
    # check if exists the ART_TITLE environment variable
    title = None
    subtitle = None

    if 'ART_TITLE' in os.environ:
        title = os.environ['ART_TITLE']
    else:
        title = "PEMPEM!"
    
    # check if there are same named command line arguments
    if '--subtitle' in sys.argv:
        # Get the index of the name argument
        index = sys.argv.index('--subtitle')
        # Get the value of the name argument
        subtitle = sys.argv[index + 1]
        # Use the value of the name argument
    else:
        subtitle = ""
    
    output = text2art(title, font='block')
    output += "\n" + text2art(subtitle, font='block')

    
    return output

def main():
    # Generate the program to print the ASCII art
    program = generate_ascii_art_program()
    # Run the program
    print(program)

main()