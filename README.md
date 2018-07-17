# Table of Contents
1. [Approach](README.md#approach)
2. [Instructions](README.md#instructions)

# Approach

To solve the problem of outputting a list of the top drug costs for a list of supplier/drug combinations, the script 'pharmacy_counting.py' is split up into segments:

Preamble: imports necessary libraries  
Arguments: establishes optional arguments for input file name, output file name, and whether or not to round the total cost to the nearest dollar for each drug  
Preparation: defines directories, inputs data, puts in a usable form for later manipulation  
Aggregate: uses a masked array for each drug to pull the number of suppliers and total drug cost for that drug  
Output: sorts results based on total cost per drug with a tie break alphabetically, then exports by writing each drug to a txt file  

One assumption was made with this approach: that the input file would resemble the test data provided to us. Specifically, this script requires each prescriber to be listed only once for each drug type. In order to account for one prescriber having multiple instances of the same drug applied to them, some additional information would need to be known (if the price is always the same, if a redundant line of data should be counted in the total cost, etc.)

# Instructions

The script 'pharmacy_counting.py' works on the assumption that the files used are in the proper place (i.e. input files in the input folder). If either the input or output file name needs to be changed, or if the person running the script decides they want an output that is not rounded to the nearest dollar, the script can be run with the optional arguments:  

--indata, --outdata, --dec  

from terminal. Likewise, the script 'run.sh' can be edited to change these options as well.
