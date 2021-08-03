from tensorflow.keras.layers import Embedding, Flatten, Dense, LSTM, Bidirectional, Dropout, BatchNormalization, GRU, Conv1D, GlobalAveragePooling1D, GlobalMaxPooling1D
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

import tensorflow as tf
import pickle 
from joblib import load
from feature_extraction import Extractor
import numpy as np 

class ConvModel(tf.keras.Model):
  embedding_vector_length = 128
  maxlen = 128
  max_words = 20000
  
  def __init__(self, tokenizer_name):
    super(ConvModel, self).__init__()
    #model
    self.tokenizer = None # token
    num_chars = self.load_tokenizer(tokenizer_name)
    
    self.embedding_layers = tf.keras.layers.Embedding(num_chars, ConvModel.embedding_vector_length, input_length=ConvModel.maxlen)
    self.conv = tf.keras.layers.Conv1D(256, 4, activation='relu')
    self.fc1 = tf.keras.layers.Dense(128, activation = "relu")
    self.fc = tf.keras.layers.Dense(1, activation = "sigmoid")
    
  def load_tokenizer(self, file):
    with open(file, 'rb') as handle:
        tokenizer = pickle.load(handle)
    num_chars = len(tokenizer.word_index)+1
    self.tokenizer = tokenizer 
    return num_chars
  
  def load_model(self, save_weights):
    self.built = True
    self.load_weights(save_weights) 
  
  def preprocess_url(self, url):
    url = url.strip()
    sequences = self.tokenizer.texts_to_sequences([url])
    word_index = self.tokenizer.word_index
    url_prepped = pad_sequences(sequences, maxlen=ConvModel.maxlen)
    return url_prepped
  
  def call(self, inputs, training=False):
    embedding = self.embedding_layers(inputs)
    conv = self.conv(embedding)
    conv_max = tf.reduce_max(conv, axis = 1)
    fc1 = self.fc1(conv_max)
    output = self.fc(fc1)
    return output
  
  def predict(self, url):
    process_url = self.preprocess_url(url)
    return self(process_url)
  
  def decode(self, output):
    pass
