from keras.layers import Dense, LSTM, Input, Masking
from keras.models import Model

def simple_model():
    inputs = Input(shape=(None, 1))
    masked = Masking()(inputs)
    lstm1 = LSTM(128, return_sequences=True)(masked)
    lstm2 = LSTM(128)(lstm1)
    output = Dense(1, activation='sigmoid')(lstm2)
    model = Model(inputs=inputs, outputs=output)
    return model