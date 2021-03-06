from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import os
import nn_utils.network_utils as network_utils
import gen_utils.seed_generator as seed_generator
import gen_utils.sequence_generator as sequence_generator
from data_utils.parse_files import *
import config.nn_config as nn_config


def gen(folder, actF, fft, inputSongs):
  config = nn_config.get_neural_net_configuration()
  nn = "TOYPAJ-NPWeights50-"


  model_filename = folder + nn + actF
  actF = actF + "moid" if actF == "sig" else actF
  sample_frequency = config['sampling_frequency']
  inputFile = folder + "TOYPAYJ-Processed"

  output_filename = folder + actF + 'generated_'



  #Load up the training data
  print ('Loading training data')
  #X_train is a tensor of size (num_train_examples, num_timesteps, num_frequency_dims)
  #y_train is a tensor of size (num_train_examples, num_timesteps, num_frequency_dims)
  #X_mean is a matrix of size (num_frequency_dims,) containing the mean for each frequency dimension
  #X_var is a matrix of size (num_frequency_dims,) containing the variance for each frequency dimension
  X_train = np.load(inputFile + '_x.npy')
  print( X_train.shape)
  print( type(X_train))
  y_train = np.load(inputFile + '_y.npy')
  X_mean = np.load(inputFile + '_mean.npy')
  X_var = np.load(inputFile + '_var.npy')
  print ('Finished loading training data')

  #Figure out how many frequencies we have in the data
  freq_space_dims = X_train.shape[1:]
  hidden_dims = config['hidden_dimension_size']

  #Creates a lstm network
  model = network_utils.create_lstm_network(num_frequency_dimensions=freq_space_dims, num_hidden_dimensions=hidden_dims, actF = actF)
  #You could also substitute this with a RNN or GRU
  #model = network_utils.create_gru_network()
  print( model_filename)
  #Load existing weights if available
  if os.path.isfile(model_filename):
	  model.load_weights(model_filename)
  else:
	  print('Model filename ' + model_filename + ' could not be found!')

  
  print ('Starting generation!')
  #Here's the interesting part
  #We need to create some seed sequence for the algorithm to start with
  #Currently, we just grab an existing seed sequence from our training data and use that
  #However, this will generally produce verbatum copies of the original songs
  #In a sense, choosing good seed sequences = how you get interesting compositions
  #There are many, many ways we can pick these seed sequences such as taking linear combinations of certain songs
  #We could even provide a uniformly random sequence, but that is highly unlikely to produce good results
  seed_len = 1
  block_size = X_train.shape[2] / 2 if fft else X_train.shape[2]

  for song in inputSongs:
    name = song[song.rfind('/') + 1:]
    print( name)
    """
    seed_seq = seed_generator.generate_from_file(
                             filename=song,
                             seed_length = 1,
                             block_size = block_size, 
                             seq_len = 40, 
                             std = X_var,
                             mean = X_mean,
                             fft = fft,
                             offsetSec = 53)
    """
    seed_seq = seed_generator.generate_copy_seed_sequence(1, X_train)
    print(seed_seq.shape)
    max_seq_len = 6; #Defines how long the final song is. Total song length in samples = max_seq_len * example_len
    output = []
    for i in xrange(seed_seq.shape[1]):
				      output.append(seed_seq[0][i].copy())
				
    save_generated_example(folder + "input_3" + name, output, sample_frequency=sample_frequency, useTimeDomain=not fft)
    
    output = sequence_generator.generate_from_seed(model=model, seed=seed_seq, sequence_length=max_seq_len,
	    data_variance=X_var, data_mean=X_mean)

    print( len(output))
    print ('Finished generation!')

    #Save the generated sequence to a WAV file
    save_generated_example(output_filename + "3" + name, output, sample_frequency=sample_frequency, useTimeDomain=not fft)

folders = ["FD-eigth", "FD-half", "FD-quart", "TD-eigth", "TD-half"]
folders = [ "FD-quart"]
folders = ["./datasets/" + f for f in folders]
fft = False
actFs = [ "tanh"]

inputSongs = [#"datasets/YourMusicLibrary/OnlineSongs.wav",
              "datasets/YourMusicLibrary/toypaj/AnthemPt2.wav"]


              
for folder in folders:
  for actF in actFs:
    print(folder)
    print(folder[folder.rfind('/') + 1:][:2] == 'FD')
    gen(folder + "/", actF, folder[folder.rfind('/') + 1:][:2] == 'FD', inputSongs)

