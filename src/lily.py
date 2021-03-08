from src import lib
from src import builtin
from src import effects

# Lilypond-like parser

# A7 = 3520
# A6 = 1760
# A5 =  880
# A4 =  440
# A3 =  220
# A2 =  110
# A1 =   55


def load(string, bpm=120, instrument=lambda x: builtin.sin_lr(-6, x, 'lily-load'), fadein=1/30, fadeout=9/10):
	current_clef = 4
	tokens = string.split()
	project = lib.Project('lily-proj')

	cpos = 0

	for token in tokens:
		clip = note2clip(token, bpm, instrument, fadein, fadeout)
		project.add_clip(clip, cpos)
		cpos += len(clip)


	return lib.Clip.from_project(project)


def note2clip(note, bpm, function, fadein, fadeout):
	mpm = bpm * 4			# measures per minute
	cptr = 0
	base = note[cptr]
	freq = 440
	# change the base frequency
	if base == 'a':
		pass
	elif base == 'b':
		freq *= 2**(2/12)
	elif base == 'c':
		freq *= 2**(3/12)
	elif base == 'd':
		freq *= 2**(5/12)
	elif base == 'e':
		freq *= 2**(7/12)
	elif base == 'f':
		freq *= 2**(8/12)
	elif base == 'g':
		freq *= 2**(10/12)

	# Change the pitch of the note based on what octave it is ('clef' is a misnomer btw)
	cptr += 1
	if note[cptr] in 'ei':
		# Flat/Sharp loop
		if note[cptr] == 'i' and note[cptr + 1] == 's': # Sharp
			freq *= 2**(1/12)
		elif note[cptr] == 'e' and note[cptr + 1] == 's': # Flat
			freq *= 2**(-1/12)
		else:
			raise ValueError('Invalid character(s): %s' % (note[:cptr+1]))
		cptr += 2
	clef = int(note[cptr])
	freq = freq * 2**(clef - 4)

	cptr += 1
	duration = int(note[cptr])	# Duration of the note (log 2)
	dot = 1				# Dotted note calculation
	cptr += 1
	if len(note) == 4 or len(note) == 6:
		if note[cptr] == '.':
			dot = 1.5
		else:
			raise ValueError('Invalid character: %s<-' % note)

	# Number of samples (effectively the length (in samples) of the clip)
	n_samples = int(lib.samplerate * dot * 60/(bpm * 2**(duration - 2)))
	clip = lib.Clip.from_function(function(freq), n_samples)
	if fadein or fadeout:
		clip = effects.fade(int(n_samples * fadein), int(n_samples * fadeout))(clip)
	return clip
