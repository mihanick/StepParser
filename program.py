import time
from StepParser import *
import yaml

start = time.time()
a = parse_file('bolt.ifc')

print('parsed in ', time.time() - start)

start = time.time()
a = pool_parse_file('bolt.ifc')

print('parsed parallel in ', time.time() - start)

#with open('test3.yaml','w') as file:
#    for aa in a:
#       docs = yaml.dump(aa, file)
