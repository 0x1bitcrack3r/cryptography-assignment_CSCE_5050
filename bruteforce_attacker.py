import time
import threading
from utils_demo import *
from Cryptodome.Cipher import AES
from base64 import b64encode, b64decode

#intializing the values
number_of_keys = 0
key_found = None
key_available = threading.Event()
key_space=24
bytes_length=3

# Reading the first 13 bytes from the generated key
key_file = open("key.bin", "rb")
data = key_file.read()
formatted_hex_value=hex(int(data, 2))
hex_value=formatted_hex_value.split('x')
byte_array=bytes.fromhex(hex_value[1])
fixed_key_bytes=byte_array[0:13]
fixed_key_pad = bytearray(fixed_key_bytes)

# Performing the bruteforce attack
def key_finder(message,cipher,nonce):
    global number_of_keys
    #mentioned key space limited to 24 bits and the range will be 2^n-1 where i starts from 0.
    for i in range(2**key_space-1):
        #generating the key with first 13 bytes and random key pad
        generated_key = fixed_key_pad + i.to_bytes(bytes_length,byteorder='big')
        #using the generated key to decrypt the cipher to obtain the message
        message_bytes = decryptor_CTR(cipher, nonce, generated_key)
        if string_to_bytes(message) == message_bytes:
            key_found = "Key for message: "+message+"\n"+"key: "+generated_key.hex()
            print(key_found)
        number_of_keys = i

def bruteforce_for_keys():
    for n in range(1,4):
        try:
            #reading the data from the files iteratively
            message = read_file("m"+str(n)+".txt")
            cipher_bytes = read_bytes("c"+str(n)+".bin")
            nonce_bytes = read_bytes("nonce"+str(n)+".bin")
            key_finder(message,cipher_bytes,nonce_bytes)
            key_available.set()
            time.sleep(10)
        except:
            print('')

def main():
    #implemented threading to execute the tasks one after the other
    thread = threading.Thread(target=bruteforce_for_keys)
    thread.start()
    while not key_available.wait(timeout=5):
        print('\r{} keys searched...'.format(number_of_keys), end='', flush=True)
    print('\r{} keys searched...'.format(number_of_keys))

if __name__ == '__main__':
    main()