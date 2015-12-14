# Ericsson ECR. All right reserved.
# IMEI_LAC_parser.py v1.0 by eromgor&epavser
#This script parse SGSN-MME list_subscribers command output and provide number of IMEI-TACs and UE models in needed LACs  

import os

# Open output files and assign variables
os.listdir('.')
output_lac_imei= open ('output_lac_imei.txt', 'w')
output_count_imei= open ('output_count_imei.txt', 'w')
output_imei_tac_model= open ('output_imei_tac_model.txt', 'w')
input_lac = open ('lacs.txt')
imei_tac_raw = open ('IMEI_TAC_raw.txt')
lac_imei = list()
imei_count = dict()
lac_rac_cgi = str()
imei_tac_list = list()
model = list()
t = tuple()
count = 0

# Open files list_subscribers output files one by one in specified directory
for file in (os.listdir('./list_subs')):
    fn = os.path.join(".\list_subs",file)
    print fn
    input = open(fn)

# For each line in file, skip lines without IMEI or LAC, extract IMEI TAC and LAC from line and create list of tuples LAC - IMEI TAC, print result to file output_lac_imei.txt
    for line in input:
        words = line.split()

        if line.startswith('25020') and words[9] != '?' and words[2] != '?' : 


            lac_rac_cgi = words[9]
            lac_rac_cgi = words[9].split('-')
            lac = lac_rac_cgi[2]
            imei_tac = str(words[2][:8])
            line_out = str(lac) +  ' ' + str(imei_tac) + '\n'
            output_lac_imei.write(line_out)
            t = (lac, imei_tac)
            lac_imei.append(t)



output_lac_imei.close()

# For all LACs in file lacs.txt find LAC in list LAC -IMEI TAC and count all IMEI TACs corresponding to that LAC. Outpu is dictionary key = IMEI TAC, value = number of IMEI TACs in LAC

for line in input_lac:
    words = line.split()
    for lac,imei in lac_imei:
        if lac == words[0]: 
            if imei not in imei_count:
                imei_count[imei] = 1
            else:
                imei_count[imei] += 1

# Create  sorted list of tuples where key = number of IMEI TACs in LAC, value = IMEI TAC

l = list()

for key, val in imei_count.items():
    l.append((val, key))
l.sort(reverse=True)


# Create output string and write it to file output_count_imei.txt

for key, val in l: 
    line_out = str(key) +  ' ' + str(val) + '\n'
    output_count_imei.write(line_out)
    #print key,val

output_count_imei.close()

# parse IMEI-Model database and extract IMEI TAC from it, create list of IMEI TACs and list of  UE models

for line in imei_tac_raw:
    words = line.split("\t")
    imei_tac_list.append(words[0])
    model.append(str(words[1:]))

# In sorted list of tuples where key = number of IMEI TACs in LAC, value = IMEI TAC, find all IMEI TACs exist in IMEI-Model database and create output string

for key, val in l:
    for n in imei_tac_list:
        if val == n:
            line_out = str(key) +  '\t ' + str(val) + '\t' + str(model[imei_tac_list.index(n)]) +  '\n'
            output_imei_tac_model.write(line_out)

output_imei_tac_model.close()

















