import keras


# each frame has two channels
# conv channel
channel1_input_shape = (640,480,3)
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
num_keys = 50
seq_len = 100
h_dim = 10
channel2_input_shape = (seq_len,)
channel2_input = keras.layers.Input((channel2_input_shape))
embedding = keras.layers.Embedding(input_dim=num_keys, output_dim=h_dim, input_length=seq_len)(channel2_input)
channel_2 = keras.layers.LSTM(10, return_sequences=False)(embedding)

combined = keras.layers.Concatenate()([channel1, channel_2])

# model = keras.models.Model(inputs=channel1_input, outputs=channel1)
# model.summary()
# model2 = keras.models.Model(inputs=channel2_input, outputs=channel_2)
# model2.summary()

model2 = keras.models.Model(inputs=[channel1_input, channel2_input], outputs=combined)
model2.summary()
