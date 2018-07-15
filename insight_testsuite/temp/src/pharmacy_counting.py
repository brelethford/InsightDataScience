#!/usr/bin/env python

############
# PREAMBLE #
############

### Import Libraries
import numpy as np
import argparse, os

#############
# ARGUMENTS #
#############

p = argparse.ArgumentParser(description="Aggregates drug prescription data to yield top drug costs",
                            formatter_class=argparse.RawTextHelpFormatter)
p.add_argument("--indata", default="itcont.txt", type=str,
                help="Name of datafile used for aggregation")
p.add_argument("--outdata", default="top_cost_drug.txt", type=str,
                help="Name of output txt file")
p.add_argument("--dec", dest='dec', action='store_true',
                help="Toggles total drug cost to be float (decimals) instead of int")


args = p.parse_args()
indata = args.indata
outdata = args.outdata 
dec = args.dec
print(dec)
print("Rounding to nearest whole dollar amount: {}".format(not dec))

###############
# PREPERATION #
###############

### Define input / output folders relative to pwd (Note - this only works when run from 'run.sh' in the base folder)
base_dir = os.getcwd()
input_dir = base_dir + '/input/'
output_dir = base_dir + '/output/'
infile = input_dir+indata
outfile = output_dir+outdata

### Load the input data file and separate the classes of information
print('Grabbing data from {}...'.format(infile))
rawdata = np.genfromtxt(input_dir+indata, dtype=str, delimiter=',')
header = rawdata[0]
ID, last, first, drug, cost = rawdata[1:].T

### Convert ID and cost into numbers 
ID = ID.astype(int)
cost = cost.astype(float)

### Recreate an array with all relevant information, sort by drug type
data = sorted(zip(drug,ID,cost))

#############
# AGGREGATE # 
#############

### Iterate over the variables, summing cost for all drugs over unique perscibers. From the information given, it seems that there are no repeats for a particular ID/drug, so we don't need to consider unique entries for zip(ID,drug). This means we can simply count the number of times a drug appears in the data, and sum the corresponding cost.

output=[]

### The following loop assumes an output for sumcost that is rounded to the nearest integer, based on test1 output

for d in np.unique(drug):
  print('Collecting records related to {}...'.format(d))
  drugmask = [drug==d][0]
  drugtype = d
  number = np.count_nonzero(drugmask)
  if dec:
    sumcost = sum(cost[drugmask])
  else:
    sumcost = int(np.round(sum(cost[drugmask])))
  output.append((sumcost,drugtype,number))

print('Collection finished.')

##########
# OUTPUT #
##########

### Sorting is simple if the sumcost comes first

output.sort(reverse=True)

### Open a file to store things in, then write the drugs (in order of greatest cost) to file
print('Printing results to {}...'.format(outfile))

text_file = open(outfile, "w")

### Write the headers first
text_file.write('drug_name,num_prescriber,total_cost\n')

### Write output of each line
for entry in output:
  if dec:
    text_file.write('{0:s},{1:d},{2:.2f}\n'.format(entry[1],entry[2],entry[0]))
  else: 
    text_file.write('{0:s},{1:d},{2:d}\n'.format(entry[1],entry[2],entry[0]))

text_file.close()
print('End program.')
