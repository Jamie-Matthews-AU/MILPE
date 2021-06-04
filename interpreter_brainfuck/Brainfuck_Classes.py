import io
import queue


class Brainfuck:
    def __init__(self, instructions, tape=None, tape_pointer=0, behavior=None, instruction_pointer=0):
        """

        :type tape: list[int]
            the tape of the program
        :type instructions: list["str"]
            queue of instructions, left to right
        :type behavior: list[int]
            what to fill new tape slots with, based on (1-indexed) index of tape modulo length of behavior
        """
        self.instructions = instructions
        self.tape = tape
        self.tape_pointer = tape_pointer
        self.behavior = behavior
        self.instruction_pointer = instruction_pointer
        self.behavior_pointer = 0
        self.io_in_queue = queue.Queue(0)
        self.io_out_queue = queue.Queue(0)
        self.while_locations = None

    def read(self):
        try:
            return str(self.io_out_queue.get(block=False))
        except queue.Empty:
            return None

    def can_read(self):
        return self.io_out_queue.qsize() > 0

    def write(self, item: str):
        for c in item:
            self.io_in_queue.put(ord(c), block=False)

    def append_tape(self, left_append=False):
        pass

    def next_instruction(self):
        return True

    def current_tape_val(self):
        return 0

    def find_one_after_matching_right_square_bracket(self):
        depth = 1
        ip = self.instruction_pointer  # Begin at point after left square bracket
        while depth > 0:
            if ip >= len(self.instructions):
                raise Exception("No matching right square bracket for square bracket at "
                                + str(self.instruction_pointer))
            instruction = self.instructions[ip]
            ip += 1
            if instruction == "]":
                depth -= 1
            elif instruction == "[":
                depth += 1

        return ip


class One_Dimensional_Brainfuck(Brainfuck):
    def __init__(self, instructions, tape=None, tape_pointer=0, behavior=None, instruction_pointer=0):
        """

        :type tape: list[int]
            the tape of the program
        :type instructions: list["str"]
            queue of instructions, left to right
        :type behavior: list[int]
            what to fill new tape slots with, based on (1-indexed) index of tape modulo length of behavior
        """
        self.instructions = instructions
        if behavior is None:
            self.behavior = [0]
        else:
            self.behavior = behavior
        self.behavior_pointer = 0  # Behavior pointer is the index in behavior list which corresponds to index 0 in tape

        if tape is None:
            self.tape = [self.behavior[0]]
        else:
            self.tape = tape

        self.tape_pointer = tape_pointer
        self.io_in_queue = queue.Queue(0)
        self.io_out_queue = queue.Queue(0)

        self.while_locations = []
        self.instruction_pointer = instruction_pointer

        # ENFORCE pointer must begin within tape by extending tape
        while self.tape_pointer > len(self.tape):
            self.append_tape()
        while self.tape_pointer < 0:
            self.append_tape(True)
            self.tape_pointer += 1

    def read(self):
        try:
            return str(self.io_out_queue.get(block=False))
        except queue.Empty:
            return None

    def can_read(self):
        return self.io_out_queue.qsize() > 0

    def write(self, item: str):
        for c in item:
            self.io_in_queue.put(ord(c), block=False)

    def append_tape(self, left_append=False):
        if left_append:
            self.behavior_pointer = self.behavior_pointer - 1
            next_item = self.behavior[self.behavior_pointer]
            self.tape.insert(0, next_item)
            if len(self.behavior) + self.behavior_pointer == 0:
                self.behavior_pointer = 0  # Wraparound has occurred
        else:
            ind = (len(self.tape) % len(self.behavior)) - self.behavior_pointer
            self.tape.append(self.behavior[ind])

    def next_instruction(self):
        if self.instruction_pointer >= len(self.instructions):
            return True  # Finished = True
        instruction = self.instructions[self.instruction_pointer]
        self.instruction_pointer += 1

        if instruction == "<":
            if self.tape_pointer == 0:
                self.append_tape(True)
            else:
                self.tape_pointer -= 1
        elif instruction == ">":
            if self.tape_pointer == len(self.tape) - 1:
                self.append_tape()
            self.tape_pointer += 1
        elif instruction == "+":
            self.tape[self.tape_pointer] = (self.current_tape_val() + 1) % 256
        elif instruction == "-":
            self.tape[self.tape_pointer] = (self.current_tape_val() - 1) % 256
        elif instruction == ".":
            self.io_out_queue.put(chr(self.current_tape_val()))
        elif instruction == ",":
            if self.io_in_queue.qsize() > 0:
                read_in = self.io_in_queue.get(block=False)
                self.tape[self.tape_pointer] = read_in
            else:
                raise BufferError("No items to read in")
        elif instruction == "[":
            if self.current_tape_val() == 0:
                matching = self.find_one_after_matching_right_square_bracket()
                self.instruction_pointer = matching
            else:
                self.while_locations.append(self.instruction_pointer - 1)
        elif instruction == "]":
            if len(self.while_locations) > 0:
                back = self.while_locations.pop()
                if self.current_tape_val() != 0:
                    self.instruction_pointer = back
            else:
                raise Exception("Attempted to break from while loop that does not have entry point at "
                                + str(self.instruction_pointer))

        if self.instruction_pointer >= len(self.instructions):
            return True
        else:
            return False

    def current_tape_val(self):
        return self.tape[self.tape_pointer]

    def find_one_after_matching_right_square_bracket(self):
        depth = 1
        ip = self.instruction_pointer  # Begin at point after left square bracket
        while depth > 0:
            if ip >= len(self.instructions):
                raise Exception("No matching right square bracket for square bracket at "
                                + str(self.instruction_pointer))
            instruction = self.instructions[ip]
            ip += 1
            if instruction == "]":
                depth -= 1
            elif instruction == "[":
                depth += 1

        return ip