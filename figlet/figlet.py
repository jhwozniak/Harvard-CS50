#converts input text using FIGlet library
from pyfiglet import Figlet
from sys import argv
import sys
import random

fonts_list = ["slant", "alphabet", "banner", "basic", "lean", "rectangles"]
random_font = random.choice(fonts_list)

if len(argv) == 1:
    text = input("Input: ")
    f = Figlet(font=random_font)
    print(f.renderText(text))
    sys.exit(0)

elif len(argv) == 3:
    if argv[1] in ["-f", "--font"]:
        if argv[2] in fonts_list:
            text = input("Input: ")
            f = Figlet(font=argv[2])
            print(f.renderText(text))
            sys.exit(0)
        else:
            print("Invalid usage.")
            sys.exit(3)
    else:
        print("Invalid usage.")
        sys.exit(2)
else:
    print("Invalid usage.")
    sys.exit(1)



