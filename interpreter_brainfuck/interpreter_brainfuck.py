import argparse
from Brainfuck_Classes import *


def parse_command_line_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--program", dest="prog_file_name",
                        default="brainfuck_hello_world.txt",
                        metavar="PROGRAM", help="Execute this brainfuck code.")

    parser.add_argument("-t", "--type", dest="brainfuck_type",
                        choices=["1", "2", "n"], default="1",
                        metavar="TYPE", help="The type of brainfuck to run.")

    parser.add_argument("-i", "--input", dest="ifn",
                        metavar="INPUTTXT", help="input txt file name")

    args = parser.parse_args()
    return args


def next_instruction(i, bf: Brainfuck):
    """Perform the next i instructions, if i < 0 continues until stopped"""
    while i != 0:
        if bf.next_instruction():
            break
        i -= 1
    return bf


def read_input(file_name: str, bf: Brainfuck):
    with open(file_name) as file:
        txt = file.read()
        io_in(txt, bf)


def io_in(input: str, bf: Brainfuck):
    bf.write(input)


def io_out(i, bf: Brainfuck):
    """Output i characters from brainfuck or until no characters left to output.
    If i is negative, go until no characters left to output"""
    output = ""
    while bf.can_read() and i != 0:
        output += bf.read()
        i -= 1
    return output


def non_matching_while_loops(txt):
    locs = []
    index = 0
    while index < len(txt):
        char = txt[index]
        if char == "]":
            if len(locs) == 0:
                return "] at " + str(index)
            else:
                locs.pop()
        elif char == "[":
            locs.append(index)
        index += 1
    if len(locs) > 0:
        return "[ at " + str(locs)
    return None


def create_interpreter(dimensions: str, file_name: str) -> Brainfuck:
    with open(file_name, "r") as file:
        txt = file.read()
        nmwl = non_matching_while_loops(txt)
        if nmwl is not None:
            raise SyntaxError("While loop doesn't match, unpartnered " + str(nmwl))
        if dimensions == "1":
            bf = One_Dimensional_Brainfuck(txt)
        elif dimensions == "2":
            raise NotImplementedError("No implementation for 2d brainfuck interpreter yet :(")
        elif dimensions == "n":
            raise NotImplementedError("No implementation for nd brainfuck interpreter yet :(")

    return bf


def main():
    args = parse_command_line_args()
    bf = create_interpreter(args.brainfuck_type, args.prog_file_name)
    if args.ifn is not None:
        read_input(args.ifn, bf)
    next_instruction(-1, bf)
    print(io_out(-1, bf))


if __name__ == "__main__":
    main()
