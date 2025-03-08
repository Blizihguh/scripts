from pathlib import Path
import re
import os

# Directory to search for xml files in
# Backslashes are necessary for this to work on Windows
INPUT_DIRECTORY = "..\\Translation\\" 
# Directory to put output files in
OUTPUT_DIRECTORY = "..\\Fixed XML\\"
# Lists of tags to make self-closing
# Tags with data attributes get their own list, because the regex is different for them
SIMPLE_TAGS = { "option_1", "option_2", "greater_than", "lesser_than", "end_line", "quote", "player_name", "hearth", 
		 "player_nickname", "paw", "music_note",  "left_arrow", "weapon_type", "black_dot", "three_dots"} 
ATTR_TAGS = { "portrait_l", "portrait_r", "player", "partner", "info" }

def fix_file(file_contents, regexes):
	"""
	Modify file_contents to update all instances of the specified tags.
	"""
	output = file_contents
	for regex in regexes:
		output = regex.sub(r"\1 />", output)

	return output


def fix_all_files_in_directory(input_dir, output_dir, regexes):
	"""
	Return a set of all tags that exist in all xml files in the given directory.
	This is very basic; open-close pairs and tags with different attributes will be treated as different.
	eg, <foo name="bar"> will be treated as a different tag from <foo name="baz">,
		and <foo> will be treated as a different tag from </foo>
	"""
	xml_files = list(Path(input_dir).rglob("*.[xX][mM][lL]")) # Get a list of all xml files in the path recursively

	for filename in xml_files:
		print("Fixing " + str(filename))
		with open(filename, "r", encoding="utf-8") as f:
			text = f.read()

		results = fix_file(text, regexes)

		output_filename = str(filename).replace(input_dir, output_dir, 1) # Only modify the first occurrence, to prevent errors like /Foo/Foo/ -> /Bar/Bar/
		output_path = os.path.dirname(output_filename)
		os.makedirs(output_path, exist_ok=True)
		with open(output_filename, "w", encoding="utf-8") as o:
			o.write(results)


	print("Fixed " + str(len(xml_files)) + " files")

if __name__ == "__main__":
	# We pre-compile the regexes for efficiency
	regexes = set()
	# I think this could be compiled into one regex with .*?, but this works fine too and is less likely to break things
	for t in SIMPLE_TAGS:
		regexes.add( re.compile("(<" + t + ")>") )
	for t in ATTR_TAGS:
		regexes.add( re.compile("(<" + t + ".+?)>") )

	fix_all_files_in_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY, regexes)