import keras

def ops_model(num_keys, seq_len, h_dim, channel1_input_shape=(640,480,3)):
    # each frame has two channels
    # conv channel
    channel1_input = keras.layers.Input(channel1_input_shape)
    channel1 = keras.layers.Conv2D(filters=3, kernel_size=5)(channel1_input)
    channel1 = keras.layers.MaxPool2D()(channel1)
    channel1 = keras.layers.Conv2D(filters=5, kernel_size=3)(channel1)
    channel1 = keras.layers.MaxPool2D()(channel1)
    channel1 = keras.layers.Conv2D(filters=5, kernel_size=3)(channel1)
    channel1 = keras.layers.MaxPool2D()(channel1)
    channel1 = keras.layers.Conv2D(filters=7, kernel_size=3)(channel1)
    channel1 = keras.layers.MaxPool2D()(channel1)
    channel1 = keras.layers.Conv2D(filters=10, kernel_size=3)(channel1)
    channel1 = keras.layers.MaxPool2D()(channel1)
    channel1 = keras.layers.Flatten()(channel1)
    # lstm channel
    channel2_input_shape = (seq_len,)
    channel2_input = keras.layers.Input((channel2_input_shape))
    embedding = keras.layers.Embedding(input_dim=num_keys, output_dim=h_dim, input_length=seq_len)(channel2_input)
    channel_2 = keras.layers.LSTM(10, return_sequences=False)(embedding)
    combined = keras.layers.Concatenate()([channel1, channel_2])
    combined = keras.layers.RepeatVector(seq_len)(combined)
    projected_out = keras.layers.LSTM(num_keys, return_sequences=True)(combined)
    model = keras.models.Model(inputs=[channel1_input, channel2_input], outputs=projected_out)
    model.compile(loss=keras.losses.CategoricalCrossentropy,optimizer=keras.optimizers.Adagrad)
    model.summary()
    return model

if __name__ == "__main__":
    # test toy model
    num_keys = 50
    seq_len = 50
    h_dim = 10
    channel1_input_shape = (640, 480, 3)
    m = ops_model(num_keys,seq_len, h_dim,channel1_input_shape)