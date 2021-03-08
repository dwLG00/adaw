from src import lily
from src import lib
from src import builtin
from src import effects

def tuple_add(*args):
	a, b = 0, 0
	for tup in args:
		a += tup[0]
		b += tup[1]
	return (a, b)

def instrument1(v):
	component1 = builtin.sin_lr(-6, v, 'instrument1-1')
	component2 = builtin.sin_lr(-12, v * 2, 'instrument1-2')
	component3 = builtin.sin_lr(-18, v * 2**(19/12), 'instrument1-3')
	component4 = builtin.sin_lr(-24, v * 4, 'instrument1-4')
	return lambda x: tuple_add(component1(x), component2(x), component3(x), component4(x))

def instrument2(v):
	component1 = builtin.sin_lr(-12, v, 'instrument2-1')
	component2 = builtin.sin_lr(-21, v * 3, 'instrument2-2')
	component3 = builtin.sin_lr(-40, v * 5, 'instrument2-3')
	return lambda x: tuple_add(component1(x), component2(x), component3(x))

melody = '''	a43 b43 cis43 b44 a44 b44 a44 gis34 b44 e32
		cis43 d43 e43 d44 cis44 b41
		fis33 gis33 a44 b44 cis44 b44 cis43 d43 b42
		e43 d44 cis44 b43 cis43 a41'''

base = '''	a32 e22 b32 e22
		cis32 a32 b32 e22
		fis22 cis22 b22 e22
		b32 e22 a31'''

melody_clip = lily.load(melody, bpm=100, instrument=instrument1)
#decay_clip = effects.delay(5, decay=0.1)(melody_clip)
base_clip = lily.load(base, bpm=100, instrument=instrument2)
project = lib.Project("my-first-daw.wav")
project.add_clip(melody_clip)
#project.add_clip(decay_clip)
project.add_clip(base_clip)
project.export(debug=True)
