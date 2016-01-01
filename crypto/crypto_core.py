import click
import sys

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOLS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""

# Implementation of the reverse cypher
# Also an implementation of its decryption
def reverse(s):
	out = ''
	for i in range(0, len(s)):
		out = s[i] + out
	return out

def caesar(s, key, encrypt=True):
	out = ''
	s = s.upper()
	for char in s:
		if char in LETTERS:
			char_num = LETTERS.find(char)
			if encrypt:
				char_num = (char_num + key) % len(LETTERS)
			else:
				char_num = (char_num - key) % len(LETTERS)
			out += LETTERS[char_num]
		else:
			out += char
	return out

def transposition(s, key, encrypt=True):
	if encrypt:
		grid = [''] * key
		for col in range(key):
			pointer = col
			while pointer < len(s):
				grid[col]+= s[pointer]
				pointer += key
		return ''.join(grid)
	else:
		num_cols = len(s)/key
		if len(s) - (num_cols*key) > 0:
			num_cols += 1
		num_rows = key
		num_shad = (num_cols * num_rows) - len(s)
		out = [''] * num_cols
		col, row = 0, 0
		for char in s:
			out[col] += char
			col += 1
			if col == num_cols or (col == num_cols -1 and row >= num_rows - num_shad):
				col = 0
				row += 1
		return ''.join(out)
# READ UP ON BRUTE-FORCING TRANSPOSITION


obfuscator = {'O':'0', 'E':'3', 'L':'1', 'T':'7', 'S':'5'}
def obfuscate(s, encrypt=True):
	out = ''
	s = s.upper()
	if encrypt:
		dictionary = obfuscator
	else:
		dictionary = {v:k for k,v in obfuscator.items()}
	for char in s:
		if char in dictionary:
			out += dictionary[char]
		else:
			out += char
	return out


# Multiplicative/Affine family
def gcd(x, y):
	while x != 0:
		x, y = y % x, x
	return y

def mod_inverse(a, m):
	if gcd(a, m) != 1:
		return None # no mod inverse exists if a & m aren't relatively prime
	u1, u2, u3 = 1, 0, a
	v1, v2, v3 = 0, 1, m
	while v3 != 0:
		q = u3 // v3 # // is the integer division operator
		v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
	return u1 % m

def multiplicative(s, key, encrypt=True):
	s = s.upper()
	out = ''
	if encrypt == False:
		key = mod_inverse(key, len(LETTERS))
	for char in s:
		if char in LETTERS:
			num = (key * LETTERS.find(char)) % len(LETTERS)
			out += LETTERS[num]
		else:
			out += char
	return out

def key_parts(key):
	keyA = key // len(SYMBOLS)
	keyB = key % len(SYMBOLS)
	return (keyA, keyB)

def affine(s, key, encrypt=True):
	keyA, keyB = key_parts(key)
	out = ''
	if not encrypt:
		mod_inverse_A = mod_inverse(keyA, len(SYMBOLS))
	for char in s:
		if char in SYMBOLS:
			i = SYMBOLS.find(char)
			if encrypt:
				out += SYMBOLS[(i * keyA + keyB) % len(SYMBOLS)]
			else:
				out += SYMBOLS[(i - keyB) * mod_inverse_A % len(SYMBOLS)]
		else:
			out += char
	return out


def simple_sub(s, key, encrypt=True):
	assert len(key) == len(LETTERS), "Simple substitution key must be " + str(len(LETTERS)) + " long."
	if not encrypt:
		charA, charB = key, LETTERS
	else:
		charB, charA = key, LETTERS
	out = ''
	for char in s.upper():
		if char in charA:
			out += charA[charB.find(char)]
		else:
			out += char
	return out


def vigenere(s, key, encrypt=True):
	out = ''
	key_index = 0
	key = key.upper()
	for symbol in s:
		num = LETTERS.find(symbol.upper())
		if num != -1:
			if encrypt:
				num += LETTERS.find(key[key_index])
			else:
				num -= LETTERS.find(key[key_index])
			num %= len(LETTERS)
			if symbol.isupper():
				out += LETTERS[num]
			elif symbol.islower():
				out += LETTERS[num].lower()
			key_index += 1
			if key_index == len(key):
				key_index = 0
		else:
			out += symbol
	return out

# TODO: having trouble with passing in/parsing text to encrypt with the flags here

@click.command()
# @click.option("-f", default="", help="A file to encrypt")
@click.option("-e", "--encrypt", default="", help="Encrypt the input")
@click.option("-d", "--decrypt", default="", help="Decrypt the input")
@click.option("-v", "--vig", default="", help="Takes a memorable string key")
@click.option("-s", "--sub", default="", help="Takes a 26-letter scrambled alphabet key")
@click.option("-a", "--aff", default="", help="Takes a large number key")
@click.option("-o", "--obf", is_flag=True, help="Obfuscate text. Destructive with some encryption: careful.")
@click.option("-t", "--tra", default="", help="Takes a number key")
@click.option("-c", "--cae", default="", help="Takes a number key")
@click.option("-r", "--rev", is_flag=True, help="Reverse text.")
def main(encrypt, decrypt, vig, sub, aff, obf, tra, cae, rev):
	if encrypt:
		s = encrypt
	elif decrypt:
		s = decrypt
	else:
		click.echo(click.style("-e to encrypt, -d to decrypt", fg="red"))
		sys.exit(0)
	if not (vig or sub or aff or obf or tra or cae or rev):
		click.echo(click.style("How to encrypt?", fg="red"))
		sys.exit(0)

	if encrypt:
		# Do the encrypt order
		if vig:
			s = vigenere(s, vig)
		if sub:
			s = simple_sub(s, sub)
		if aff:
			s = affine(s, aff)
		if obf:
			s = obfuscate(s)
		if tra:
			s = transposition(s, tra)
		if cae:
			s = caesar(s, cae)
		if rev:
			s = reverse(s)
		click.echo(
			click.style(
				"Contents encrypted successfully! \n\n" + s,
				fg="green"))
		sys.exit(1)
	else:
		# Do the decrypt order
		if rev:
			s = reverse(s)
		if cae:
			s = caesar(s, cae, encrypt=False)
		if tra:
			s = transposition(s, tra, encrypt=False)
		if obf:
			s = obfuscate(s, encrypt=False)
		if aff:
			s = affine(s, aff, encrypt=False)
		if sub:
			s = simple_sub(s, sub, encrypt=False)
		if vig:
			s = vigenere(s, vig, encrypt=False)
		click.echo(
			click.style(
				"Contents decrypted successfully! \n\n" + s,
				fg="green"))
		sys.exit(1)