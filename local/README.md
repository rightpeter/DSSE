Dynamic Searchable Symmetric Encryption
============================================================
This a simple implementation of DSSE designed by 

    Seny Kamara - Microsoft Research
    Charalampos Papamanthou - UC Berkeley
    Tom Roeder - Microsoft Research

in Dynamic Searchable Symmetric Encryption.


Author
-----------------------------------------------------------
Implemented by rightpeter. You can fork this project at 
    
    https://github.com/rightptere/DSSE

or contact me by E-mail:

    rightpeter.lu@gmail.com


Usage
-----------------------------------------------------------
DSSE Client includes 8 main python scriptions. 
You can put your own files in db/(your id)/.

### DSSE_gen.py
    This script generate public and private key of RSA.

### DSSE_enc.py
    Example: python DSSE_enc.py haha
    This script encrypts files in db/haha/*.

### DSSE_index.py
    Example: python DSSE_index.py haha
    This script creates the index of files db/haha/*.

### DSSE_addtoken.py
    Example: python DSSE_addtoken.py haha 5
    This script creates add token of file db/haha/5. 

### DSSE_srchtoken.py
    Example: python DSSE_srchtoken.py haha even
    This script creates search token of word for haha.

### DSSE_deltoken.py
    Example: python DSSE_deltoken.py haha 5
    This script creates del token of file 5 in haha.

### DSSE_zip.py
    Example: python DSSE_zip.py haha
    This script creates a zip file for db/haha/*.
    The zip file will be uploaded to server later.

### DSSE_dec.py
    Example: python DSSE_dec.py haha even
    This script deciphers the search result of word even and 
    puts result in folder db/haha/even
