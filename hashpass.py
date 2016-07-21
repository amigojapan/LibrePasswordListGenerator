#note, I suck at math, so I am not very confident in this part, and I think it can suerly be made much more optimized
import hashlib
import array
import string
def hash_my_password(passwod,salt,symbols,spaces):
	dk = hashlib.pbkdf2_hmac('sha256', passwod, salt, 100000)
	
	def testBit(int_type, offset):
	     mask = 1 << offset
	     return(int(bool(int_type & mask)))
	
	def setBit(int_type, offset):
	     mask = 1 << offset
	     return(int_type | mask)
		
	#convert the data to a string 
	barray=array.array('B', dk)
	increment=0
	stringout=""
	for byte in barray:
	    increment=increment+1
	    for c in range(0,8):
	        stringout = stringout+ str(testBit(byte,c))
		
	#put everything into groups of 8
	g=[]#list that contains the values of each byte
	bytenum=0
	while(True):
	    if bytenum==256-1:
	        break
	    if bytenum%8==0:
	        g.append(0)
	    if stringout[bytenum]=="1":
	        g[len(g)-1]=setBit(g[len(g)-1],bytenum%8)
	    bytenum=bytenum+1
	stringout=""
	if spaces:
		symbols=" "+symbols
	chars=string.ascii_uppercase + string.ascii_lowercase+string.digits +  symbols
	for element in g:
	    stringout=stringout+chars[element%len(chars)]
	
	return stringout
