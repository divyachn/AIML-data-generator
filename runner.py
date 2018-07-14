import sys
import re
from Aiml_Generator import Aiml_Generator

read_file = sys.argv[1]
write_file = sys.argv[2]

rf = open(read_file, 'r')
wf = open(write_file, 'w')

aiml = Aiml_Generator()

line = rf.readline()
line_number = 0

while line:
    line_number += 1
    # Remove the leading and trailing spaces.
    line = line.strip()
    if len(line)==0:
        # If it's an empty line then discard it.
        pass
    elif line[0] == ';':
        # Write the data to .aiml file
        #aiml.print_categories()
        write_data = aiml.combine()
        wf.write(write_data)
    else:
        aiml.classify_line(line.strip(), line_number)
    line = rf.readline()
    
rf.close()
wf.close()
