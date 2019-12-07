import math


class Md5Checker:
    def __init__(self, byte_stream):
        self.byte_stream = byte_stream
        self.A = 0x67452301
        self.B = 0xefcdab89
        self.C = 0x98badcfe
        self.D = 0x10325476
        self.md5_result = None
        self.s = [
            7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
            5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
            4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
            6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
        ]
        self.K = []
        for i in range(64):
            self.K.append(math.floor(2 ** 32 * abs(math.sin(i + 1))))
        self.padding()
        print('Bytes after padding:')
        print(bin(self.byte_stream))
        print(hex(self.byte_stream))
        print()
        self.chunk_num = (len(bin(self.byte_stream)[2:]) + 511) // 512
        self.chunks = []
        dup_bytes = self.byte_stream
        for i in range(self.chunk_num):
            self.chunks.append(dup_bytes % (2 ** 512))
            dup_bytes = dup_bytes >> 512
        self.chunks.reverse()
        print('\n'.join(['Chunks:'] + list(map(lambda chunk: bin(chunk)[2:], self.chunks))))
        print()

    def padding(self):
        if self.byte_stream == 0:
            self.byte_stream = 0b1<<511
            return
        origin_length = (len(bin(self.byte_stream)[2:]) + 7) // 8 * 8
        self.byte_stream = self.byte_stream << 8
        self.byte_stream += 0x80
        cur_length = origin_length + 8
        padding_length = 512 - 64 - cur_length % 512
        if padding_length < 0:
            padding_length += 512
        self.byte_stream = self.byte_stream << padding_length
        self.byte_stream = (self.byte_stream << 64) + origin_length % (2 ** 64)

    def F(self, X, Y, Z):
        return (((X & Y) | ((0xffffffff - (X & 0xffffffff)) & Z)) & 0xffffffff)

    def G(self, X, Y, Z):
        return (((X & Z) | (Y & (0xffffffff - (Z & 0xffffffff)))) & 0xffffffff)

    def H(self, X, Y, Z):
        return ((X ^ Y ^ Z) & 0xffffffff)

    def I(self, X, Y, Z):
        return ((Y ^ (X | (0xffffffff - (Z & 0xffffffff)))) & 0xffffffff)

    def FF(self, a, b, c, d, Mj, s, ti):
        # print('FF:')
        # print(hex(a), hex(b), hex(c), hex(d), hex(Mj), s, hex(ti))
        a += (self.F(b, c, d) & 0xffffffff) + Mj + ti
        a = ((a & 0xffffffff) << s) | ((a & 0xffffffff) >> (32 - s))
        a += b
        # print(hex(a), hex(b), hex(c), hex(d))
        # print(a, b, c, d)
        # print()
        return a & 0xffffffff

    def GG(self, a, b, c, d, Mj, s, ti):
        # print('GG:')
        # print(hex(a), hex(b), hex(c), hex(d), hex(Mj), s, hex(ti))
        a += (self.G(b, c, d) & 0xffffffff) + Mj + ti
        a = ((a & 0xffffffff) << s) | ((a & 0xffffffff) >> (32 - s))
        a += b
        # print(hex(a), hex(b), hex(c), hex(d))
        # print()
        return a & 0xffffffff

    def HH(self, a, b, c, d, Mj, s, ti):
        # print('HH:')
        # print(hex(a), hex(b), hex(c), hex(d), hex(Mj), s, hex(ti))
        a += (self.H(b, c, d) & 0xffffffff) + Mj + ti
        a = ((a & 0xffffffff) << s) | ((a & 0xffffffff) >> (32 - s))
        a += b
        # print(hex(a), hex(b), hex(c), hex(d))
        # print()
        return a & 0xffffffff

    def II(self, a, b, c, d, Mj, s, ti):
        # print('II:')
        # print(hex(a), hex(b), hex(c), hex(d), hex(Mj), s, hex(ti))
        a += (self.I(b, c, d) & 0xffffffff) + Mj + ti
        a = ((a & 0xffffffff) << s) | ((a & 0xffffffff) >> (32 - s))
        a += b
        # print(hex(a), hex(b), hex(c), hex(d))
        # print()
        return a & 0xffffffff

    def reverse4bytes(self, four_bytes):
        four_bytes = hex(four_bytes)[2:]
        four_bytes = '0' * (8 - len(four_bytes)) + four_bytes
        four_bytes = [four_bytes[:2], four_bytes[2:4], four_bytes[4:6], four_bytes[6:]]
        four_bytes.reverse()
        return eval('0x' + ''.join(four_bytes))

    def single_chunk_process(self, chunk, is_last):
        words = []
        for i in range(16):
            words.append(self.reverse4bytes(chunk & 0xffffffff))
            chunk = chunk >> 32
        words.reverse()
        if is_last:
            tmp = words[-1]
            words[-1] = words[-2]
            words[-2] = tmp
            words[-1] = self.reverse4bytes(words[-1])
            words[-2] = self.reverse4bytes(words[-2])
        # print('\n'.join(['words'] + list(map(lambda word: bin(word)[2:], words))))
        a, b, c, d = self.A, self.B, self.C, self.D
        # print('abcd:', hex(a), hex(b), hex(c), hex(d))
        for i in range(4):
            a = self.FF(a, b, c, d, words[4 * i + 0], self.s[4 * i + 0], self.K[4 * i + 0])
            d = self.FF(d, a, b, c, words[4 * i + 1], self.s[4 * i + 1], self.K[4 * i + 1])
            c = self.FF(c, d, a, b, words[4 * i + 2], self.s[4 * i + 2], self.K[4 * i + 2])
            b = self.FF(b, c, d, a, words[4 * i + 3], self.s[4 * i + 3], self.K[4 * i + 3])
        # print(hex(a), hex(b), hex(c), hex(d))
        words_id = 1
        for i in range(4):
            a = self.GG(a, b, c, d, words[words_id], self.s[4 * i + 16], self.K[4 * i + 16])
            words_id += 5
            words_id %= 16
            d = self.GG(d, a, b, c, words[words_id], self.s[4 * i + 17], self.K[4 * i + 17])
            words_id += 5
            words_id %= 16
            c = self.GG(c, d, a, b, words[words_id], self.s[4 * i + 18], self.K[4 * i + 18])
            words_id += 5
            words_id %= 16
            b = self.GG(b, c, d, a, words[words_id], self.s[4 * i + 19], self.K[4 * i + 19])
            words_id += 5
            words_id %= 16
        words_id = 5
        for i in range(4):
            a = self.HH(a, b, c, d, words[words_id], self.s[4 * i + 32], self.K[4 * i + 32])
            words_id += 3
            words_id %= 16
            d = self.HH(d, a, b, c, words[words_id], self.s[4 * i + 33], self.K[4 * i + 33])
            words_id += 3
            words_id %= 16
            c = self.HH(c, d, a, b, words[words_id], self.s[4 * i + 34], self.K[4 * i + 34])
            words_id += 3
            words_id %= 16
            b = self.HH(b, c, d, a, words[words_id], self.s[4 * i + 35], self.K[4 * i + 35])
            words_id += 3
            words_id %= 16
        words_id = 0
        for i in range(4):
            a = self.II(a, b, c, d, words[words_id], self.s[4 * i + 48], self.K[4 * i + 48])
            words_id += 7
            words_id %= 16
            d = self.II(d, a, b, c, words[words_id], self.s[4 * i + 49], self.K[4 * i + 49])
            words_id += 7
            words_id %= 16
            c = self.II(c, d, a, b, words[words_id], self.s[4 * i + 50], self.K[4 * i + 50])
            words_id += 7
            words_id %= 16
            b = self.II(b, c, d, a, words[words_id], self.s[4 * i + 51], self.K[4 * i + 51])
            words_id += 7
            words_id %= 16

        # print('abcd:', hex(a), hex(b), hex(c), hex(d))
        # print('abcd:', bin(a), bin(b), bin(c), bin(d))
        # print('ABCD:', hex(self.A), hex(self.B), hex(self.C), hex(self.D))
        # print('ABCD:', bin(self.A), bin(self.B), bin(self.C), bin(self.D))
        self.A += a
        self.B += b
        self.C += c
        self.D += d
        self.A &= 0xffffffff
        self.B &= 0xffffffff
        self.C &= 0xffffffff
        self.D &= 0xffffffff
        print('abcd:', hex(self.A), hex(self.B), hex(self.C), hex(self.D))

    def hashing(self):
        for chunk in self.chunks[:-1]:
            self.single_chunk_process(chunk, False)
        self.single_chunk_process(self.chunks[-1], True)
        self.A = hex(self.reverse4bytes(self.A))[2:]
        self.B = hex(self.reverse4bytes(self.B))[2:]
        self.C = hex(self.reverse4bytes(self.C))[2:]
        self.D = hex(self.reverse4bytes(self.D))[2:]
        self.A = '0' * (8 - len(self.A)) + self.A
        self.B = '0' * (8 - len(self.B)) + self.B
        self.C = '0' * (8 - len(self.C)) + self.C
        self.D = '0' * (8 - len(self.D)) + self.D
        self.md5_result = self.A + self.B + self.C + self.D

    def get_hash(self):
        if self.md5_result is None:
            self.hashing()
        return self.md5_result


if __name__ == '__main__':
    md5_obj = Md5Checker(0)
    print(md5_obj.get_hash())
