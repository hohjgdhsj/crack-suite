#!/usr/bin/python
#coding=utf-8
#le4f.net

import sys,time,hashlib,crypt

#字符集charset
charset = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-=@&*!~,.;'
charset1 = '0123456789'
charset2 = 'abcdefghijklmnopqrstuvwxyz'
charset3 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
charset4 = '0123456789abcdefghijklmnopqrstuvwxyz'
charset5 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#最小长度min
min = 1
#最大长度max-1
max = 9
def xselections(items, n):
	if n == 0:
		yield[]
	else:
		for i in range(len(items)):
			for ss in xselections(items, n-1):
				yield[items[i]]+ss

def dicrack(hash,format,dic):
	try:
		start = time.time()
		allTries = 0
		cycleInt = 3		
		for word in open(dic,'rU'):
			word = word.rstrip()
			allTries+=1
			if genhash(word,format,hash) == hash:
				stop = time.time()
				spent = stop - start
				print '[*] Hash: %s  Word: %s  Time: %.f seconds' % (hash,word, spent)                
				raise
			if (time.time()-start) >= cycleInt:
				cycleInt+=3
				print("[x] Word: "+ word + " ~ " + str(int((float(allTries) // (time.time()-start)))) + " Hashes/s")			
		raise
	except :
		end = time.time()
		print("[*] " + str(allTries) + " Hashes Tryed Takes " + str(end-start) + "s With Speed of " + str(int((float(allTries) // (end-start)))) + " Hashes/s")

def brute(hash,format):
	try:
		start = time.time()
		allTries = 0
		cycleInt = 3
		for i in range(min,max):
			for s in xselections(charset,i):
				word = ''.join(s)
				allTries+=1
				if genhash(word,format,hash) == hash:
					stop = time.time()
					spent = stop - start					
					print '[*] Hash: %s  Word: %s  Time: %.f seconds' % (hash,word,spent)               
					raise
				if (time.time()-start) >= cycleInt:
					cycleInt+=3
					print("[x] Word: "+ word + " ~ " + str(int((float(allTries) // (time.time()-start)))) + " Hashes/s")
		raise
	except :
		end = time.time()
		print("[*] " + str(allTries) + " Hashes Tryed Takes " + str(end-start) + "s With Speed of " + str(int((float(allTries) // (end-start)))) + " Hashes/s")

def genhash(word,format,hash):
	format = format.lower()
	if format == 'md5':
		return hashlib.md5(word).hexdigest()
	elif format == 'sha1':
		return hashlib.sha1(word).hexdigest()
	elif format == 'sha224':
		return hashlib.sha224(word).hexdigest()
	elif format == 'sha256':
		return hashlib.sha256(word).hexdigest()
	elif format == 'sha384':
		return hashlib.sha384(word).hexdigest()	
	elif format == 'sha512':
		return hashlib.sha512(word).hexdigest()			
	elif format == 'des':
		return crypt.crypt(word,hash[0:2:])
	else:
		print '[-] Format Not Find.'
		sys.exit()
		
def crack(hash,format,dic):
	if dic:
		print '[*] Crack Hash: '+ hash+ 'Using Dic: ' + dic
		dicrack(hash,format,dic)
	else:
		print '[*] Brute Crack Hash: '+ hash
		brute(hash,format)
	
	
if __name__ == "__main__":
	from optparse import OptionParser	
	parser = OptionParser()
	parser.add_option(
	        '-c','--hash',
		dest = 'hash',
		help = u'Hash To Crack')
	parser.add_option(
	        '-w','--wordlist',
		dest = 'dic',
		help = u'Crack With PasswordList[Optional]')
	parser.add_option(
	        '-f','--format',
		dest = 'format',
		help = u'Hash Format:MD5/DES/SHA1/SHA224/SHA256/SHA384/SHA512')		
	(options, args) = parser.parse_args()
	if options.hash and options.format:
		crack(options.hash,options.format,options.dic)
	else:
		print parser.print_help()