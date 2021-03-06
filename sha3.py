# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 01:23:55 2019

@author: Weizhi Wang
"""

# import argparse  # Use with CLI method of input
import sys  # Use with debugging/writing input
from os import path
import bitstring
from copy import deepcopy

from attrdict import AttrDict

constant = AttrDict({
    'BLOCK_WIDTH': 1600,
    'BIT_RATE': 1088,
    'WORD_SIZE': 64,
    'WORD_POWER': 6,
    'CAPACITY': 512
})


class Sha3Checker:
    """docstring for Sha3Checker"""

    def __init__(self, input_msg, is_file):
        super(Sha3Checker, self).__init__()
        self.hash_value = None

        # Consider using mmap here
        if is_file:
            self.input_string = bitstring.BitArray(open(input_msg, "rb").read())
        else:
            self.input_string = bitstring.BitArray(bin(int(
                ''.join(format(ord(x), 'b') for x in input_msg), base=2
            )))

    def do_hash(self):
        print('do hash of', self.input_string)
        pad_input(self.input_string)
        padded_input = self.input_string
        padded_input_list = []

        for x in range(int(padded_input.len / constant.BIT_RATE)):
            padded_input_list.append(bitstring.BitArray(
                padded_input[x * constant.BIT_RATE:(x + 1) * constant.BIT_RATE]
            ))

        state = bitstring.BitArray('0b0')
        for _ in range(constant.BLOCK_WIDTH - 1):
            state.prepend('0b0')
        for p_i in padded_input_list:
            for _ in range(constant.CAPACITY):
                p_i.append("0b0")
            state ^= p_i
            state = block_permutation(state)

        input_hash = bitstring.BitArray()
        while input_hash.len < 64:
            input_hash.append(state[0:constant.BIT_RATE])
            state = block_permutation(state)
        return input_hash.hex[:64]

    def get_hash(self):
        if self.hash_value is None:
            self.hash_value = self.do_hash()
            return self.hash_value
        else:
            return self.hash_value


def pad_input(string_to_pad):
    string_to_pad.prepend('0b1')
    while string_to_pad.len % constant.BIT_RATE != (constant.BIT_RATE - 1):
        string_to_pad.prepend('0b0')
    string_to_pad.prepend('0b1')


def block_permutation(state):
    state_prime = deepcopy(state)
    state_array = [[[int(0) for _ in range(constant.WORD_SIZE)] for _ in range(5)] for _ in range(5)]

    for x in range(5):
        for y in range(5):
            for z in range(constant.WORD_SIZE):
                state_array[x][y][z] = state[constant.WORD_SIZE * (5 * y + x) + z]

    for i in range(12 + 2 * constant.WORD_POWER):
        state_array = theta(state_array)
        state_array = rho(state_array)
        state_array = pi(state_array)
        state_array = chi(state_array)
        state_array = iota(state_array, i)

    for i in range(5):
        for j in range(5):
            for k in range(constant.WORD_SIZE):
                state_prime[constant.WORD_SIZE * (5 * j + i) + k] = state_array[i][j][k]

    return state_prime


def theta(state_array):
    C = [[bitstring.Bits() for _ in range(constant.WORD_SIZE)] for _ in range(5)]
    for x in range(5):
        for z in range(constant.WORD_SIZE):
            C[x][z] = (state_array[x][0][z] ^ state_array[x][1][z] ^
                       state_array[x][2][z] ^ state_array[x][3][z] ^
                       state_array[x][4][z])
    D = [[bitstring.Bits() for _ in range(constant.WORD_SIZE)] for _ in range(5)]
    for x in range(5):
        for z in range(constant.WORD_SIZE):
            D[x][z] = C[(x - 1) % 5][z] ^ C[(x + 1) % 5][(z - 1) % constant.WORD_SIZE]

    state_array_prime = deepcopy(state_array)
    for x in range(5):
        for y in range(5):
            for z in range(constant.WORD_SIZE):
                state_array_prime[x][y][z] = state_array[x][y][z] ^ D[x][z]
    return state_array_prime


def rho(state_array):
    state_array_prime = deepcopy(state_array)
    for z in range(constant.WORD_SIZE):
        state_array_prime[0][0][z] = state_array[0][0][z]
    x, y = 1, 0
    for t in range(24):
        for z in range(constant.WORD_SIZE):
            state_array_prime[x][y][z] = state_array[x][y][z - int((t + 1) * (t + 2) / 2) % constant.WORD_SIZE]
            x, y = y, (2 * x + 3 * y) % 5
    return state_array_prime


def pi(state_array):
    state_array_prime = deepcopy(state_array)
    for x in range(5):
        for y in range(5):
            for z in range(constant.WORD_SIZE):
                state_array_prime[x][y][z] = state_array[(x + 3 * y) % 5][x][z]
    return state_array_prime


def chi(state_array):
    state_array_prime = deepcopy(state_array)
    for x in range(5):
        for y in range(5):
            for z in range(constant.WORD_SIZE):
                state_array_prime[x][y][z] = (state_array[x][y][z] ^
                                              ((state_array[(x + 1) % 5][y][z] ^ 1) *
                                               state_array[(x + 2) % 5][y][z]))
    return state_array_prime


def iota(state_array, round_index):
    state_array_prime = deepcopy(state_array)
    RC = [0 for _ in range(constant.WORD_SIZE)]
    for j in range(constant.WORD_POWER):
        RC[pow(2, j) - 1] = round_constant_generation(j + 7 * round_index)
    for z in range(constant.WORD_SIZE):
        state_array_prime[0][0][z] = state_array[0][0][z] ^ RC[z]
    return state_array_prime


def round_constant_generation(t):
    if t % 255 == 0:
        return 1
    R = [1, 0, 0, 0, 0, 0, 0, 0]
    for i in range(1, t % 255):
        R.insert(0, 0)
        R[0] = R[0] ^ R[8]
        R[4] = R[4] ^ R[8]
        R[5] = R[5] ^ R[8]
        R[6] = R[6] ^ R[8]
        del (R[8:])
    return R[0]
