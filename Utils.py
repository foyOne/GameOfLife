import random
import string
import secrets


def GetRandomStringValue(length=64):
    letters = string.hexdigits
    return ''.join(secrets.choice(letters) for _ in range(length)).lower()


def GetRandomInterger(limit):
    return secrets.randbelow(limit)


def GetRandomPair(L1, L2):
    return (GetRandomInterger(L1), GetRandomInterger(L2))

def GetRandomPair(size):
    return (GetRandomInterger(size[0]), GetRandomInterger(size[1]))
