import time
from StepParser import *

start = time.time()
a = parse_file('bolt.ifc')
# print(a)
print('parsed in ', time.time() - start)