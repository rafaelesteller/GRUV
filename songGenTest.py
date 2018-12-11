from gen_utils import seed_generator as g
a = g.generate_from_file(filename="datasets/YourMusicLibrary/OnlineSongs.wav",
                         seed_length = 1,
                         block_size = 11025, 
                         seq_len = 40, 
                         std = .2, 
                         mean = .1)
print a.shape
print type(a)
