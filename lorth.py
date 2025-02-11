#!/usr/bin/env python3
iota_counter = 0
import sys
import subprocess
def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result

OP_PUSH=iota(True)
OP_PLUS=iota()
OP_MINUS=iota()
OP_DUMP=iota()
COUNT_OPS=iota()

def push(x):
    return (OP_PUSH, x)
def plus():
    return (OP_PLUS, )
def minus():
    return (OP_MINUS, )
def dump():
    return (OP_DUMP, )
def simulate_program(program):
    stack = []
    for op in program:
        assert COUNT_OPS == 4, "Exhaustive handling of operation in simulation"
        if op[0] == OP_PUSH:
            stack.append(op[1])
        elif op[0] == OP_PLUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)
        elif op[0] == OP_MINUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
        elif op[0] == OP_DUMP:
            a = stack.pop()
            print(a)
        else:
            assert False, "unreachable"
def compile_program(program, out_file_path):
    with open(out_file_path, "w") as out:
        out.write("dump:\n")
        out.write("    push    rbp\n") 
        out.write("    mov     rbp, rsp\n") 
        out.write("    sub     rsp, 64\n") 
        out.write("    mov     QWORD [rbp-56], rdi\n") 
        out.write("    mov     QWORD [rbp-8], 1\n") 
        out.write("    mov     eax, 32\n") 
        out.write("    sub     rax, QWORD  [rbp-8]\n") 
        out.write("    mov     BYTE  [rbp-48+rax], 10\n") 
        out.write(".L2:\n") 
        out.write("    mov     rcx, QWORD  [rbp-56]\n") 
        out.write("    mov  rdx, -3689348814741910323\n") 
        out.write("    mov     rax, rcx\n") 
        out.write("    mul     rdx\n") 
        out.write("    shr     rdx, 3\n") 
        out.write("    mov     rax, rdx\n") 
        out.write("    sal     rax, 2\n") 
        out.write("    add     rax, rdx\n") 
        out.write("    add     rax, rax\n") 
        out.write("    sub     rcx, rax\n") 
        out.write("    mov     rdx, rcx\n") 
        out.write("    mov     eax, edx\n") 
        out.write("    lea     edx, [rax+48]\n") 
        out.write("    mov     eax, 31\n") 
        out.write("    sub     rax, QWORD  [rbp-8]\n") 
        out.write("    mov     BYTE  [rbp-48+rax], dl\n") 
        out.write("    add     QWORD  [rbp-8], 1\n") 
        out.write("    mov     rax, QWORD  [rbp-56]\n") 
        out.write("    mov  rdx, -3689348814741910323\n") 
        out.write("    mul     rdx\n") 
        out.write("    mov     rax, rdx\n") 
        out.write("    shr     rax, 3\n") 
        out.write("    mov     QWORD  [rbp-56], rax\n") 
        out.write("    cmp     QWORD  [rbp-56], 0\n") 
        out.write("    jne     .L2\n") 
        out.write("    mov     eax, 32\n") 
        out.write("    sub     rax, QWORD  [rbp-8]\n") 
        out.write("    lea     rdx, [rbp-48]\n") 
        out.write("    lea     rcx, [rdx+rax]\n") 
        out.write("    mov     rax, QWORD  [rbp-8]\n") 
        out.write("    mov     rdx, rax\n") 
        out.write("    mov     rsi, rcx\n") 
        out.write("    mov     edi, 1\n") 
        out.write("    mov     rax, 1\n")
        out.write("    syscall\n") 
        out.write("    nop\n") 
        out.write("    leave\n") 
        out.write("    ret\n")
        out.write("section .data\n")
        out.write('fmt db "Number: %d", 10, 0\n')

        out.write("section .text\n")
        out.write("global _start\n")
        out.write("extern printf\n")

        out.write("_start:\n")
        out.write("lea rdi, [fmt]\n")
        out.write("mov rsi, 69\n")
        out.write("xor rax, rax\n")
        out.write("call printf\n")

        out.write("lea rdi, [fmt]\n")
        out.write("mov rsi, 420\n")
        out.write("xor rax, rax\n")
        out.write("call printf\n")

        out.write("lea rdi, [fmt]\n")
        out.write("mov rsi, 30\n")
        out.write("xor rax, rax\n")
        out.write("call printf\n")

        out.write("mov eax, 60\n")
        out.write("xor edi, edi\n")
        out.write("syscall\n")


        for op in program:
            assert COUNT_OPS == 4, "Exhausive handling of ops in compilation"
            if op[0] == OP_PUSH:
                out.write("    ;; -- push %d --\n" % op[1])
                out.write("    push %d\n" % op[1])
            elif op[0] == OP_PLUS:
                out.write("    ;; -- plus --\n")
                out.write("    pop rax\n")
                out.write("    pop rbx\n")
                out.write("    add rax, rbx\n")
                out.write("    push rax\n")
            elif op[0] == OP_MINUS:
                out.write("    ;; -- minus --\n")
                out.write("    pop rax\n")
                out.write("    pop rbx\n")
                out.write("    sub rax, rbx\n")
                out.write("    push rbx\n")
            elif op[0] == OP_DUMP:
                out.write("    ;; -- dump --\n")
                out.write("    pop rdi\n")
                out.write("    call dump\n")
            else:
                assert False, "unreachable"
def parse_word_as_op(word):
    assert COUNT_OPS == 4, "Exhaustive op handling in parse_word_as_op"
    if word == "+":
        return plus()
    elif word == '-':
        return minus()
    elif word == ".":
        return dump()
    else:
        return push(int(word))
def load_program_from_file(file_path):
    with open(file_path, "r") as f:
        return [parse_word_as_op(word) for word in f.read().split()]

program=[push(34), push(35), plus(), dump(), push(500), push(80), minus(), dump()]
def usage(program):
    print("Usage: %s <SUBCOMMAND> [ARGS]", program)
    print("SUBCOMMANDS:")
    print("    sim <file>    Simulate the program")
    print("    com <file>    Compile the program")

def call_cmd(cmd):
    print(cmd)
    subprocess.call(cmd)
def uncons(xs):
    return (xs[0], xs[1:])

if __name__ == '__main__':
    argv = sys.argv
    assert len(argv) >= 1
    print(argv)
    (program_name, argv) = uncons(argv)
    print(argv)
    if len(argv) < 1:
        usage(program_name)
        print("ERROR: no subcommand is provided")
        exit(1)
    (subcommand, argv) = uncons(argv)
    print(argv)
    #argv = argv[1:]
    print(argv)
    if subcommand == "sim":
        if len(argv) < 1:
            usage(program_name)
            print("ERROR: no input file is provided for the simulation")
            exit(1)
        (program_path, argv) = uncons(argv)
        program = load_program_from_file(program_path)
        simulate_program(program)
    elif subcommand == "com":
        if len(argv) < 1:
            usage(program_name)
            print("ERROR: no input file is provided for the compilation")
            exit(1)
        (program_path, argv) = uncons(argv)
        program = load_program_from_file(program_path)
        compile_program(program, "output.asm")
        call_cmd(["nasm", "-f", "elf64", "output.asm", "-o", "output.o"])
        call_cmd(["gcc", "-nostartfiles",  "output.o", "-o", "output", "-no-pie"])
    else:
        usage()
        print("ERROR: unknown subcommand %s" % (subcommand))
        exit(1)

