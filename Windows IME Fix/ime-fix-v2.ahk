; Edited version of original script that works with AutoHotKey Version 2.0
; Note: Assumes the Microsoft Japanese IME is set to default 
; Microsoft IME template (as opposed to ATOK etc.)

#MaxThreadsPerHotkey 2

mode := 0

F1::
{
global
if (mode = 0) {
	Send "^{CapsLock}" ; Turn Hiragana on
	mode := 1
}else if (mode == 1) {
	Send "!{CapsLock}" ; Turn Katakana on
	mode := 2
} else if (mode == 2) {
	Send "!``" ; Turn HWAN on
	mode := 3
} else if (mode == 3) {
	Send "!``" ; Turn HWAN off (which sets mode back to Katakana) and then turn Hiragana on
	Send "^{CapsLock}"
	mode := 1
} else if (mode == 4) {
	Send "!{CapsLock}" ; Turn Katakana on
	mode := 2
} else if (mode == 5) {
	Send "!``" ; Turn HWAN on
	mode := 1
}

}

; Unfortunately, because Microsoft IME is full of weird unchangeable commands, it is very easy to accidentally hit some weird combo and ruin everything.
; The following lines disable most of these strange combos.
; TODO: None of these work for some reason.
$^CapsLock:: return ; disables switch to Hiragana
$!CapsLock:: return ; disables switch to Katakana
$+CapsLock:: return ; disables switch to FWAN

#space:: return