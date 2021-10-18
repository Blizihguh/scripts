Miscellaneous scripts that don't require their own repositories, but which might maybe be helpful to someone at some point. All scripts are provided as-is, with no guarantee of functionality, portability, maintainability, sanity, or decency.

# JMusicBot Playlist Generator
A script to generate playlist files for [John Grosh's JMusicBot](https://github.com/jagrosh/MusicBot/). When run with no arguments, it outputs a playlist.txt file which contains absolute paths of all the audio files in the directory. The first argument is the directory to get music from; the second argument is the filename to output. Arguments are optional and positional (so you need to give a directory if you want to give a filename). Currently does not handle non-ASCII characters properly, at least on my machine.

# Multipurpose File Ripper
A script to extract (uncompressed, unencrypted) files that are embedded in a file. Supports a bunch of multimedia filetypes, and is pretty easy to extend if you want to support more. The blessing and curse of this script is its simplicty; it doesn't do any fancy file parsing, it just looks for file signatures and then saves them. This means it's basically guaranteed to find anything that's there, as long as the files' headers are stored in plaintext. But this naive approach is likely to be slow on large files, and won't capture metadata like filenames. Also, there is a very small but nonzero chance that it might read garbage data as a file, if your input file happens to contain the magic numbers of a supported filetype in some place that isn't actually a file.

Various commandline arguments are supported; run with the help flag or look inside the script for more info about these. Some sample config .inis are provided, but these are not necessary to use.

# SSBU Ironman Graph Generator
A script to generate an HTML graph for a [1v1 Smash Ironman](https://www.ssbwiki.com/Ironman#Full_Roster_Ironman), with fancy tooltips and stuff. Uses Bokeh. Some effort has been made to make it easy to edit, but given the nature of webdev, I wouldn't be surprised if this just completely breaks at some point. Assumes you're doing a full-roster ironman in SSBU, but it should be fairly easy to convert it to a more sane format by just deleting characters from the list.

# Windows IME Fix
Windows' IME (for converting QWERTY keyboard input to Japanese characters) is horrible. This AHK script makes it more palatable by replacing the messy, obnoxious, uncomfortable, generally-awful keybinds with two buttons: F1 to cycle between latin/hiragana/katakana, and F2 to cycle between half-width and full-width.