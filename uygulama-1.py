import time
import random

class MersenneTwister:
    def __init__(self, seed):
        self.n = 624
        self.m = 397
        self.w = 32
        self.r = 31
        self.a = 0x9908b0df
        self.u = 11
        self.s = 7
        self.t = 15
        self.l = 18
        self.b = 0x9d2c5680
        self.c = 0xefc60000
        self.f = 1812433253
        self.state_array = [0] * self.n
        self.state_index = 0
        self.initialize_state(seed)
    
    def initialize_state(self, seed):
        self.state_array[0] = seed
        for i in range(1, self.n):
            seed = self.f * (seed ^ (seed >> (self.w - 2))) + i
            self.state_array[i] = seed
        self.state_index = 0
    
    def random_uint32(self):
        k = self.state_index
        j = k - (self.n - 1)
        if j < 0:
            j += self.n
        x = (self.state_array[k] & ((1 << self.r) - 1)) | (self.state_array[j] & ((1 << (self.w - self.r)) - 1))
        xA = x >> 1
        if x & 1:
            xA ^= self.a
        j = k - (self.n - self.m)
        if j < 0:
            j += self.n
        x = self.state_array[j] ^ xA
        self.state_array[k] = x
        if k + 1 >= self.n:
            self.state_index = 0
        else:
            self.state_index += 1
        y = x ^ (x >> self.u)
        y ^= ((y << self.s) & self.b)
        y ^= ((y << self.t) & self.c)
        return (y ^ (y >> self.l)) & 0xFFFFFFFF

def generate_mersenne_twister(seed, filename="mt_numbers.txt"):
    mt = MersenneTwister(seed)
    with open(filename, "w") as f:
        for _ in range(100):
            f.write(f"{mt.random_uint32()}\n")

class Xorshift:
    def __init__(self, seed=None):
        if seed is None:
            seed = random.getrandbits(32)
        self.state = seed
    
    def next(self):
        self.state ^= (self.state << 13) & 0xFFFFFFFF
        self.state ^= (self.state >> 17)
        self.state ^= (self.state << 5) & 0xFFFFFFFF
        return self.state & 0xFFFFFFFF

def generate_xorshift(seed, filename="xorshift_numbers.txt"):
    prng = Xorshift(seed)
    with open(filename, "w") as f:
        for _ in range(100):
            f.write(f"{prng.next()}\n")

class PCG:
    def __init__(self, seed=None):
        if seed is None:
            seed = int(time.time())
        self.state = seed & 0xFFFFFFFFFFFFFFFF
        self.MULTIPLIER = 6364136223846793005
        self.INCREMENT = 1442695040888963407
        self.MASK_32 = 0xFFFFFFFF
    
    def next(self):
        self.state = (self.state * self.MULTIPLIER + self.INCREMENT) & 0xFFFFFFFFFFFFFFFF
        xorshifted = ((self.state >> 18) ^ self.state) >> 27
        rot = self.state >> 59
        return ((xorshifted >> rot) | (xorshifted << ((-rot) & 31))) & self.MASK_32

def generate_pcg(seed, filename="pcg_numbers.txt"):
    pcg = PCG(seed)
    with open(filename, "w") as f:
        for _ in range(100):
            f.write(f"{pcg.next()}\n")

class BlumBlumShub:
    def __init__(self, seed=None):
        if seed is None:
            seed = int(time.time())
        self.p = 499
        self.q = 547
        self.n = self.p * self.q
        self.state = (seed * seed) % self.n
    
    def next(self):
        self.state = (self.state * self.state) % self.n
        return self.state & 0xFFFFFFFF

def generate_bbs(seed, filename="bbs_numbers.txt"):
    bbs = BlumBlumShub(seed)
    with open(filename, "w") as f:
        for _ in range(100):
            f.write(f"{bbs.next()}\n")

def main():
    seed = 42
    generate_mersenne_twister(seed)
    generate_xorshift(seed)
    generate_pcg(seed)
    generate_bbs(seed)
    print("Tüm rastgele sayılar dosyalara kaydedildi.")

if __name__ == "__main__":
    main()