#This is example code on using the Combined Cryptogrophy library
#I used this in the example for my presentation
#Created by Douglas Richardson
#Code starts here
import Cryptogrophy_Combined_Richardson as DR
import time as time
p = 6746328388801
q = 9999991111111 #Two somewhat large primes (Not cryptographically safe, but will be used for an example)
print("First we will have a message to encrypt")
garbage = input("Press Enter to continue")
m = "Once upon a midnight dreary, while I pondered, weak and weary,\n" +"Over many a quaint and curious volume of forgotten lore—\n"+"While I nodded, nearly napping, suddenly there came a tapping,\n"+"As of some one gently rapping, rapping at my chamber door.\n"+"’Tis some visitor, I muttered, tapping at my chamber door—\n"+"Only this and nothing more.\n"
print(m)
garbage = input("Press Enter to continue")
print("Next We make an encryption key with RSA")
print("To do this, we run the RSA.MakeEncrypt function on two prime numbers")
print("Let p = ",p)
print("Let q = ",q)
rsae , rsad = DR.RSA.MakeEncrypt(p,q)
print("So that gives us e = ", rsae, " and d = ", rsad)
print("To use sign with ECDSA We need to pick a curve, like y^2 = x^3 + 0x + 7 with modbase 101 as a small example")
print("A point on this curve is (63,68) so we can use that as our generator")
print("Side note, this is the same curve that Bitcoin uses, just a different modular base")
print("The order of this point is 17, a prime number")
print("We then choose a public key in the range(1,17-1), We will use d = 14 as our private key")
ecC = DR.Curve(0, 7, 101)#Curve
ecG = DR.Point(63,68)#Generator
ecn = 17
ecd = 14#Private and keep it that way
ecQ = DR.multpoint(ecd, ecG, ecC)
print("Now lets get the signature using ECSDA.sign function")
output = DR.ECDSA.sign(ecC,ecG,ecn,32,ecQ,m,ecd)
print("This gives us our signature as r = ", output.x, "and s = ", output.y)
print("Now we will use RSA.encrypt function to encrypt the message")
Encrypted = DR.RSA.encrypt(m,p*q,rsae)
print("Here is part of the encrypted message:")
print(Encrypted[0],Encrypted[1],Encrypted[2],"...")
print("The full message is", len(Encrypted),"more numbers so we won't show all of those.")
print("Now lets decrypt it using RSA.decrypt")
garbage = input("Press Enter to continue")
Decrypted = DR.RSA.decrypt(Encrypted,p*q,rsad)
print("Here is our final result:")
print(Decrypted)
print("Now let us verify the message is from the origional sender using ECDSA.verify")
garbage = input("Press Enter to continue")
if(DR.ECDSA.verify(ecC,ecG,ecn,32,ecQ,Decrypted,output.x,output.y)):
    print("That function returned true so it worked, we have verified this singature!")
else:
    print("If you are reading this something went terribly wrong since verify returned false")
garbage = input("Press Enter to continue")
print("Now we are going to try and break the encryption")
print("We know the public key is ", p*q, " so lets factor that with Pollard's ECM")
t = time.time()
print("So we got: ",DR.Pollard.Factor(p*q))
print("That took:", time.time() - t, "seconds")
print("Now we will attempt to use Lenstra's ECM")
t = time.time()
print("So we got: ",DR.Lenstra.Factor(p*q))
print("That took:", time.time() - t, "seconds")
#End of example code