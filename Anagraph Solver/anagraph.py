FORMULAE = {
	"A": {"c": 1, "o": 0, "e": 0, "r": 0, "s": 0, "'": 1, "?": 0, ".": 0},
	"B": {"c": 1, "o": 0, "e": 0, "r": 0, "s": 0, "'": 2, "?": 0, ".": 0},
	"C": {"c": 1, "o": 0, "e": 0, "r": 0, "s": 0, "'": 0, "?": 0, ".": 0},
	"D": {"c": 1, "o": 0, "e": 0, "r": 0, "s": 0, "'": 2, "?": 0, ".": 0},
	"E": {"c": 0, "o": 0, "e": 1, "r": 0, "s": 0, "'": 0, "?": 0, ".": 0},
	"F": {"c": 0, "o": 0, "e": 0, "r": 0, "s": 0, "'": 1, "?": 1, ".": 0},
	"G": {"c": 1, "o": 0, "e": 0, "r": 0, "s": 0, "'": 0, "?": 1, ".": 0},
	"H": {"c": 0, "o": 0, "e": 0, "r": 1, "s": 0, "'": 2, "?": 0, ".": 0},
	"I": {"c": 0, "o": 0, "e": 0, "r": 0, "s": 0, "'": 1, "?": 0, ".": 1},
	"J": {"c": 0, "o": 0, "e": 0, "r": 0, "s": 0, "'": 0, "?": 1, ".": 1},
	"K": {"c": 0, "o": 0, "e": 0, "r": 0, "s": 0, "'": 4, "?": 0, ".": 0},
	"L": {"c": 0, "o": 0, "e": 0, "r": 0, "s": 0, "'": 2, "?": 0, ".": 0},
	"M": {"c": 0, "o": 0, "e": 0, "r": 2, "s": 0, "'": 1, "?": 0, ".": 0},
	"N": {"c": 0, "o": 0, "e": 0, "r": 1, "s": 0, "'": 1, "?": 0, ".": 0},
	"O": {"c": 0, "o": 1, "e": 0, "r": 0, "s": 0, "'": 0, "?": 0, ".": 0},
	"P": {"c": 1, "o": 0, "e": 0, "r": 0, "s": 0, "'": 2, "?": 0, ".": 0},
	"Q": {"c": 1, "o": 0, "e": 0, "r": 0, "s": 0, "'": 2, "?": 0, ".": 0},
	"R": {"c": 0, "o": 0, "e": 0, "r": 1, "s": 0, "'": 0, "?": 0, ".": 0},
	"S": {"c": 0, "o": 0, "e": 0, "r": 0, "s": 1, "'": 0, "?": 0, ".": 0},
	"T": {"c": 0, "o": 0, "e": 0, "r": 0, "s": 0, "'": 3, "?": 0, ".": 0},
	"U": {"c": 0, "o": 0, "e": 0, "r": 1, "s": 0, "'": 1, "?": 0, ".": 0},
	"V": {"c": 0, "o": 0, "e": 0, "r": 0, "s": 0, "'": 2, "?": 0, ".": 0},
	"W": {"c": 0, "o": 0, "e": 0, "r": 0, "s": 0, "'": 4, "?": 0, ".": 0},
	"X": {"c": 0, "o": 0, "e": 0, "r": 0, "s": 0, "'": 4, "?": 0, ".": 0},
	"Y": {"c": 0, "o": 0, "e": 0, "r": 1, "s": 0, "'": 1, "?": 1, ".": 0},
	"Z": {"c": 0, "o": 0, "e": 0, "r": 0, "s": 0, "'": 3, "?": 0, ".": 0}
}

LEX = []

def build_lex(dfile):
	# is it faster to break up the dictionary by word length?
	# once upon a time <s>I</s> my professor guessed so, so that is what this does
	words = []
	for _ in range(16):
		words.append(set())
	for line in open(dfile):
		w = line.strip().lower()
		w = "".join([i for i in w if i.isalpha()])
		if len(w) <= 15:
			words[len(w)].add(w)
	return words

def atomize(word):
	# Convert a word to its atoms
	atoms = {"c": 0, "o": 0, "e": 0, "r": 0, "s": 0, "'": 0, "?": 0, ".": 0}
	for char in word:
		for atom in "coers'?.":
			atoms[atom] += FORMULAE[char][atom]
	return atoms

def stringify(atoms):
	output = ""
	for atom in "coers'?.":
		output += atom*atoms[atom]
	return output

def print_anagraphs(atoms, length, lex):
	# Loop over the dictionary and print matching words
	string = stringify(atoms)
	if length != "*":
		length = int(length)
		for word in lex[length]:
			if stringify(atomize(word.upper())) == string:
				print(word)
	else:
		for size in range(len(lex)):
			for word in lex[size]:
				if stringify(atomize(word.upper())) == string:
					print(word)

def solve_final(lex):
	for i in "abcdefghijklmnopqrstuvwxyz":
		print("##### " + i.upper() + " #####")
		string = i+"JLPPSSCVFAVCPVIP"
		for size in range(len(lex)):
			for word in lex[size]:
				for size2 in range(len(lex)):
					for word2 in lex[size2]:
						if stringify(atomize(word.upper() + word2.upper())) == string:
							print(word)

LEX = build_lex("american-english.txt")
while True:
	word = raw_input("Enter a word to make anagraphs of: ")
	length = raw_input("Enter the desired anagraph length, or * for any length: ")
	word = word.upper()
	atoms = atomize(word)
	print("Decomposition: " + stringify(atoms))
	print_anagraphs(atoms, length, LEX)
	print("")