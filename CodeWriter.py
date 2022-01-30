class CodeWriter:
    def __init__(self, filename):
        self.filename = filename
        self.asm_file = open(self.filename, "w")

    def write_asm(self, text):
        self.asm_file.write(text + '\n')

    def increment_stack(self):
        self.write_asm("@SP")
        self.write_asm("M=M+1")

    def decrement_stack(self):
        self.write_asm("@SP")
        self.write_asm("M=M-1")

    def write_arithmetic(self, operation, arg1, arg2, counter):
        arg1 = arg1.strip()
        if arg1 == "not":
            self.arith_not()
            return None
        if arg1 == "neg":
            self.arith_neg()
            return None
        self.decrement_stack()
        self.write_asm("A=M")
        self.write_asm("D=M")
        self.decrement_stack()
        self.write_asm("A=M")
        if arg1 == "add":
            self.write_asm("M=M+D")
        elif arg1 == "sub":
            self.write_asm("M=M-D")
        elif arg1 == "and":
            self.write_asm("M=M&D")
        elif arg1 == "or":
            self.write_asm("M=M|D")
        elif arg1 == "eq":
            self.write_asm("M=M-D")
            self.write_asm("D=M")
            self.write_asm(f"@SetEqBOOL{counter}")
            self.write_asm("D;JEQ")
            self.write_asm("D=0")
            self.write_asm(f"@SKIP{counter}")
            self.write_asm("0;JEQ")
            self.write_asm(f"(SetEqBOOL{counter})")
            self.write_asm("@SP")
            self.write_asm("D=-1")
            self.write_asm(f"(SKIP{counter})")
            self.write_asm("@SP")
            self.write_asm("A=M")
            self.write_asm("M=D")
        elif arg1 == "gt":
            self.write_asm("D=M-D")
            self.write_asm(f"@Greater_than{counter}")
            self.write_asm("D;JGT")
            self.write_asm("D=0")
            self.write_asm(f"@SKIP_GT{counter}")
            self.write_asm("0;JEQ")
            self.write_asm(f"(Greater_than{counter})")
            self.write_asm("@SP")
            self.write_asm("D=-1")
            self.write_asm(f"(SKIP_GT{counter})")
            self.write_asm("@SP")
            self.write_asm("A=M")
            self.write_asm("M=D")
        elif arg1 == "lt":
            self.write_asm("D=M-D")
            self.write_asm(f"@Lesser_than{counter}")
            self.write_asm("D;JLT")
            self.write_asm("D=0")
            self.write_asm(f"@SKIP_LT{counter}")
            self.write_asm("0;JEQ")
            self.write_asm(f"(Lesser_than{counter})")
            self.write_asm("@SP")
            self.write_asm("D=-1")
            self.write_asm(f"(SKIP_LT{counter})")
            self.write_asm("@SP")
            self.write_asm("A=M")
            self.write_asm("M=D")
        self.increment_stack()

    def arith_not(self):
        self.decrement_stack()
        self.write_asm("A=M")
        self.write_asm("D=!M")
        self.write_asm("M=D")
        self.increment_stack()

    def arith_neg(self):
        self.decrement_stack()
        self.write_asm("A=M")
        self.write_asm("D=-M")
        self.write_asm("M=D")
        self.increment_stack()

    def push_stack_to_d(self):
        self.write_asm("@SP")
        self.write_asm("A=M")
        self.write_asm("M=D")
        self.write_asm("@SP")
        self.write_asm("M=M+1")

    def pop_stack_to_d(self):
        self.write_asm("@SP")
        self.write_asm("M=M-1")
        self.write_asm("A=M")
        self.write_asm("D=M")

    def write_push_pop(self, operation, arg1, arg2):
        if operation == "C_PUSH":
            if arg1 == "constant":
                self.write_asm(f"@{arg2}")
                self.write_asm("D=A")
                self.push_stack_to_d()
            elif arg1 == "local":
                self.write_asm(f"@{arg2}")
                self.write_asm("D=A")
                self.write_asm("@LCL")
                self.write_asm(f"A=A+D")
                self.write_asm("D=M")
                self.push_stack_to_d()
            elif arg1 == "argument":
                self.write_asm(f"@{arg2}")
                self.write_asm("D=A")
                self.write_asm("@ARG")
                self.write_asm(f"A=A+D")
                self.write_asm("D=M")
                self.push_stack_to_d()
            elif arg1 == "this":
                self.write_asm(f"@{arg2}")
                self.write_asm("D=A")
                self.write_asm("@THIS")
                self.write_asm(f"A=A+D")
                self.write_asm("D=M")
                self.push_stack_to_d()
            elif arg1 == "that":
                self.write_asm(f"@{arg2}")
                self.write_asm("D=A")
                self.write_asm("@THAT")
                self.write_asm("A=A+D")
                self.write_asm("D=M")
                self.push_stack_to_d()
            elif arg1 == "static":
                self.write_asm(f"@{self.filename}.{arg2}")
                self.write_asm("D=M")
                self.push_stack_to_d()
            elif arg1 == "temp":
                self.write_asm(f"@{(5 + int(arg2))}")
                self.write_asm("D=M")
                self.push_stack_to_d()
            elif arg1 == "pointer":
                arg2 = int(arg2)
                if arg2 == 0:
                    self.write_asm("@THIS")
                    self.write_asm("D=M")
                    self.push_stack_to_d()
                else:
                    self.write_asm("@THAT")
                    self.write_asm("D=M")
                    self.push_stack_to_d()
        elif operation == "C_POP":
            if arg1 == "local":
                self.write_asm(f"@{arg2}")
                self.write_asm("D=A")
                self.write_asm("@LCL")
                self.write_asm("D=D+M")
                self.write_asm(f"@var")
                self.write_asm(f"M=D")
                self.pop_stack_to_d()
                self.write_asm("@var")
                self.write_asm("A=M")
                self.write_asm("M=D")
            elif arg1 == "argument":
                self.write_asm(f"@{arg2}")
                self.write_asm("D=A")
                self.write_asm("@ARG")
                self.write_asm("D=D+M")
                self.write_asm(f"@var")
                self.write_asm(f"M=D")
                self.pop_stack_to_d()
                self.write_asm("@var")
                self.write_asm("A=M")
                self.write_asm("M=D")
            elif arg1 == "this":
                self.write_asm(f"@{arg2}")
                self.write_asm("D=A")
                self.write_asm("@THIS")
                self.write_asm("D=D+M")
                self.write_asm(f"@var")
                self.write_asm(f"M=D")
                self.pop_stack_to_d()
                self.write_asm("@var")
                self.write_asm("A=M")
                self.write_asm("M=D")
            elif arg1 == "that":
                self.write_asm(f"@{arg2}")
                self.write_asm("D=A")
                self.write_asm("@THAT")
                self.write_asm("D=D+M")
                self.write_asm(f"@varr")
                self.write_asm(f"M=D")
                self.pop_stack_to_d()
                self.write_asm("@varr")
                self.write_asm("A=M")
                self.write_asm("M=D")
            elif arg1 == "static":
                self.pop_stack_to_d()
                self.write_asm(f"@{self.filename}.{arg2}")
                self.write_asm("M=D")
            elif arg1 == "temp":
                self.pop_stack_to_d()
                self.write_asm(f"@{(5 + int(arg2))}")
                self.write_asm("M=D")
            elif arg1 == "pointer":
                self.decrement_stack()
                if int(arg2) == 0:
                    self.write_asm("A=M")
                    self.write_asm("D=M")
                    self.write_asm("@THIS")
                    self.write_asm("M=D")
                else:
                    self.write_asm("A=M")
                    self.write_asm("D=M")
                    self.write_asm("@THAT")
                    self.write_asm("M=D")
