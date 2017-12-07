# Combined-Cryptography-
This is a library that has access implementations of a few different cryptography algorithms
This is a work in progress right now, If you are reading this, it isn't done yet.

# Actual explination
So this library contains two different modernly used cryptography methods. It uses ECDSA as a digital signature and it uses RSA for encryption. It also contains two methods for breaking RSA encryption (AKA-Factoring) Pollard's Rho and Lenstra's ECM. The full paper that goes allong with this code can be found here(LINK NOT AVAILABLE) and it goes into much more detail as to how these methods work.

It should be noted that the implementations used here do not nessessairly allign with how these methods are actually used. It is my own implementation and likely will varry from other implementations. Most notably in how block encoding works. What this means in practice is that if your friend sends you something secured with a different implementation of RSA it may not nessessairly give the correct output. However both using the same implementation should be fine.

# Different functions that come with this library
This library is divided into multiple different classes and those classes have methods within them.

# Pollard Class
Pollard.GCD(a,b)
  This method takes two numbers a and b, and returns the gratest common divisor (factor) of the two numbers.
Pollard.f(x,c,n)
  This method is used as a psudo random number generator for Pollard's Rho. n is the numberthat you want to factor, c is a constant that only really changes when something goes terribly wrong (althought that is quite rare from my testing)
Pollard.Factor(n)
  This method uses Pollard's Rho to factor whatever number you give it. Generally this is fast for numbers less than 20-30 digits long. Any longer and you are more likely to be sucessfull with Lenstra's ECM
# Lenstra
Lenstra.Factor(n)
  This method return a non-trivial factor of n using Lenstra'sECM method 
# ECDSA
WORK IN PROGRESS
# Floating functions
These are functions that don't belong to any class. I did this because they are part of doing elliptic curve algebra and both ECDSA and Lenstra's ECM both use elliptic curve algebra.
gcd and egcd(a,b)
  Both these methods return the gratest common divisor of a and b, egcd needs to recursively call itself with some extra parameters which is why it returns three arguments. This is slightly different in approach than Pollard.GCD and is mostly a product of not having enough care to change ether of them at this point.
modinv(a,m)
  returns the modular inverse of a with respect of m. Raises an exception if the mod inverse doesn't exist. If it does fail, it will put the GCD(a,m) into the "save_value" variable before throwing the exception, that way lenstra's ECM can pick it up. 
Point(x,y)
  returns an instance of point. Technically this is a class, but it is a class that only has those two public elements, x and y.
Curve(a,b,c)
  returns and instance of Curve. This represents an elliptic curve under modular inverse. The curve in question is y^2 = x^3 + ax + b mod c. Other than a,b, and c Curve also has a built in function Curve.oncurve(P) which returns true if the point is on the curve, and false if it isn't. This method is almost never actually used.
addpoints(P,Q,Curve)
  returns a point instance representing the addition of point P and Q on an elliptic curve Curve, or False if the elliptic curve algebra fails (as can, and will, happen when using lenstra's ECM)
multpoint(a,P,curve)
  returns a point instance representing the multiplication of point P by scaler integer a on elliptic curve curve, or false if the elliptic curve algebra fails (again, its part of lenstra's ECM)
get_order(P,curve)
  returns the order of point P on the curve, or false if P is not on the curve
