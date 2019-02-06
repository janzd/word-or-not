import os
import numpy as np
from sklearn.model_selection import train_test_split

from keras.layers import Dense
from keras.optimizers import Adam
from keras.losses import binary_crossentropy
from keras.metrics import binary_accuracy
from keras.callbacks import ModelCheckpoint

from models import simple_model
from utils import read_words, create_result_subdir, convert_to_char_seq, pad_words
from config import *


def train():
    result_subdir = create_result_subdir(result_dir)
    real_words = read_words(real_words_path)
    fake_words = read_words(fake_words_path)
    real_words = [word for word in [convert_to_char_seq(word) for word in real_words] if word != []]
    fake_words = [word for word in [convert_to_char_seq(word) for word in fake_words] if word != []]
    words = real_words + fake_words
    words = pad_words(words)
    words = np.array(words)[:, :, np.newaxis]
    print(words.shape)
    labels = np.concatenate([np.ones(len(real_words)), np.zeros(len(fake_words))])
    words_train, words_val, labels_train, labels_val = train_test_split(words, labels, test_size=0.2, random_state=42)

    model = simple_model()
    opt = Adam(0.01)
    model.compile(loss=binary_crossentropy, optimizer=opt, metrics=[binary_accuracy])
    model.summary()

    checkpoint = ModelCheckpoint(os.path.join(result_subdir, 'model.{epoch:03d}-{val_loss:.2f}.h5'), monitor='val_loss')

    model.fit(words_train, labels_train, batch_size=32, epochs=10, verbose=1, validation_data=(words_val, labels_val), callbacks=[])


train()