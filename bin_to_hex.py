
key_file = open("key.bin", "rb")
data = key_file.read()
formatted_hex_value=hex(int(data, 2))
hex_value=formatted_hex_value.split('x')
byte_array=bytes.fromhex(hex_value[1])
fixed_key_bytes=byte_array[0:13]