import keras

def img_encoder():
    '''
    input is 4d tensor, outer dimension is time dimension
    '''
    m = keras.models.Sequential()
    m.add(keras.layers.Conv2D(filters=3, kernel_size=5))
    m.add(keras.layers.MaxPool2D())
    m.add(keras.layers.Conv2D(filters=5, kernel_size=3))
    m.add(keras.layers.MaxPool2D())
    m.add(keras.layers.Conv2D(filters=5, kernel_size=3))
    m.add(keras.layers.MaxPool2D())
    m.add(keras.layers.Conv2D(filters=7, kernel_size=3))
    m.add(keras.layers.MaxPool2D())
    m.add(keras.layers.Conv2D(filters=10, kernel_size=3))
    m.add(keras.layers.MaxPool2D())
    m.add(keras.layers.Flatten())
    return m

def seq_encoder(num_keys, seq_len, h_dim):
    m = keras.models.Sequential()
    embedding = keras.layers.Embedding(input_dim=num_keys, output_dim=h_dim, input_length=seq_len)
    m.add(embedding)
    m.add(keras.layers.LSTM(10, return_sequences=False))
    return m



def get_seq_model(num_keys=50, seq_len=45, h_dim=50, frames=10,):

    channel1_input_shape = (None, 480, 640, 3)
    channel2_input_shape = (None, seq_len, )
    channel1_seq_input = keras.layers.Input(channel1_input_shape)
    channel2_seq_input = keras.layers.Input(channel2_input_shape)
    i_enc = img_encoder()
    s_enc = seq_encoder(num_keys,seq_len,h_dim)

    channel1 = keras.layers.TimeDistributed(i_enc)(channel1_seq_input)
    channel1 = keras.layers.LSTM(h_dim, return_sequences=False)(channel1)
    channel2 = keras.layers.TimeDistributed(s_enc)(channel2_seq_input)
    channel2 = keras.layers.LSTM(h_dim, return_sequences=False)(channel2)

    combined = keras.layers.Concatenate()([channel1, channel2])
    combined = keras.layers.RepeatVector(seq_len)(combined)
    output = keras.layers.TimeDistributed(keras.layers.Dense(num_keys))(combined)
    model = keras.models.Model(inputs=[channel1_seq_input, channel2_seq_input], outputs=[output])
    model.compile(loss=keras.losses.sparse_categorical_crossentropy, optimizer=keras.optimizers.Adam())
    # frame =
    # r_n =  np.random.uniform(0, 1, combined_input_shape)
    # m = encoder(num_keys, seq_len, h_dim, channel1_input_shape)
    return model


