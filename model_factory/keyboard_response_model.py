# from model_arch.multi_channel import ops_model
import keyboard


# need a hashing to hash keyboard keys to int
# use dict to map inx and key token

multifier = 2 # down and up

reserved_keyspace = 128 * multifier

print(dir(keyboard))
print(keyboard.KeyboardEvent.name)