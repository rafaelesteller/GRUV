import numpy as np
import sys
sys.path.append("../")
from data_utils.parse_files import *

#A very simple seed generator
#Copies a random example's first seed_length sequences as input to the generation algorithm
def generate_copy_seed_sequence(seed_length, training_data):
	num_examples = training_data.shape[0]
	example_len = training_data.shape[1]
	randIdx = 109 #np.random.randint(num_examples, size=1)[0]
	randSeed = np.concatenate(tuple([training_data[randIdx + i] for i in xrange(seed_length)]), axis=0)
	seedSeq = np.reshape(randSeed, (1, randSeed.shape[0], randSeed.shape[1]))
	return seedSeq

def generate_from_file(filename, seed_length, block_size, seq_len, std, mean, fft= False, offsetSec = 0):
  data, bitrate = read_wav_as_np(filename)
  data=data[(bitrate*offsetSec):]
  blocks = convert_np_audio_to_sample_blocks(data, block_size)
  if fft:
    blocks = time_blocks_to_fft_blocks(blocks)
  chunks_X = []
  total_seq = len(blocks)
  cur_seq = 0
  print seq_len
  while cur_seq +  seq_len < total_seq:
    chunks_X.append(blocks[cur_seq:cur_seq+seq_len])
    cur_seq+= seq_len
  block_size = block_size * 2 if fft else block_size
  out_shape = (len(chunks_X), seq_len, block_size)
  
  x_data = np.zeros(out_shape)
  for n in xrange(len(chunks_X)):
    for i in xrange(seq_len):
      x_data[n][i] = chunks_X[n][i]
  print x_data.shape
  x_data[:][:] -= mean
  x_data[:][:] /= std
  
  return generate_seed_sequence(seed_length, x_data)

def generate_seed_sequence(seed_length, training_data, offset = 0):
  return training_data[offset:seed_length]

  

