"""
Multipurpose File Ripper
Blizihguh 2019

Searches an uncompressed binary archive file for files of the specified type(s) and extracts them.
"""
import sys, re, struct, os, math, mmap, argparse, ConfigParser
from sortedcontainers import SortedSet

#TODO: Move copy_large_data and extract_ functions to their own file
#TODO: Docstring everything
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

def extract_dds(file, name):
	# Print DDS location
	verbose_print("DDS: "+name)
	with open(name+".dds", "wb") as output:
		# Write the header, since we ate it from the stream already
		output.write("\x44\x44\x53\x20")

		# Next, get the values from the header that we need in order to calculate the filesize
		# Immediately write them to the output as well, since they're important data!

		# Skip dwSize and dwFlags
		output.write(file.read(8))
		# Get height and width, write it to output, and unpack it
		height = file.read(4)
		width = file.read(4)
		output.write(height)
		output.write(width)
		height = struct.unpack("I", height)[0]
		width = struct.unpack("I", width)[0]
		# Skip dwPitchOrLinearSize, dwDepth, dwMipMapCount
		output.write(file.read(12))
		# Skip dwReserved1[11]
		output.write(file.read(44))
		# Skip ddspf:dwSize, ddspf:dwFlags
		output.write(file.read(8))
		# Get ddspf:dwFourCC, write it to output, and unpack it
		fmt = file.read(4)
		output.write(fmt)
		# Skip ddspf:dwRGBBitCount, ddspf:dwRBitMask, ddspf:dwGBitMask, ddspf:dwBBitMask, and ddspf:dwABitMask
		output.write(file.read(20))
		# Skip dwCaps, dwCaps2, dwCaps3, dwCaps4, and dwReserved2
		output.write(file.read(20))

		# Header having been parsed, calculate the length of the rest of the file
		# Formula retrieved from:
		# https://www.gamedev.net/forums/topic/529862-need-help-retrieving-image-data-from-dds-filesanswered/
		byteSize = ((width + 3)/4) * ((height + 3)/4) * (8 if fmt=="DXT1" else 16)

		# Then, write the actual data to output!
		copy_large_data(file, output, byteSize)
	# Print success message and return number of bytes to increment counter
	verbose_print("extracted successfully!\n")
	return (124+byteSize, "DDS")

def extract_png(file, name):
	verbose_print("PNG: " + name)
	with open(name+".png", "wb") as output:
		# Write the first four bytes of the header (since we ate them), then write the last four (whilst eating them)
		output.write("\x89\x50\x4E\x47")
		output.write(file.read(4))
		# PNG files consist of a series of chunks.
		# Thankfully, each chunk starts with its length, which makes this fairly easy to deal with.
		length = file.read(4)
		fmt = file.read(4)
		byteSize = 16
		while fmt != "IEND":
			# Write the header to output
			output.write(length)
			output.write(fmt)
			# Write the data to output
			length = struct.unpack(">I", length)[0] # PNG is big-endian! Who knew?
			# The PNG spec says that length should not exceed 2^31, but then, who cares about what the spec says?
			# Certainly not people who make PNG writers!
			copy_large_data(file, output, length)
			# Write the CRC to output
			output.write(file.read(4))
			# Continue on to next chunk
			byteSize = byteSize + length + 4
			length = file.read(4)
			fmt = file.read(4)
		# We've hit the IEND chunk, which means it's time to wrap up:
		output.write(length)
		output.write(fmt)
		output.write(file.read(4))
		byteSize = byteSize + 12
	# Print success message and return number of bytes to increment counter
	verbose_print("extracted successfully!\n")
	return (byteSize, "PNG")

def extract_ogg(file, name):
	verbose_print("OGG: " + name)
	with open(name+".ogg", "wb") as output:
		# Write the magic numbers that were consumed
		output.write("\x4F\x67\x67\x53")
		first = True # If it's the first loop, skip reading the magic number
		cont = True # Set to false once we've finished reading the file
		byteSize = 0 # Will be updated at the end of each page
		while cont:
			# Skip magic on first loop
			if first:
				first = False
			else:
				output.write(file.read(4))
			# Skip version
			output.write(file.read(1))
			# This byte will tell us whether we've reached the end of the file
			# The ogg format is slightly arcane, and in niche circumstances this may not actually work
			# For more information: https://en.wikipedia.org/wiki/Ogg#Page_structure
			# For even more information: https://stackoverflow.com/questions/20794204/how-to-determine-length-of-ogg-file/44407355
			isLast = file.read(1)
			output.write(isLast)
			isLast = (struct.unpack("B", isLast)[0] & 4) > 0
			# Skip granule position, bitstream serial number, page sequence number, and checksum
			output.write(file.read(20))
			# Get the number of segments to read before next page
			segmentCount = file.read(1)
			output.write(segmentCount)
			segmentCount = struct.unpack("B", segmentCount)[0]
			# Add up the length of each segment, calculating the number of bytes to be read before the next page
			bytesInPage = 0
			for i in xrange(segmentCount):
				b = file.read(1)
				output.write(b)
				bytesInPage = bytesInPage + struct.unpack("B", b)[0]
			# Read that many bytes
			output.write(file.read(bytesInPage))
			# Update byteSize
			byteSize = byteSize + 27 + segmentCount + bytesInPage # add size of header, segment table, and page
			# If that was the last page, we're done!
			if isLast:
				cont = False
	verbose_print("extracted successfully!\n")
	return (byteSize, "OGG")

