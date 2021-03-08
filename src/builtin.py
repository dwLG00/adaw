import math
from src import lib
import numpy as np

def db_to_magnitude(db):
	return 10**(db/20)



def sin(db, frequency, phase=0):
	return lambda x: db_to_magnitude(db) * 32767 * math.sin((2*math.pi)*(x*frequency/lib.samplerate + phase))

def sin_lr(db, frequency, id):
	f = sin(db, frequency)
	return lambda x: (f(x), f(x))

def wavetable_lr(sample):
	if isinstance(sample, lib.Clip):
		return lambda x: sample.sample_l[x % len(sample)], sample.sample_r[x % len(sample)]
	return None
