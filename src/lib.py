import numpy as np
import struct

samplerate = 44100

class Project:
	def __init__(self, name: str, bitrate=16, samplerate=44100):
		self.name = name
		self.clips = []
		self.bitrate = bitrate
		self.samplerate = samplerate


	def add_clip(self, clip, startpos=0):
		self.clips.append((clip, startpos))

	def commulative(self):
		set = False
		for clip, pos in self.clips:
			if not set:
				sample_l = numpy_shift(clip.sample_l, pos, clip.sample_l.size + pos)
				sample_r = numpy_shift(clip.sample_r, pos, clip.sample_r.size + pos)
				set = True
			else:
				sample_l = add_numpy_array(sample_l, 0, clip.sample_l, pos)
				sample_r = add_numpy_array(sample_r, 0, clip.sample_r, pos)
		return (sample_l, sample_r)

	def export(self, fname=None, debug=True, dither=False):
		if not fname: fname = self.name
		condensed_l, condensed_r = self.commulative()

		# Dither the signal
		if dither:
			dither_array = np.resize([0, 1], condensed.size)
			final_l = np.bitwise_or(condensed_l, dither_array)
			final_r = np.bitwise_or(condensed_r, dither_array)
		else:
			final_l = condensed_l
			final_r = condensed_r

		chunk2_size = final_l.size * 4			# 2 bytes per sample, times 2 channels, times # of samples
		interleave = np.empty((final_l.size + final_r.size,), dtype=np.int16)	# Already little-endian
		interleave[0::2] = final_l
		interleave[1::2] = final_r
		raw_bytes = interleave.tobytes()

		if debug: print('final: %s , %s' % (final_l, final_r))
		if debug: print('raw_bytes preview: %s' % (raw_bytes[:64]))
		with open(fname, 'wb') as f:

			#header
			f.write(b'RIFF')
			f.write(int2bin(chunk2_size + 36, '<L'))
			f.write(b'WAVE')

			f.write(b'fmt\x20')
			f.write(int2bin(16, '<L'))
			f.write(int2bin(1, '<H'))
			f.write(int2bin(2, '<H'))
			f.write(int2bin(samplerate, '<L'))
			f.write(int2bin(samplerate * 4, '<L'))
			f.write(int2bin(4, '<H'))
			f.write(int2bin(16, '<H'))

			f.write(b'data')
			f.write(int2bin(chunk2_size, '<L'))
			f.write(raw_bytes)
		return 0

class Clip:
	def __init__(self, sample_l, sample_r):
		self.sample_l = sample_l
		self.sample_r = sample_r

	def __len__(self):
		if self.sample_l.size == self.sample_r.size:
			return self.sample_l.size
		raise ValueError('left and right channels mismatched')

	def sample(self):
		return self.sample_l, self.sample_r

	@classmethod
	def from_function(cls, func, length):
		sample_l = np.zeros(length, dtype=np.int16)
		sample_r = np.zeros(length, dtype=np.int16)
		for i in range(length):
			sample_l[i], sample_r[i] = func(i)
		return cls(sample_l, sample_r)

	@classmethod
	def from_project(cls, project):
		sample_l, sample_r = project.commulative()
		return cls(sample_l, sample_r)

	@classmethod
	def load_file(cls, filename, debug=False):
		# Only works with wav for now
		with open(filename, 'rb') as f:
			startcode = f.read(4)
			if startcode == b'RIFF':
				endian = 'little'
			elif startcode == b'RIFX':
				endian = 'big'
			else:
				raise TypeError('StartcodeError: %s' % str(startcode))

			if debug: print('Endian: %s' % endian)

			total_size = int.from_bytes(f.read(4), endian)
			assert f.read(4) == b'WAVE'

			# Actually important data
			f.read(4)				#fmt
			f.read(4)				#chunk1 size
			f.read(2)				#format
			n_channels = int.from_bytes(f.read(2), endian)
			sample_rate = int.from_bytes(f.read(4), endian)
			byte_rate = int.from_bytes(f.read(4), endian)
			f.read(2)				#block align, can be infered
			if debug: print('n_channels: %s\nsample_rate: %s\nbyte_rate: %s' %
				(n_channels, sample_rate, byte_rate)
			)

			bitrate = int.from_bytes(f.read(2), endian)
			if bitrate != 16:
				raise TypeError('BitrateError: %s' % str(bitrate))

			f.read(4)				#data
			chunk2_size = int.from_bytes(f.read(4), endian)
			endian_code = '>' if endian == 'big' else '<'
			if debug: print('seekpos: %s' % f.tell())
			raw_data = np.frombuffer(f.read(), dtype=(endian_code+'i2'))
			if debug: print('raw_data: %s' % str(raw_data[:4000]))

		if n_channels == 2:
			left_channel = raw_data[0::2]
			right_channel = raw_data[1::2]
			if debug: print('left: %s\nright: %s' % (str(left_channel[:2000]), str(right_channel[:2000])))
			#final = np.add(left_channel, right_channel, dtype=np.int16) // 2 # Average the two channels together
			final = (left_channel.astype('int16'), right_channel.astype('int16'))
		else:
			left_channel, right_channel = raw_data, raw_data
			final = (left_channel, right_channel)
		return cls(*final)


def numpy_shift(array, shift, size):
	result = np.zeros(size, dtype=array.dtype)
	assert shift >= 0
	result[:shift] = 0
	result[shift:shift+array.size] = array[:]
	return result

def add_numpy_array(a1, shift1, a2, shift2):
	length = max(a1.size + shift1, a2.size + shift2)
	result = np.add(numpy_shift(a1, shift1, length), numpy_shift(a2, shift2, length))
	return result

def int2bin(n, code):
	return struct.pack(code, n)


if __name__ == '__main__':
	pass