def extract_ivf(file, name):
	verbose_print("IVF:" + name)
	with open(name+".ivf", "wb") as output:
		# Write the magic numbers that were consumed
		output.write("\x44\x4B\x49\x46")
		# Ignore version, header length, codec, width, height, and time base
		output.write(file.read(20))
		# Get number of frames
		frames = file.read(4)
		output.write(frames)
		frames = struct.unpack("<I", frames)[0]
		# Ignore unusued bytes
		output.write(file.read(4))
		# Write frames
		byteSize = 32
		while frames > 0:
			# Get size of frame in bytes
			size = file.read(4)
			output.write(size)
			size = struct.unpack("<I", size)[0]
			# Skip the rest of the header
			output.write(file.read(8))
			# Write the rest of the file
			copy_large_data(file, output, size)
			byteSize = byteSize + 12 + size
			frames = frames - 1
	verbose_print("extracted successfully!\n")
	return (byteSize, "IVF")

def extract_riff(file, name):
	# Get the size of the file and the filetype
	sizeStr = file.read(4)
	fmt = file.read(4)
	size = struct.unpack("<I", sizeStr)[0]
	# Figure out what type of riff file this is
	# .cdr files must be handled specially, as their header is "CDR*" instead of a set four-character string
	# Massive thanks to the following for providing much of this information:
	# https://www.garykessler.net/library/file_sigs.html
	ext = ".riff"
	if fmt[0:3] == "CDR":
		ext = ".cdr"
	else:
		riffTypes = {
			"WAVE": ".wav",
			"AVI ": ".avi",
			"RMID": ".rmi", # Riff Midi
			"CDDA": ".cda", # Compact Disc Digital Audio (CD-DA)
			"QLCM": ".qcp", # Qualcomm PureVoice (I do not know what this is)
			"WEBP": ".webp"
		}
		"""
			I could not find magic numbers for the following:
			"": ".rdi", # "Bitmapped data", according to soundfile.sapp.org/doc/WaveFormat -- BMP? DIB? rDIB?
			"": ".cmx", # Corel Presentation Exchange metafile (???)
			"": ".dls", # Downloadable Sounds
			"": ".xma", # XBox WMA (unsure if this is actually riff...?)
			"": ".pal", # Palette
			"": ".rmn", # "Multimedia Movie"
			"": ".ani", # Windows animated cursor format
			"": ".bnd" # Bundle of other RIFF files
		"""
		if fmt in riffTypes:
			ext = riffTypes[fmt]
	# Now that we know what type of riff it is, we can open the file and write the data!
	verbose_print(fmt + ": " + name)
	with open(name+ext, "wb") as output:
		# Write the data we already consumed
		output.write("\x52\x49\x46\x46")
		output.write(sizeStr)
		output.write(fmt)
		# Copy the rest of the file (size doesn't include the first 8 bytes, but DOES include the bytes that make up fmt)
		copy_large_data(file, output, size-4)
	verbose_print("extracted successfully!\n")
	return (size+8, fmt)

# Magic numbers of supported filetypes
"""
TODO: File formats
- AIFF (contains size in header)
- MP3 (common -- 0x49443303 should be doable, although 0xFFFB might be impossible)
- MIDI (common)
- FLAC (common enough)
- M4A (common enough)
- XMA (already implemented as RIFF, theoretically)

- MKV (common, albeit maybe not embedded frequently)
- MOV (common enough)
- MP4 (common)
- FLV (common enough)

- JPEG (common, although "proper JPEG files start with a two-byte header." some may have 0xFFD8FFEX instead of just 0xFFD8, though)
- BMP/DIB (common enough, contains size in header)
- TIFF (common enough I guess)
- GIF (common)
- ICO (theoretically easy, since it has a size-containing header, but I think the magic number is like 0x00001000 or some BS)

- ZIP
- RAR
"""
MAGIC = {
	"\x44\x44\x53\x20": ("DDS", extract_dds),
	"\x89\x50\x4E\x47": ("PNG", extract_png),
	"\x4F\x67\x67\x53": ("OGG", extract_ogg),
	"\x44\x4B\x49\x46": ("IVF", extract_ivf),
	"\x52\x49\x46\x46": ("RIFF", extract_riff) # eg WAV, AVI, WEBP, CDA, RMI, QCP
}
# Number of extracted files of each type
EXTRACTED = {}
# Verbose output?
global VERBOSE 
VERBOSE = False

