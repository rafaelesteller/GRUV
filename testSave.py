#test for reading in song and getting certain time blocks
from data_utils.parse_files import *

#testing that bit rate can be use to set length
data, bitrate = read_wav_as_np("datasets/YourMusicLibrary/OnlineSongs.wav")
print bitrate
timeS = 15
write_np_as_wav(data[:int(bitrate*timeS)], bitrate,  "testLen.wav")

#testing using fft blocks of varying sizes
blockTime = .2
n = 4410
block_size = int(bitrate * blockTime)
blocks = convert_np_audio_to_sample_blocks(data, block_size)
print 'block shape: ' + str(blocks[0].shape)
fftBlocks = time_blocks_to_fft_blocks(blocks, n=n)
print 'fft block shape: ' + str(fftBlocks[0].shape)
timeBlock = fft_blocks_to_time_blocks(fftBlocks)
print 'back shape: ' + str(timeBlock[0].shape)
data = convert_sample_blocks_to_np_audio(timeBlock)
write_np_as_wav(data[:int(bitrate*timeS)], int(bitrate * .75),  "testLenFft.wav")

