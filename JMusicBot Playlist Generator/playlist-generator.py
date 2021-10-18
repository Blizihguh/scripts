import os, sys
import unicodedata as ud

FILETYPES = (".mp3", ".m4a", ".opus", ".ogg", ".flac", ".wav")
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
OUTPUT_FL = "output.txt"

if len(sys.argv) > 1:
	DIRECTORY = sys.argv[1]
if len(sys.argv) > 2:
	OUTPUT_FL = sys.argv[2]

with open(OUTPUT_FL, "w") as file:
	for filename in os.listdir(DIRECTORY):
		for filetype in FILETYPES:
			if filename.endswith(filetype):
				#TODO: Does not work with non-ASCII characters
				file.write(DIRECTORY + "\\" + filename + "\n")