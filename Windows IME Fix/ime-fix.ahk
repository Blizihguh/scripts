; Set threads to 2 so we can run the script again while it's already running
#MaxThreadsPerHotkey 2

; Microsoft IME is very buggy. Some of the alleged shortcuts do not work, and others work in strange and unexpected ways.
; Logically, this should have three states: one for Hira, one for Kata, and one for HWAN.
; However, there is no key to set the mode to HWAN like there is for Hira and Kata, and the only command that does exist exhibits a strange, glitchy cycle.
; Doubling the number of modes fixes the problem.
; Note: +{CapsLock} turns FWAN on, but if you enter FWAN mode from a non-Hiragana input mode, it's buggy

mode := 0

F1::
if (mode == 0) {
	Send ^{CapsLock} ; Turn Hiragana on
	mode := 1
} else if (mode == 1) {
	Send !{CapsLock} ; Turn Katakana on
	mode := 2
} else if (mode == 2) {
	Send !`` ; Turn HWAN on
	mode := 3
} else if (mode == 3) {
	Send !`` ; Turn HWAN off (which sets mode back to Katakana) and then turn Hiragana on
	Send ^{CapsLock}
	mode := 1
} else if (mode == 4) {
	Send !{CapsLock} ; Turn Katakana on
	mode := 2
} else if (mode == 5) {
	Send !`` ; Turn HWAN on
	mode := 1
}
return

; Unfortunately, because Microsoft IME is full of weird unchangeable commands, it is very easy to accidentally hit some weird combo and ruin everything.
; The following lines disable most of these strange combos.
; TODO: None of these work for some reason.
$^CapsLock:: return ; disables switch to Hiragana
$!CapsLock:: return ; disables switch to Katakana
$+CapsLock:: return ; disables switch to FWAN

; WinKey+Space introduces its own special problem. Switching between English and Japanese will cause Firefox (and I think Chrome) to hang for sometimes several minutes.
; This is true even on my state-of-the-art laptop, and appears to be completely unfixable on Firefox's end. The problem exists solely with a Microsoft dll called imetip.
; Fixing Microsoft's dll problems is going to be hard, but disabling the command to change between English and Japanese is easy.
; It is not recommended to re-add this command unless you really need it. Is there even any benefit to having the English keyboard there, when the HWAN input mode behaves identically?
#space:: return