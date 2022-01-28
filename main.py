import sys

from CodeWriter import CodeWriter
from Parser import Parser


def get_source_filename():
    return sys.argv[-1]


def get_destination_filename():
    return f"{get_source_filename().split('.vm')[0]}.asm"


def translate_file():
    counter = 1
    cw = CodeWriter(get_destination_filename())
    p = Parser(get_source_filename())
    p.init_file()
    while p.has_more_commands():
        cmd_type, arg1, arg2 = p.advance()
        if cmd_type == "C_ARITHMETIC":
            cw.write_arithmetic(cmd_type, arg1, arg2, counter)
        else:
            cw.write_push_pop(cmd_type, arg1, arg2)
        counter += 1
    p.vmfile.close()


translate_file()
