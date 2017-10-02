from __future__ import print_function
import argparse


ValidRanges = {(0,126), }

class Colors:
    purple = '\033[95m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    grey = '\033[1;37m'
    darkgrey = '\033[1;30m'
    cyan = '\033[1;36m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class CLIArgParser(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--file", type=str, help="path to the solidity source file")
        self.args = parser.parse_args()

    def getFilePath(self):
        return self.args.file


class Doppelgaenger():
    def __init__(self, sol_file_path):
        self.sol_file = open(sol_file_path, "r")

    def isLineComment(self, line):
        return False

    def isHalfLineComment(self, line):
        return False

    def isComment(self):
        return self.isLineComment or self.isHalfLineComment

    def findAPoser(self):
        found_an_impostor = False
        line_number = int()
        char_number = int()
        whitespace_counter = int()
        for line in self.sol_file:
            char_number = 0
            line_number += 1
            for char in line:
                char_number += 1
                for min, max in ValidRanges:
                    if ord(char) > max or ord(char) < min and not self.isComment():
                        if not found_an_impostor:  found_an_impostor = True
                        print(Colors.red + "found an imposter: " + Colors.ENDC)
                        print(Colors.red + "line number: " + repr(line_number) + Colors.ENDC)
                        print(Colors.red + "column number: " + repr(char_number) + Colors.ENDC)
                        print(line[0:char_number - 1], end = '')
                        print(' ' + line[char_number-1:char_number] + ' ', end = '')
                        print(line[char_number:])
                    if whitespace_counter > 60:
                        found_an_impostor = True
                        print(Colors.red + "Too many whiteapces..." + Colors.ENDC)
                        print(Colors.red + "line number: " + repr(line_number) + Colors.ENDC)
                        print(Colors.red + "column number: " + repr(char_number) + Colors.ENDC)
                    if ord(char) == 32: whitespace_counter += 1
                    else: whitespace_counter = 0
        if not found_an_impostor:
            print(Colors.green + "Doppelgaenger: Nothing found. Passed." + Colors.ENDC)

    def run(self):
        self.findAPoser()


def main():
    argparser = CLIArgParser()
    file_path = argparser.getFilePath()
    doppelgaenger = Doppelgaenger(file_path)
    doppelgaenger.run()


if __name__ == "__main__":
    main()
