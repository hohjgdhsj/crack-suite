#!/bin/bash/python
#coding=utf-8
#le4f.net

import copy
import enchant

vals = [
		[],
		[],
		["a","b","c"],
		["d","e","f"],
		["g","h","i"],
		["j","k","l"],
		["m","n","o"],
		["p","q","r","s"],
		["t","u","v"],
		["w","x","y","z"],
		]

def getnum(strnum):
	return ord(strnum) - 48

def decrypt(value):
	letters= []
	for c in value:
		letters.append(vals[getnum(c)])

	length = len(letters)
	table = [ [[] for x in range(length+1)] for y in range(length)]
	for i in range(length):
		solutioni = []
		for c in letters[i]:
			solution = [""] * length
			for j in range(length):
				if j == i:
					solution[j] = c
			solutioni.append(solution)
		table[i][1] = solutioni

	for j in range(2, length+1):
		for i in range(length):
			solution = []
			if not j-1 == i:
				for g in table[i][j-1]:
					for a in table[j-1][1]:
						x = copy.copy(g)
						x[j-1] = a[j-1]
						solution.append(x)
				table[i][j] = solution
	size = len(value)
	for i in range(length):
		if not len(table[i][size]) == 0:
			for s in table[i][size]:
				word=''.join(c for c in s)
				chkwords(word)
	
def chkwords(words):
	d = enchant.Dict("en_US")
	if d.check(words):
		print words

if __name__ == "__main__":
	from optparse import OptionParser	
	parser = OptionParser()
	parser.add_option(
	        '-n','--nums',
		dest = 'nums',
		help = u'nums of possible words')
	(options, args) = parser.parse_args()
	if options.nums:
		print '-----------------'
		numlist = options.nums.split('1')
		for value in numlist:
			decrypt(value)
			print '-----------------'
	else:
		print parser.print_help()
