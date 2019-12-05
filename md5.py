import math


class Md5Checker:
    def __init__(self, byte_stream):
        self.byte_stream = byte_stream
        self.A = 0x67452301
        self.B = 0xefcdab89
        self.C = 0x98badcfe
        self.D = 0x10325476
        self.s = [
            7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
            5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
            4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
            6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
        ]
        self.K = []
        for i in range(64):
            self.K.append(math.floor(2**32 * abs(math.sin(i + 1))))
        self.padding()
        print(bin(self.byte_stream))
        print(hex(self.byte_stream))
        print(self.byte_stream.bit_length())
        self.chunk_num = (len(bin(self.byte_stream)[2:]) + 511) // 512
        self.chunks = []
        dup_bytes = self.byte_stream
        for i in range(self.chunk_num):
            self.chunks.append(dup_bytes % (2 ** 512))
            dup_bytes = dup_bytes >> 512
        self.chunks.reverse()
        print('\n'.join(list(map(lambda chunk: bin(chunk)[2:], self.chunks))))

    def padding(self):
        origin_length = (len(bin(self.byte_stream)[2:]) + 7) // 8 * 8
        self.byte_stream = self.byte_stream << 8
        self.byte_stream += 0x80
        cur_length = origin_length + 8
        padding_length = 512 - 64 - cur_length % (512 - 64)
        self.byte_stream = self.byte_stream << padding_length
        self.byte_stream = (self.byte_stream << 64) + origin_length % (2 ** 64)

    def F(self, X, Y, Z):
        return (X & Y) | ((~X) & Z)

    def G(self, X, Y, Z):
        return (X & Z) | (Y & (~Z))

    def H(self, X, Y, Z):
        return X ^ Y ^ Z

    def I(self, X, Y, Z):
        return Y ^ (X | (~Z))

    def FF(self, a, b, c, d, Mj, s, ti):
        a += (self.F(b, c, d) & 0xffffffff) + Mj + ti
        a = ((a & 0xffffffff) << s) | ((a & 0xffffffff) >> (32 - s))
        a += b
        return a & 0xffffffff

    def GG(self, a, b, c, d, Mj, s, ti):
        a += (self.G(b, c, d) & 0xffffffff) + Mj + ti
        a = ((a & 0xffffffff) << s) | ((a & 0xffffffff) >> (32 - s))
        a += b
        return a & 0xffffffff

    def HH(self, a, b, c, d, Mj, s, ti):
        a += (self.H(b, c, d) & 0xffffffff) + Mj + ti
        a = ((a & 0xffffffff) << s) | ((a & 0xffffffff) >> (32 - s))
        a += b
        return a & 0xffffffff

    def II(self, a, b, c, d, Mj, s, ti):
        a += (self.I(b, c, d) & 0xffffffff) + Mj + ti
        a = ((a & 0xffffffff) << s) | ((a & 0xffffffff) >> (32 - s))
        a += b
        return a & 0xffffffff
