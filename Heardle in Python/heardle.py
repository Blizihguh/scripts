from pydub import AudioSegment
from pydub.playback import play
import os
import random

"""
<http://builds.libav.org/windows/release-gpl/libav-11.3-win64.7z>
Add bin of above to %PATH%
python3 -m pip install pydub
python3 -m pip install simpleaudio
"""

ONE_SEC = 1000
ROUNDS = [1, 2, 4, 7, 11, 16]
DIR = "D:\\Music\\Albums"

def random_file(directory):
	"""
	Biased towards files that are less deep in the hierarchy
	"""
	file = os.path.join(directory, random.choice(os.listdir(directory)));
	if os.path.isdir(file):
		return random_file(file)
	else:
		return file

def random_song(directory):
	song = None
	while song == None:
		file = random_file(directory)
		if file.lower().endswith((".mp3")):
			song = file
			break
	return song

def clip_song(song, rnd):
	return song[:ONE_SEC*ROUNDS[rnd]]

def heardle_init():
	name = random_song(DIR)
	audio = AudioSegment.from_file(name, "mp3")
	clips = []
	for i in range(len(ROUNDS)):
		clips.append(clip_song(audio,i))

	heardle_repl(name, clips)


def heardle_repl(name, clips):
	rnd = 0
	while True:
		heardle_print_cli(rnd)
		x = input("")
		if x.lower().startswith("p"):
			play(clips[rnd])
		elif x.lower().startswith("c"):
			rnd += 1
			if rnd >= 6:
				break
		elif x.lower().startswith("e"):
			break
	print("The song was: " + name)

def heardle_print_cli(rnd):
	os.system('cls' if os.name=='nt' else 'clear')
	print("===[ HEARDLE, Round " + str(rnd+1) + "/6 ]===============")
	print("Current length: " + str(ROUNDS[rnd]) + " seconds")
	print("[P]lay to play the clip, [C]ontinue to continue, [E]nd to end")
	print(">", end="")


heardle_init()