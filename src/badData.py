import random, string

def randString():
    return ''.join(random.choice(string.ascii_letters) for x in range(random.randint(0, 1024)))

badStrings = [
'Nan', 'NaN', 'Inf',
'e' * 1024, 'E' * 1024,
'e' * random.randint(2^5, 2^15),
'E' * random.randint(2^5, 2^15),
'E' * random.randint(2^5, 2^15),
'%s' * random.randint(2^5, 2^15),
'%n' * random.randint(2^5, 2^15),
randString(), randString() ]

badNums = [
-1, 0, 1,
0xFE, 0xFF, 0x100, 0x101,
0xFFFE, 0xFFFF, 0x1000, 0x1001,
0xFFFFFFFE, 0xFFFFFFFF, 0x10000000, 0x10000001,
0.000000000001, 1000000000000.0000, -10e-10 ]

