import random

def rabinMiller(n, d):
    a = random.randint(2, (n - 2) - 2)
    x = pow(a, int(d), n) # a^d%n
    if x == 1 or x == n - 1:
        return True

    # square x
    while d != n - 1:
        x = pow(x, 2, n)
        d *= 2

        if x == 1:
            return False
        elif x == n - 1:
            return True

    # is not prime
    return False

def isPrime(n):
    """
        return True if n prime
        fall back to rabinMiller if uncertain
    """

    # 0, 1, -ve numbers not prime
    if n < 2:
        return False

    # low prime numbers to save time
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    # if in lowPrimes
    if n in lowPrimes:
        return True

    # if low primes divide into n
    for prime in lowPrimes:
        if n % prime == 0:
            return False

    # find number c such that c * 2 ^ r = n - 1
    c = n - 1 # c even bc n not divisible by 2
    while c % 2 == 0:
        c /= 2 # make c odd

    # prove not prime 128 times
    for i in range(128):
        if not rabinMiller(n, c):
            return False

    return True

def generateKeys(keysize=1024):
    e = d = N = 0

    # get prime nums, p & q
    p = generateLargePrime(keysize)
    q = generateLargePrime(keysize)

    print("p: {}.".format(p))
    print("q: {}.".format(q))

    N = p * q # RSA Modulus
    phiN = (p - 1) * (q - 1) # totient

    # choose e
    # e is coprime with phiN & 1 < e <= phiN
    while True:
        e = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isCoPrime(e, phiN)):
            break

    # choose d
    # d is mod inv of e with respect to phiN, e * d (mod phiN) = 1
    d = modularInv(e, phiN)

    return e, d, N

def generateLargePrime(keysize):
    """
        return random large prime number of keysize bits in size
    """

    while True:
        num = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1)
        if (isPrime(num)):
            return num

def isCoPrime(p, q):
    """
        return True if gcd(p, q) is 1
        relatively prime
    """

    return gcd(p, q) == 1

def gcd(p, q):
    """
        euclidean algorithm to find gcd of p and q
    """

    while q:
        p, q = q, p % q
    return p

def egcd(a, b):
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    # return gcd, x, y
    return old_r, old_s, old_t

def modularInv(a, b):
    gcd, x, y = egcd(a, b)

    if x < 0:
        x += b

    return x

def encrypt(e, N, msg):
    cipher = pow(msg, e, N)
    return cipher

def decrypt(d, N, cipher):
    msg = pow(cipher, d, N)
    return msg

def signName(d,N, chunkedName):
    signedName = pow(chunkedName, d, N)
    return signedName


def verifySign(e, N, signedMessage):
    verifiedSign = pow(signedMessage, e, N)
    return verifiedSign

def chunks(lst, n):
    "Yield successive n-sized chunks from lst"
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def toHex(dec):
    digits = "0123456789ABCDEF"
    x = (dec%16)
    rest = dec // 16
    if (rest == 0):
        return digits[x]
    return toHex(rest) + digits[x]


def main():
    print("HAPPYYY CODING SALVIN!")

    keysize = 16

    e, d, N = generateKeys(keysize)

    msg = "Hello From Salvin"
    print("Msg: {}".format(msg))
    print("Msg type: {}".format(type(msg)))

    chunkArray = list(chunks(msg,3))
    print("chunkArray: {}".format(chunkArray))

    hexArray = [i.encode("utf-8").hex() for i in chunkArray]
    print("hexArray: {}".format(hexArray))

    intArray = [int(i, 16) for i in hexArray]
    print("intArray: {}".format(intArray))


    encIntArray = []
    for i in range(len(intArray)):
        # print("dataI: {}.".format(intArray[i]))
        dataE = encrypt(2033, 1709148229, intArray[i])
        # print("dataE: {}.".format(dataE))
        encIntArray.append(dataE)

    print("encIntArray: {}".format(encIntArray))

    givenIntArray = [1440695500,164493413,1333355651,1593297656]
    # print("givenIntArray: {}".format(givenIntArray))

    decIntArray = []

    for i in range(len(givenIntArray)):
        # print("dataI: {}.".format(encIntArray[i]))
        dateD = decrypt(1303866437, 1709148229, givenIntArray[i])
        # print("dateD: {}.".format(dateD))
        decIntArray.append(dateD)

    print("decIntArray: {}".format(decIntArray))

    decHexArray = [hex(i) for i in decIntArray]
    print("decHexArray: {}".format(decHexArray))

    # decStringArray = [bytes.fromhex(i[2:]).decode('utf-8') for i in decHexArray]
    decStringArray = [bytes.fromhex(i[2:]).decode('utf-8') for i in decHexArray]

    print("decStringArray: {}".format(decStringArray))

    decodedMessage = ''.join([str(item) for item in decStringArray])
    print("decodedMessage: {}".format(decodedMessage))

    print("Signing Process\n\n")

    ################################
    signature = "Mirza Aliva Salvin"
    print("Signature: {}".format(signature))

    chunkSignArray = list(chunks(signature,3))
    print("chunkSignArray: {}".format(chunkSignArray))

    hexSignArray = [i.encode("utf-8").hex() for i in chunkSignArray]
    print("hexArray: {}".format(hexSignArray))

    intSignArray = [int(i, 16) for i in hexSignArray]
    print("intArray: {}".format(intSignArray))

    encSignArray = []
    for i in range(len(intSignArray)):
        # print("dataI: {}.".format(intArray[i]))
        dataE = signName(1303866437, 1709148229, intSignArray[i])
        # print("dataE: {}.".format(dataE))
        encSignArray.append(dataE)

    print("encSignArray: {}".format(encSignArray))

    # givenIntArray = [1440695500,164493413,1333355651,1593297656]
    givenIntSignArray = [59690197,1847713031,1122144269,905387114,643905088,134811023]
    # print("givenIntArray: {}".format(givenIntArray))

    decSignIntArray = []


    for i in range(len(encSignArray)):
        # print("dataI: {}.".format(encIntArray[i]))
        dateD = verifySign(2033, 1709148229, encSignArray[i])
        # print("dateD: {}.".format(dateD))
        decSignIntArray.append(dateD)

    print("decSignIntArray: {}".format(decSignIntArray))

    decSignHexArray = [hex(i) for i in decSignIntArray]
    print("decSignHexArray: {}".format(decHexArray))

    # decStringArray = [bytes.fromhex(i[2:]).decode('utf-8') for i in decHexArray]
    decSignStringArray = [bytes.fromhex(i[2:]).decode('utf-8') for i in decSignHexArray]

    print("decSignStringArray: {}".format(decSignStringArray))

    verifiedSignature = ''.join([str(item) for item in decSignStringArray])
    print("verifiedSignature: {}".format(verifiedSignature))

 ###################################

    print("e: {}.".format(e))
    print("d: {}.".format(d))
    print("N: {}.".format(N))



main()

"""
    My , N = 1709148229, e = 2033, d = 1303866437
    Partner , N = 2730288283, e = 847792097,
    Enc message = [1345927603 , 603648529 ,763142900 ,1122464479]
"""
