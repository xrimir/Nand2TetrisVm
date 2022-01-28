class CodeWriter:
    def __init__(self, filename):
        self.filename = filename
        self.asm_file = open(self.filename, "w")
        self.address_dict = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            'pointer': 3,
            'temp': 5,
            'static': 16,
        }

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
            self.write_asm("//---------------------- ADD --------------------------")
            self.write_asm("M=M+D")
        elif arg1 == "sub":
            self.write_asm("//---------------------- SUB --------------------------")
            self.write_asm("M=M-D")
        elif arg1 == "and":
            self.write_asm("//---------------------- AND --------------------------")
            self.write_asm("M=M&D")
        elif arg1 == "or":
            self.write_asm("M=M|D")
        elif arg1 == "eq":
            self.write_asm("//---------------------- EQ --------------------------")
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
            self.write_asm("//---------------------- GT --------------------------")
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
            self.write_asm("//---------------------- LT --------------------------")
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
        self.write_asm("//---------------------- NOT --------------------------")
        self.decrement_stack()
        self.write_asm("A=M")
        self.write_asm("D=!M")
        self.write_asm("M=D")
        self.increment_stack()

    def arith_neg(self):
        self.write_asm("//---------------------- NEG --------------------------")
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
                self.write_asm("//Writing constant to the stack")
                self.write_asm(f"@{arg2}")
                self.write_asm("D=A")
                self.push_stack_to_d()
            elif operation == "local":
                self.write_asm(f"@{self.address_dict[operation]}")
                self.write_asm(f"A=A+{arg2}")
                self.write_asm("D=M")
                self.push_stack_to_d()
            elif operation == "temp":
                self.write_asm(f"@{5 + arg2}")
                self.write_asm("")
        elif operation == "C_POP":
            if arg1 == "static":
                self.pop_stack_to_d()
                self.write_asm(f"@{self.filename}.{arg2}")
                self.write_asm("M=D")