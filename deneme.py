import time

for i in range(100):
    time.sleep(0.1)
    print('Downloading File FooFile.txt [%d%%]\r'%i, end="")