from md5 import Md5Checker


class Checker:
    def __init__(self, msg, algo):
        if msg == '':
            msg = 0
        else:
            msg = eval('0x' + bytes(msg.encode()).hex())
        self.byte_stream = msg
        print('Msg:')
        print(bin(msg))
        print(hex(msg))
        print()
        if algo == 'md5':
            self.checker = Md5Checker(self.byte_stream)

    def get_hash(self):
        return self.checker.get_hash()


if __name__ == '__main__':
    msg = input('Please input the msg: ')
    hash_func = input('Please input the hash function you want to use(md5, sha3): ')
    checker = Checker(msg, hash_func)
    print(hash_func, 'hash of', msg, 'is', checker.get_hash())
