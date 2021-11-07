class OpcodeComputer:
    def __init__(self) -> None:
        self.mem = [0] * 4
    
    # Set memory
    def set_mem(self, mem):
        self.mem = mem
    
    # Run an instruction string, for example "addr 3 5 7"
    def run_instruction(self, instr_str):
        instruction = instr_str.split(' ')
        opcode = instruction[0] 
        A, B, C = tuple(map(int, instruction[1:]))
        command = f"self._OpcodeComputer__{opcode}({A},{B},{C})" # https://stackoverflow.com/questions/46284205/call-private-class-function-in-exec-python     
        exec(command)
        
    # Addition
    def __addr(self, A, B, C):
        self.mem[C] = self.mem[A] + self.mem[B]
    
    def __addi(self, A, B, C):
        self.mem[C] = self.mem[A] + B
    
    # Multiplication
    def __mulr(self, A, B, C):
        self.mem[C] = self.mem[A] * self.mem[B]
    
    def __muli(self, A, B, C):
        self.mem[C] = self.mem[A] * B
    
    # Bitwise AND
    def __banr(self, A, B, C):
        self.mem[C] = self.mem[A] & self.mem[B]
    
    def __bani(self, A, B, C):
        self.mem[C] = self.mem[A] & B
    
    # Bitwise OR
    def __borr(self, A, B, C):
        self.mem[C] = self.mem[A] | self.mem[B]
    
    def __bori(self, A, B, C):
        self.mem[C] = self.mem[A] | B
    
    # Assignment
    def __setr(self, A, B, C):
        self.mem[C] = self.mem[A]
    
    def __seti(self, A, B, C):
        self.mem[C] = A

    # Greater-than
    def __gtir(self, A, B, C):
        self.mem[C] = int(A > self.mem[B])
    
    def __gtri(self, A, B, C):
        self.mem[C] = int(self.mem[A] > B)
    
    def __gtrr(self, A, B, C):
        self.mem[C] = int(self.mem[A] > self.mem[B])
    
    # Equality
    def __eqir(self, A, B, C):
        self.mem[C] = int(A == self.mem[B])
    
    def __eqri(self, A, B, C):
        self.mem[C] = int(self.mem[A] == B)
    
    def __eqrr(self, A, B, C):
        self.mem[C] = int(self.mem[A] == self.mem[B])
