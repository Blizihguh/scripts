import sys

def build_dict(f):
	lex = {}
	with open(f) as dfile:
		for line in dfile:
			w = line.strip().lower()
			lex[w] = hash_word(w)

	return lex

def hash_word(word):
	return "".join(sorted(set(word)))

def is_valid(word_hash, board):
	if not board[0] in word_hash:
		return False
	for letter in word_hash:
		if not letter in board:
			return False
	return True

def is_pangram(word, board):
	for letter in board:
		if not letter in word:
			return False
	return True

def get_words_in_board(lex, board):
	valid_words = set()
	for word in lex.keys():
		if is_valid(lex[word], board):
			valid_words.add(word)
	return valid_words

def score_word(word, word_hash):
	length = 1 if len(word) == 4 else len(word) # 4-letter words score 1, otherwise they score their length
	if len(word_hash) == 7: # Pangrams score bonus points
		return 7 + length
	return length

def calculate_board_score(lex, words):
	total = 0
	for word in words:
		total += score_word(word, lex[word])
	return total

def board_generator(h):
	for letter in h:
		yield letter + h.replace(letter, "")

def get_valid_boards(lex):
	# Get all possible pangrams
	pangram_hashes = set()
	for word in lex:
		# We can skip the expensive hash function for words less than 7 characters long
		if len(word) < 7:
			continue
		# Get the hash of the word and add it if it contains exactly 7 letters
		h = hash_word(word)
		if len(h) == 7:
			pangram_hashes.add(h)
	# For every pangram, there are seven boards to be made
	boards = set()
	for p in pangram_hashes:
		for board in board_generator(p):
			boards.add(board)
	return boards

def find_global_extrema(f="wordlists/enable1.txt"):
	lex = build_dict(f)
	boards = get_valid_boards(lex)

	print(str(len(lex)) + " words in lexicon")
	print(str(len(boards)) + " valid boards")

	input("Ready? ")

	best_board = ""
	best_score = 0

	worst_board = ""
	worst_score = 1000000

	for board in boards:
		# Get all the words in the board
		words = get_words_in_board(lex, board)
		score = calculate_board_score(lex, words)

		# Did we find what we're looking for?
		if score >= best_score:
			print("NEW BEST BOARD: " + board)
			print(score)
			print(words)
			best_board = board
			best_score = score
		elif score <= worst_score:
			print("NEW WORST BOARD: " + board)
			print(score)
			print(words)
			worst_board = board
			worst_score = score

def solve_board(board, f="wordlists/enable1.txt"):
	lex = build_dict(f)
	words = get_words_in_board(lex, board)
	score = calculate_board_score(lex, words)
	words_sorted = {}
	for word in words:
		if not len(word) in words_sorted:
			words_sorted[len(word)] = [word]
		else:
			words_sorted[len(word)].append(word)

	print("Board: ", board)
	print("Total score: ", score)
	for number in sorted(words_sorted.keys()):
		print("Words of length " + str(number) +  ": ", words_sorted[number])
	

if sys.argv[1] == "all": # Usage: python3 spelling-bee.py all
	find_global_extrema()
else: # Usage: python3 spelling-bee.py <board, with central letter as the first letter>
	solve_board(sys.argv[1])