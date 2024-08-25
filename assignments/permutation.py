# -*- coding: utf-8 -*-
# Based on an implementation by Gilles Van Assche.

import numpy as np
#Constants
bsize = 400
laneSize = bsize // 25
widthBytes = laneSize // 8

RC = [
    0x0001,
    0x808B,
    0x8082,
    0x008B,
    0x808A,
    0x8089,
    0x8000,
    0x8003,
    0x808B,
    0x8002,
    0x0001,
    0x0080,
    0x8081,
    0x800A,
    0x8009,
    0x000A,
    0x008A,
    0x8081,
    0x0088,
    0x8080,
    0x8009,
    0x0001,
    0x000A,
    0x8008,
]


# Define the keccak-f round function
def keccak_round(A, RC):
    # Define the theta step
    C = [0] * 5
    D = [0] * 5
    for x in range(5):
        C[x] = A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4]
    for x in range(5):
        D[x] = C[(x - 1) % 5] ^ rotate_left(C[(x + 1) % 5], 1)
    for x in range(5):
        for y in range(5):
            A[x][y] ^= D[x]

    # Define the rho and pi steps
    B = [[0] * 5 for i in range(5)]
    for x in range(5):
        for y in range(5):
            B[y][(2 * x + 3 * y) % 5] = rotate_left(A[x][y], (x + 3 * y) % 8)

    # Define the chi step
    for x in range(5):
        for y in range(5):
            A[x][y] = B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y])

    # Define the iota step
    A[0][0] ^= RC

    return A


# Define the rotate_left function
def rotate_left(x, n):
    return ((x << n) & 0xFFFF) | (x >> (16 - n))


def KeccakFonLanes(A):
    for i in range(18):
        A = keccak_round(A, RC[i])
    return A


# For b=400
def load16(a):
    return sum((a[i] << (8 * i)) for i in range(2))


# For b=400
def store16(a):
    return list((a >> (8 * i)) % 256 for i in range(2))


def KeccakF(state, b=bsize):
    #We have 5x5 lanes, so each lane is 400bits//25=16bits=2bytes
    lanes = [[
        load16(state[2 * (x + 5 * y):2 * (x + 5 * y) + 2]) for y in range(5)
    ] for x in range(5)]
    lanes = KeccakFonLanes(lanes)
    state = bytearray(50)
    for x in range(5):
        for y in range(5):
            state[2 * (x + 5 * y):2 * (x + 5 * y) + 2] = store16(lanes[x][y])
    return state


#General round constants.
#RC=[ 0x0000000000000001,	0x000000008000808B, 0x0000000000008082,	0x800000000000008B, 0x800000000000808A,	0x8000000000008089, 0x8000000080008000,	0x8000000000008003, 0x000000000000808B,	0x8000000000008002, 0x0000000080000001,	0x8000000000000080, 0x8000000080008081,	0x000000000000800A, 0x8000000000008009,	0x800000008000000A, 0x000000000000008A,	0x8000000080008081, 0x0000000000000088,	0x8000000000008080, 0x0000000080008009,	0x0000000080000001, 0x000000008000000A,	0x8000000080008008, ]
