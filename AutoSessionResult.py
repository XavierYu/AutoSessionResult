
# to create a batch progam to read all test results to a result.csv file

# step 1: a) file location
#         b) open filename contain "full", split to get TCID
#         c) Seek 1000 chars from the end, readline until get the target fail_count line
#         d) read fail_count==> result= pass/ fail/ tc empty/ tc incomplete
#         e) write tc_id and pass/fail to result.csv

import sys
import time
import csv
from os import listdir
from os.path import isfile, join

mypath = "."
# listdir return a list in arbitrary order
onlyfiles = sorted( f1 for f1 in listdir(mypath) if 'full' in f1 if isfile(join(mypath,f1)) )

# wb = write binary, to eliminate the blank lines in between when write new results to file
resultWriter = csv.writer(open('./result.csv', 'wb'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)


for item in onlyfiles:

    #---------- Open File--------------
    fullname= join(mypath,item)
    f = open(fullname, 'r')
    temp = item.split('_')
    TCID = int(temp[1])

    # to be improve, read first line "empty" to determine whether file is empty
    if f.readline() == '':
        result = "ERROR:TC EMPTY"
    else:    
        try:
            #f.seek(-50000, 2)			
            targetline= ""
            while "- Result Start -" not in targetline:
                targetline = f.readline()
            fail_count_str_1 = f.readline()
            fail_count_str_2 = f.readline()
            fail_count_str = f.readline()
            print fail_count_str 
            fail_count = int(fail_count_str[-2])  # with newline char at the end as -1
            print fail_count
            print TCID
            print item			

            if fail_count == 0 :
            # write to csv file : Pass
                result = 'Pass'
            else:
            # write to csv file : Fail
                result = 'Fail'
        except IOError:
            result = "ERROR:TC File Incomplete"
            pass

    resultWriter.writerow([TCID,' ',result, item])
    f.close()

time.sleep(2)

