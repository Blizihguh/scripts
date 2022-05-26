"""
AGAR WAD Dumper
Blizihguh 2022

Dumper for 428: Shibuya Scramble, and probably other games developed by Abstraction Games
See also: https://github.com/TcT2k/HLMWadExplorer/issues/4
          https://wiki.spiralframework.info/WAD
"""
import struct, os, math, mmap

# Settings
global OUTPUT_DIR, FILENAME
OUTPUT_DIR = "main_dump/"
FILENAME = "shibuya_desktop_data_main.wad"

def copy_large_data(file, output, length):
	maxSize = 2147483647 # I don't know why this is 2147483647 and not sys.maxsize either!
	if length < maxSize: 
		output.write(file.read(length))
	else:
		# data is bigger than maxSize, so we have to do it in parts
		sizeLeft = length
		while sizeLeft > maxSize:
			output.write(file.read(maxSize))
			sizeLeft = sizeLeft - maxSize
		output.write(file.read(sizeLeft))

# Note: Removed "\r" in the progress bar print function because it was behaving weirdly with low length values
# Manual blank print after status but before progress bar deals with lack of "\r" in function
# https://stackoverflow.com/a/34325723
# Actually, I borrowed this function from a friend, so the chain of custody is even longer than that stackex link implies...
def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
	"""
	Call in a loop to create terminal progress bar
	@params:
			iteration   - Required  : current iteration (Int)
			total       - Required  : total iterations (Int)
			prefix      - Optional  : prefix string (Str)
			suffix      - Optional  : suffix string (Str)
			decimals    - Optional  : positive number of decimals in percent complete (Int)
			length      - Optional  : character length of bar (Int)
			fill        - Optional  : bar fill character (Str)
			printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print(f'{prefix} |{bar}| {percent}% {suffix}', end = printEnd)

	# Print New Line on Complete
	if iteration == total: 
		print()

def main():
	# Get the path to save files to
	path = os.path.join(os.path.dirname(__file__), OUTPUT_DIR)
	if not os.path.exists(path):
		os.makedirs(path)

	# Get the number of digits necessary for filenames
	digits = 8
	fileSize = os.stat(FILENAME).st_size
	if fileSize > 4294967295:
		digits = int(math.ceil(math.log(fileSize)/math.log(16))) # log_b(a) = log(a)/log(b)

	# Open the file and begin searching
	with open(FILENAME, "rb") as file:
		# Find all the file offsets and lengths we're looking for
		files = set()
		directories = set()

		# Skip version info
		file.seek(12)

		# Skip header data
		header_length = struct.unpack("I", file.read(4))[0]
		file.seek(header_length,1)

		# Get info for all files
		num_files = struct.unpack("I", file.read(4))[0]

		for i in range(num_files):
			file_name_length = struct.unpack("I", file.read(4))[0]
			file_name = struct.unpack("{}s".format(file_name_length), file.read(file_name_length))[0].decode("utf-8")
			file_size = struct.unpack("q", file.read(8))[0] & 0x7FFFFFFFFFFFFFFF # Set high bit to 0 -- I don't know why they're stored with a high bit of 1, but they are...
			file_offset = struct.unpack("q", file.read(8))[0] & 0x7FFFFFFFFFFFFFFF
			files.add((file_name, file_size, file_offset))

		# Get info for all directories
		num_dirs = struct.unpack("I", file.read(4))[0]

		for i in range(num_dirs):
			dir_name_length = struct.unpack("I", file.read(4))[0]
			dir_name = struct.unpack("{}s".format(dir_name_length), file.read(dir_name_length))[0].decode("utf-8")
			num_subfiles = struct.unpack("I", file.read(4))[0]
			subfiles = []
			for j in range(num_subfiles):
				subfile_name_length = struct.unpack("I", file.read(4))[0]
				subfile_name = struct.unpack("{}s".format(subfile_name_length), file.read(subfile_name_length))[0].decode("utf-8")
				subfile_isdir = struct.unpack("?", file.read(1))[0]
				subfiles.append((subfile_name, subfile_isdir))
			directories.add((dir_name, tuple(subfiles)))

		print("Found %i files and %i directories!" % (len(files), len(directories)))

		# Create all directories
		for dir_info in directories:
			os.makedirs(OUTPUT_DIR + dir_info[0], exist_ok=True)

		print("Directories created!")

		data_start_pos = file.tell()
		mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)

		copied = 0

		for output_file in files:
			name = output_file[0]
			length = output_file[1]
			offset = output_file[2]
			copied += 1

			print_progress_bar(copied, num_files, f"[{copied}/{num_files}]")

			with open(OUTPUT_DIR + name, "wb") as f:
				mm.seek(data_start_pos + offset)
				copy_large_data(mm, f, length)

main()