def get_info_from_magic(num):
	for magic in MAGIC:
		if magic == num:
			return MAGIC[magic]
	return None

def prune_magic(fmt):
	for magic in MAGIC:
		if MAGIC[magic][0] == fmt.upper():
			MAGIC.pop(magic)
			break

def verbose_print(s):
	global VERBOSE
	if VERBOSE:
		print s,

def verbose_printf(s, t):
	global VERBOSE
	if VERBOSE:
		print s % t,

def clear_console():
	if os.name == "nt": # Windows
		_ = os.system("cls")
	else: # Mac/Linux
		_ = os.system("clear")


def print_progress(step, found, extracted):
	#TODO: Add progress bar (percent of file searched)
	#TODO: Add information on magic numbers skipped
	if not VERBOSE:
		clear_console()
		sys.stdout.write("Beginning search...\n")
		if step > 0:
			sys.stdout.write("File map created...\n")
		if step > 1:
			sys.stdout.write("Found %i magic number%s!\n" % (found, ("s" if found > 1 else "")))
		if step > 2:
			sys.stdout.write("Extracted %i file%s!\n" % (extracted, ("s" if extracted > 1 else "")))

def main():
	# Validate and process args
	parser = argparse.ArgumentParser(description="Extracts unencrypted/uncompressed files embedded inside of an unknown file or binary.")
	parser.add_argument("file", help="The file to be searched")
	parser.add_argument("-o", "--offset", type=int, default=0, help="The offset to start searching at")
	parser.add_argument("-v", "--verbose", type=bool, default=False, help="Enable verbose output?")
	parser.add_argument("-d", "--directory", default="rip", help="Directory to extract files to")
	parser.add_argument("-f", "--filetypes", default="", help="Select an .ini file to search only for specific filetypes (by default, all supported types will be searched for)")
	args = parser.parse_args()
	offset = args.offset
	directory = args.directory + "/"
	filename = args.file
	name = re.search("([^/]+)/?$", filename).group(0)[0:-4]
	global VERBOSE
	verbose = args.verbose
	pruningFile = args.filetypes

	# If pruningFile is set, prune MAGIC to remove anything that's not turned on in the ini
	if pruningFile != "":
		config = ConfigParser.ConfigParser()
		try:
			config.read(pruningFile)
			formats = config.items("Formats")
			for fmt in formats:
				if fmt[1] == "False":
					# Format is set to false, prune it from the dictionary
					prune_magic(fmt[0])
			if len(MAGIC) == 0:
				print "No file types selected! Exiting..."
				return
		except:
			print "Invalid config file! Exiting..."
			return

	# Get the path to save files to
	path = os.path.join(os.path.dirname(__file__), directory)
	if not os.path.exists(path):
		os.mkdir(path)

	# Get the number of digits necessary for filenames
	digits = 8
	fileSize = os.stat(filename).st_size
	if fileSize > 4294967295:
		digits = int(math.ceil(math.log(fileSize)/math.log(16))) # log_b(a) = log(a)/log(b)

	# Update console with beginning search message
	print_progress(0, 0, 0)
	# Open the file and begin searching
	with open(filename, "rb") as file:
		# Create a memory map of the file and update console info
		mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
		print_progress(1, 0, 0)
		# Find all the magic numbers we're looking for and get them in order
		extractables = SortedSet()
		foundCount = 0
		for magicString in MAGIC:
			offset = mm.find(magicString)
			while offset > -1:
				# Store the offset in our set of offsets
				extractables.add(offset)
				# Update info in console
				foundCount = foundCount + 1
				print_progress(2, foundCount, 0)
				verbose_print(MAGIC[magicString][0] + " found at " + str(offset) + "\n")
				# Move onto next file
				offset = mm.find(magicString, offset+1)
		# Now that we have the offsets, we can extract them!
		verbose_print("Found %i magic numbers!" % foundCount)
		extractedCount = 0
		for offset in extractables:
			# If we've already passed the offset, it was a segment of another file
			# Certain formats (eg ogg) will actually contain their magic number multiple times,
			# so we can use this to prevent saving partial files
			if(file.tell() > offset):
				verbose_printf("%i was a segment of a previously-dumped file and will be ignored\n", offset)
			else:
				verbose_printf("Seeking %i", offset)
				file.seek(offset)
				# Get the proper handler for the filetype
				info = get_info_from_magic(file.read(4))
				details = info[1](file, path+name+"_"+("%0*x" % (digits, offset)))
				# Update EXTRACTED with info
				if details[1] in EXTRACTED:
					EXTRACTED[details[1]] += 1
				else:
					EXTRACTED[details[1]] = 1
				# Update info in console
				extractedCount = extractedCount + 1
				print_progress(3, foundCount, extractedCount)
	print "Search completed:"
	for fmt in EXTRACTED:
		print "\t%i %s file%s extracted" % (EXTRACTED[fmt], fmt, ("s" if EXTRACTED[fmt] > 1 else ""))

main()