import argparse
from Brainfuck_Classes import *


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-p", "--program", dest="prog_file_name",
                       default="examples/1d/1-brainfuck_hello_world.brainfuck1",
                       metavar="PROGRAM", help="Execute this brainfuck code.")

    group.add_argument("-e", "--example", dest="example",
                       choices=["None", "1-1", "1-2"], default="None",
                       metavar="EXAMPLE", help="example file number, instead of program file name")

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


def console_connected_interpretation(bf):
    stop = False
    while not stop:
        try:
            stop = bf.next_instruction()
        except BufferError:
            bf.write(input("\n$ "))
            bf.instruction_pointer -= 1
        print(io_out(-1, bf), end="")


def main():
    args = parse_command_line_args()
    pfn = args.prog_file_name
    if args.example != "None":
        if args.example == "1-1":
            pfn = "/examples/1d/1-brainfuck_hello_world.brainfuck1"
        elif args.example == "1-2":
            pfn = "examples/1d/2-brainfuck_rot13.brainfuck1"
    bf = create_interpreter(args.brainfuck_type, pfn)
    if args.ifn is not None:
        read_input(args.ifn, bf)
        next_instruction(-1, bf)
        print(io_out(-1, bf))
    else:
        console_connected_interpretation(bf)


if __name__ == "__main__":
    main()
