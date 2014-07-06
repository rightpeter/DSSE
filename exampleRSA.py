#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Rightpeter'
import rsa

(pubkey, privkey) = rsa.newkeys(1024)

pub = pubkey.save_pkcs1()
pubfile = open('public.pem', 'w+')
pubfile.write(pub)
pubfile.close()

pri = privkey.save_pkcs1()
prifile = open('private.pem', 'w+')
prifile.write(pri)
prifile.close()

with open('A.txt') as inputfile:
    content = inputfile.read()

with open('public.pem') as publickfile:
    p = publickfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)

with open('private.pem') as privatefile:
    p = privatefile.read()
    privkey= rsa.PrivateKey.load_pkcs1(p)

crypto = rsa.encrypt(content, pubkey)
message = rsa.decrypt(crypto, privkey)
print 'crypto: ', crypto
print 'content: ', content 

with open('A_enc.txt', 'w+') as outputfile:
    outputfile.write(crypto)
    outputfile.close()
    
signature = rsa.sign(content, privkey, 'SHA-1')
print 'verify: ', rsa.verify(content, signature, pubkey)
