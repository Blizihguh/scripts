# Initial puzzle state
initialState = []

# Settings
FIND_MULTIPLE_SOLUTIONS = False # Do we want to keep going after we find a solution? If we don't care about the solution being unique this can be False
FIND_HIGH_SCORE         = False # Do we care about "high-scoring" partial solves? If we're sure the puzzle is solvable and don't care about the time it takes, this can be False

# Meta-state variables
global currentHighScore, currentBestPartialSolve, currentSolves, currentSolveCount
currentHighScore = 0
currentBestPartialSolve = None
currentSolves = []
currentSolveCount = 0

class Puzzle:
	def __init__(self, state):
		"""
		Set up all state for the puzzle here
		"""
		self.state = state
	
	def clone(self):
		"""
		Return a new copy of the Puzzle
		The copy library can help, but may not be as efficient as (eg) list comprehensions if you don't need to copy EVERYTHING
		"""
		# For a 2D array, you can use this:
		# clonedState = [val[:] for val in self.state]
		clonedState = [val for val in self.state]
		return Puzzle(clonedState)

	def __str__(self):
		"""
		Return a string to print
		"""
		return str(self.state)

	def is_solved(self):
		"""
		Return True if the puzzle is solved, or False otherwise
		"""
		return False

	def is_valid(self):
		"""
		Return False if the puzzle is unsolvable from the current state, or True otherwise
		"""
		return True

	def generate_options(self):
		"""
		Generate all the possible values we could set in the current state with set_value
		"""
		for pos in range(len(self.state)):
			newPuzzle = self.clone()
			newPuzzle.set_value(pos, 0)
			yield newPuzzle

	def set_value(self, pos, val):
		"""
		Setter for puzzle state
		"""
		self.state[pos] = val

	def get_score(self):
		"""
		Evaluate the "score" of a partial solve
		If FIND_HIGH_SCORE is on, we use this to determine whether one solve is "better" than another
		"""
		return 0

def solve(puzzle):
	global currentHighScore, currentBestPartialSolve, currentSolves, currentSolveCount
	
	# If we have a solution and only care about finding one, we can just exit now
	if not FIND_MULTIPLE_SOLUTIONS and currentSolveCount > 0:
		return
	
	# Check if this is a solution
	if puzzle.is_solved():
		print("Solution found!")
		print(puzzle)
		if FIND_HIGH_SCORE:
			print("Score: ", puzzle.get_score())
		currentSolves.append(puzzle)
		currentSolveCount += 1
	
	# Check if this is a high score
	if FIND_HIGH_SCORE:
		if score := puzzle.get_score() > currentHighScore:
			print("New high score!")
			print(puzzle)
			currentBestPartialSolve = puzzle
			currentHighScore = score
	
	# Check if the puzzle is unsolvable from this state
	if not puzzle.is_valid():
		return
	
	# If we reach this point, it's time to branch!
	for puz in puzzle.generate_options():
		solve(puz)

if __name__ == "__main__":
	puz = Puzzle(initialState)
	solve(puz)