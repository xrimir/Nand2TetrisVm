class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.vmfile = open(filename, 'r')
        self.arg1 = ""
        self.arg2 = ""
        self.current_instruction = ""
        self.next_instruction = ""
        self.command_dict = {
            'add': 'C_ARITHMETIC',
            'sub': 'C_ARITHMETIC',
            'neg': 'C_ARITHMETIC',
            'eq': 'C_ARITHMETIC',
            'gt': 'C_ARITHMETIC',
            'lt': 'C_ARITHMETIC',
            'and': 'C_ARITHMETIC',
            'or': 'C_ARITHMETIC',
            'not': 'C_ARITHMETIC',
            'push': 'C_PUSH',
            'pop': 'C_POP',
            'label': 'C_LABEL',
            'goto': 'C_GOTO',
            'if-goto': 'C_IF',
            'function': 'C_FUNCTION',
            'return': 'C_RETURN',
            'call': 'C_CALL'
        }

    def init_file(self):
        self.vmfile.seek(0, 0)
        self.load_next_instruction()

    def strip_line(self, l):
        if l:
            char = l[0]
            if char == "\n" or char == "/":
                return "nl"
            else:
                return l

    def has_more_commands(self):
        return bool(self.next_instruction)

    def load_next_instruction(self):
        line = self.strip_line(self.vmfile.readline())
        while line == "nl":
            line = self.strip_line(self.vmfile.readline())
        if line is not None:
            self.next_instruction = line
        else:
            self.next_instruction = False

    def get_command_type(self, command):
        return self.command_dict[command.strip()]

    def get_arg1(self):
        return self.arg1

    def get_arg2(self):
        return self.arg2

    def advance(self):
        self.current_instruction = self.next_instruction
        cmd_type = self.current_instruction
        c_type = self.current_instruction
        if " " in self.current_instruction:
            cmd_type = self.current_instruction.split(" ")[0]
        cmd_type = self.get_command_type(cmd_type)
        if cmd_type == "C_ARITHMETIC":
            self.arg1 = self.current_instruction
            self.arg2 = self.current_instruction
        else:
            self.arg1 = self.current_instruction.split(" ")[1]
            self.arg2 = self.current_instruction.split(" ")[2]
        self.load_next_instruction()
        return cmd_type, self.get_arg1(), self.get_arg2()
