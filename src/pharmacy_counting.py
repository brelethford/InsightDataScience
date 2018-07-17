#!/usr/bin/bash

###############
# PREPERATION #
###############

indata = 'itcont.txt'
outdata = 'top_cost_drug.txt' 
dec = False
print("Rounding to nearest whole dollar amount: {}".format(not dec))

### Define input / output folders relative to cwd (Note - this only works when run from 'run.sh' in the base folder)
input_dir = './input/'
output_dir = './output/'
infile = input_dir+indata
outfile = output_dir+outdata

### Load the input data file and separate the classes of information
print('Grabbing data from {}...'.format(infile))
input_file = open(infile,'r')
rawdata = [line.strip('\n').split(',') for line in  input_file.readlines()]
header = rawdata[0]
ID, last, first, drugs, cost = [list(i) for i in zip(*rawdata[1:])]

### Convert ID and cost into numbers 
ID = map(int,ID)
cost = map(float,cost)

### Recreate an array with all relevant information, sort by drug type
data = sorted(zip(drugs,ID,cost))

#############
# AGGREGATE # 
#############

### Iterate over the variables, summing cost for all drugs over unique perscibers. From the information given, it seems that there are no repeats for a particular ID/drug, so we don't need to consider unique entries for zip(ID,drug). This means we can simply count the number of times a drug appears in the data, and sum the corresponding cost.

output=[]

### The following loop assumes an output for sumcost that is rounded to the nearest integer, based on test1 output.

for d in list(set(drugs)):
  print('Collecting records related to {}...'.format(d))
  drugmask = [drug==d for drug in drugs]
  drugtype = d
  number = sum(drugmask)
  subcost = [c*d for c,d in zip(cost,drugmask)]
  if dec:
    sumcost = sum(subcost)
  else:
    sumcost = int(round(sum(subcost)))
  output.append((drugtype,number,sumcost))

print('Collection finished.')

##########
# OUTPUT #
##########

### Sorting happens first by reversed sumcost, then by drug in alphebetical order

output = sorted(output,key=lambda x: (-x[2],x[1]))

### Open a file to store things in, then write the drugs (in order of greatest cost) to file
print('Printing results to {}...'.format(outfile))

text_file = open(outfile, "w")

### Write the headers first
text_file.write('drug_name,num_prescriber,total_cost\n')

### Write output of each line
for entry in output:
  if dec:
    text_file.write('{0:s},{1:d},{2:.2f}\n'.format(entry[0],entry[1],entry[2]))
  else: 
    text_file.write('{0:s},{1:d},{2:d}\n'.format(entry[0],entry[1],entry[2]))

text_file.close()
print('End program.')
