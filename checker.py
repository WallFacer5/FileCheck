from md5 import Md5Checker


class Checker:
    def __init__(self, msg, algo):
        msg = eval('0x' + bytes(msg.encode()).hex())
        self.byte_stream = msg
        print(bin(msg))
        print(hex(msg))
        print(msg.bit_length())
        if algo == 'md5':
            self.checker = Md5Checker(self.byte_stream)


if __name__ == '__main__':
    checker = Checker('jasdljf8afj98ajf98jsad9f8j9asdjf9s8djf8asjf98ajs8fjas98fja98jf9as8jf89jfs89jf89jfasjfjsa' +
                      'sdfasdfasdfsafkashfkhasfkjhjsahfjhfjkshafjahfjshfjahfjhasfjhasfjhasjkfhjkshfjkhfjhffhjdh' +
                      'sjfkjasfljaskldjfksajfksladjfksjfksjflksjflkjsklfjsakjfklsjfksaljfklsdjfkljaskfljakslfjf' +
                      'djsflksajfkljsdkfjskdfjksaljfakdjfklsjfklsdjfklsjfakljfklsajfksajfksajfklsajfklajfkjffff'
                      , 'md5')
