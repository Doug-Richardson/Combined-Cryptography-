import math as math
import time as time
import random as rand
import hashlib as hashlib


class Pollard:
    def GCD(a, b):
        if (a < b):
            c = a
            a = b
            b = c
        if (a%b == 0):
            return b
        else:
            return (Pollard.GCD(b, a%b))

    def f(x, c, n):
        return ((x*x)+c)%n
    def Factor(n):
        tries = math.ceil(5*math.sqrt(math.sqrt(n)))
        #5sqrt(min(p,q)) gives 99.99% sucess, 
        #we don't know p or q but we know max for them is squr(n)
        x = 2
        y = 2
        c = 1
        i = 0
        for i in range(1, tries):
            x = Pollard.f(x,c,n)
            y = Pollard.f(Pollard.f(y,c,n),c,n)
            result = abs(y - x)
            test = Pollard.GCD(n, result)
            if (test == 0):
                print("Try a different C, we got 0")
                return 0
            elif (test != 1):
                return test
        print("Well that is awkward... Is the number prime?")
        return -1

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def gcd(a,b):
    output,one,two = egcd(a,b)
    return output

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        global save_value
        save_value = g
        raise Exception('modular inverse does not exist')
    else:
        return x % m

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
class Curve:
    def __init__(self,a,b,c):
        self.a = a
        self.b = b
        self.c = c
    def oncurve(self,P):
        if ((P.y*P.y)%self.c == (self.a * P.x + self.b + P.x*P.x*P.x)%self.c):
            return True
        else:
            return False

def addpoints(P, Q, curve):
    if (P == False and Q != False):
        return Q
    if (P != False and Q == False):
        return P
    try:
        return _addpoints(P, Q, curve, curve.c)
    except Exception:
        return False
def _addpoints(P,Q,curve,n):
    if (P.x == Q.x and P.y == Q.y):
        return _multpoint(2,P,curve,n)
    output = Point(0,0)
    Lamb = (((P.y-Q.y)%n)*modinv(((P.x - Q.x)%n),n))%n
    output.x = (((Lamb*Lamb)%n) - P.x - Q.x)%n
    output.y = (Lamb*(P.x - output.x) - P.y)%n
    return output
def multpoint(a, P, curve):
    try:
        return _multpoint(a, P, curve, curve.c)
    except Exception:
        return False
def _multpoint(a, P, curve, n):
    if (a == 0):
        return Point(0, 0)
    if ((a != 2) and (a != 1)):
        if (a%2 == 0):
            return _multpoint(2,_multpoint(a//2,P,curve,n),curve,n)
        else:
            return _addpoints(_multpoint(a-1,P,curve,n),P,curve,n)
    elif (a == 1):
        return P
    else:#a == 2
        output = Point(0,0)
        Lamb = ((3*P.x*P.x+curve.a)*modinv((2*P.y)%n,n))%n
        output.x = (((Lamb*Lamb)%n) - 2*P.x)%n
        output.y = (Lamb*(P.x - output.x) - P.y)%n
        return output
def get_order(P, curve):
    if (curve.oncurve(P)):
        i = 0
        temp = P
        while(temp != False):
            temp = addpoints(temp, P, curve)
            i = i + 1
        return i
    else:
        return False

class Lenstra:
    def Factor(n):
        for q in range(0,100000):
            a = rand.randint(0,n-1)
            x = rand.randint(0,n-1)
            y = rand.randint(0,n-1)
            b = (y*y - x*x*x - (a*x))%n
            E = Point(x,y)
            Temp = E
            C = Curve(a,b,n)
            k = 2
            while (k < 1500):
                Temp = multpoint(k,Temp, C)
                if (Temp == False):
                    global save_value
                    output = save_value
                    save_value = -1
                    if (output == n):
                        break
                    else:
                        return output
                    if (not C.oncurve(E)):
                        print("Shit")
                        return gcd(E.x,n)
                k = k + 1
        return -1
class ECDSA:
    def sign(C,G,n,i,Q,m,d):
        hashslingingslasher = hashlib.sha256()
        hashslingingslasher.update(m.encode('utf-8'))
        e = hashslingingslasher.digest()
        temp = 1
        prez = [e[0]]
        while (temp < i):
            prez.append(e[0])
            temp = temp + 1
        z = int.from_bytes(prez, byteorder = 'big')
        r = 0
        s = 0
        while (r == 0 and s == 0):
            k = rand.randint(1, n-1)
            p = multpoint(k, G, C)
            r = p.x%n
            try:
                s = (modinv(k, n) * (z + r*d))%n
            except Exception:
                s = 0
        return Point(r,s)

    def verify(C,G,n,i,Q,m,r,s):
        hashslingingslasher = hashlib.sha256()
        hashslingingslasher.update(m.encode('utf-8'))
        e = hashslingingslasher.digest()
        temp = 1
        prez = [e[0]]
        while (temp < i):
            prez.append(e[0])
            temp = temp + 1
        z = int.from_bytes(prez, byteorder = 'big')
        w = modinv(s,n)
        u = (z*w)%n
        v = (r*w)%n
        a = multpoint(u,G,C)
        b = multpoint(v,Q,C)
        x = addpoints(a,b,C).x
        if (r%n == x%n):
            return True
        else:
            return False
class RSA:
    def block_encode(m):
        l = len(m)
        i = 0
        output = list()
        while(i < l):
            k = ord(m[i])
            if (i + 1 < l):
                k = k * 10000 + ord(m[i+1])
            else:
                k = k * 10000
            i = i + 2
            output.append(k)
        return output
    def block_decode(m):
        l = len(m)
        i = 0
        output = ""
        while(i < l):
            k = m[i]//10000
            if (k != 0):
                output = output + chr(k)
            k = m[i]%10000
            if (k != 0):
                output = output + chr(k)
            i = i + 1
        return output
    def MakeEncrypt(p,q):
        x = q*rand.randint(7,50)+rand.randint(1,1000)#some number about the size of q
        k = 0#k is a flag, it is 1 when we found a number that is relativly prime to the encryption key AND the decryption key
        while (k == 0):
            x = x-1
            if ((gcd(x, p*q) == 1) and (gcd(x,(p-1)*(q-1)) == 1)):
                k = 1
            if x == 10:
                print("Shit Something Broke... Ignore anything after this line")#If x is 10 then the prime number is too low 
                break#OR we couldn't find something relitavely prime. This almost never happens as relitavely prime numbers are a dime a dozen
        d = modinv(x,(p-1)*(q-1))
        return x,d#returns a number relitavely prime to p*q and (p-1)*(q-1) AKA encryption key
    def big_pow(x,y,n):
        if (x == 1):
            return 1
        if (x == 0):
            return 0
        if (y == 0):
            return 1
        if (y == 1):
            return x
        if (y == 2):
            return x*x
        if (y % 2 == 1):
            return (x*RSA.big_pow(RSA.big_pow(x,y//2,n),2,n) % n)
        else:
            return (RSA.big_pow(RSA.big_pow(x,y//2,n),2,n) % n)
    def encrypt(m,n,e):
        encoded = RSA.block_encode(m)
        output = list()
        k = 0
        while k < len(encoded):
            output.append(RSA.big_pow(encoded[k],e,n))
            k = k + 1
        return output
    def decrypt(m,n,d):
        output = list()
        k = 0
        while k < len(m):
            output.append(RSA.big_pow(m[k],d,n))
            k = k + 1
        return RSA.block_decode(output)
class brute_force:
    def factor(n):
        i = 2
        while (n%i != 0):
            i = i + 1
        return i
