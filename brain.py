filename = 'test.hex'
with open(filename, 'rb') as f:
    content = f.readlines()

for l in content:
    line = l[1:-1]

    data = line[8:]

    chars = ' '.join([data[i:i+2] for i in range(0, len(data), 2)])

    print('%s:%s  %s'%(line[2:6], line[6:8], chars))
