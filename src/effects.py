import numpy as np
import math

from src import lib

def delay(delay_time=lib.samplerate*2, decay=0.5):
	def function(clip):
		l = len(clip)
		delay_t = int(delay_time)

		delay_array_l = lib.numpy_shift(clip.sample_l, delay_t, l + delay_t)
		delay_array_r = lib.numpy_shift(clip.sample_r, delay_t, l + delay_t)
		delay_array_l[:] = delay_array_l[:] * decay
		delay_array_r[:] = delay_array_r[:] * decay

		new_sample_l = np.add(delay_array_l, lib.numpy_shift(clip.sample_l, 0, l + delay_t), dtype=np.int16)
		new_sample_r = np.add(delay_array_r, lib.numpy_shift(clip.sample_r, 0, l + delay_t), dtype=np.int16)
		new_clip = lib.Clip(new_sample_l, new_sample_r)
		return new_clip
	return function

def fadeout(startpos, endpos):
	diff = startpos - endpos
	def function(clip):
		new_sample_l = clip.sample_l[:]
		new_sample_r = clip.sample_r[:]
		for i in range(startpos, endpos):
			coef = 1 + (i - startpos)/(diff)
			new_sample_l[i] = int(new_sample_l[i] * coef)
			new_sample_r[i] = int(new_sample_r[i] * coef)
		return lib.Clip(new_sample_l, new_sample_r)
	return function

def fadein(startpos, endpos):
	diff = endpos - startpos
	def function(clip):
		new_sample_l = clip.sample_l[:]
		new_sample_r = clip.sample_r[:]
		for i in range(startpos, endpos):
			coef = (x - startpos)/diff
			new_sample_l[i] = int(new_sample_l[i] * coef)
			new_sample_r[i] = int(new_sample_r[i] * coef)
		return lib.Clip(new_sample_l, new_sample_r)
	return function

def fade(fadein_end, fadeout_start):
	def function(clip):
		fadeout_end = len(clip)

		new_sample_l = clip.sample_l[:]
		new_sample_r = clip.sample_r[:]
		for i in range(fadein_end):
			coef = i/fadein_end
			new_sample_l[i] = int(new_sample_l[i] * coef)
			new_sample_r[i] = int(new_sample_r[i] * coef)
		diff = fadeout_start - fadeout_end
		for i in range(fadeout_start, fadeout_end):
			coef = 1 + (i - fadeout_start)/diff
			new_sample_l[i] = int(new_sample_l[i] * coef)
			new_sample_r[i] = int(new_sample_r[i] * coef)
		return lib.Clip(new_sample_l, new_sample_r)
	return function
