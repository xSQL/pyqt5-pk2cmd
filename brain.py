#filename = 'test.hex'
#with open(filename, 'rb') as f:
#    content = f.readlines()
#
#for l in content:
#    line = l[1:-1]
#
#    data = line[8:]
#
#    chars = ' '.join([data[i:i+2] for i in range(0, len(data), 2)])
#
#    print('%s:%s  %s'%(line[2:6], line[6:8], chars))

a = 256

def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'little')

print(int_to_bytes(a))
