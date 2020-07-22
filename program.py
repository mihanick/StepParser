import time
from StepParser import *
import yaml

start = time.time()
a = parse_file('DC_Riverside_Bldg-LOD_300.ifc')

print('parsed in ', time.time() - start)

with open('DC_Riverside_Bldg-LOD_300.yaml','w') as file:
    for aa in a:
       docs = yaml.dump(aa, file)
