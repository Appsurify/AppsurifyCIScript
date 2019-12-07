# Script to run Sahi tests with Appsurify

# inputs
# list of tests with format testsuitename#testname,
# i.e. #teststorun = "ddcsv_dd_csv#test9.sah,ddcsv_dd_csv#test10.sah,sahi_demo_sah#sahi_demo.sah,demo_suite#getwin_popupWithParam.sah"

# Questions/TODO's
#should we get the first line comment?

# query to get which tests to run
# Can get - <testsuite name="ddcsv_dd_csv" tests="3" failures="3" errors="0" time="24.051">
# <testcase classname="ddcsv_dd_csv.test9" name="test9.sah" time="17.982">
# normal suite <?xml version="1.0" encoding="UTF-8"?><testsuite name="demo_suite" tests="138" failures="23" errors="0" time="2322.014">
# <testcase classname="demo_suite.204" name="204.sah" time="4.615"></testcase>
# single test
#<?xml version="1.0" encoding="UTF-8"?><testsuite name="sahi_demo_sah" tests="1" failures="0" errors="0" time="14.008">
#	<testcase classname="sahi_demo_sah.sahi_demo" name="sahi_demo.sah" time="9.967"></testcase></testsuite>
# find file before the . in classname
# open that file and find the row with test9.sah
# copy that row to new file

import csv
import os
import sys


teststorun = sys.argv[1]
datarows = []
tests = teststorun.split(",")
print(tests)
standalonetests = []
suitetests = []
datatests = []
rows = []
standalonerows = []

def find(name):
    currentdir = os.getcwd() # using current dir, could change this to work with full computer search
    for root, dirs, files in os.walk(currentdir):
        if name in files:
            return os.path.join(os.path.relpath(root, currentdir), name) # for relative path
            #return os.path.join(root, name) # for full path - could also change the main search to search all folders


if os.path.exists("temp.dd.csv"):
    os.remove("temp.dd.csv")
if os.path.exists("temp.suite"):
    os.remove("temp.suite")

for test in tests:
    testsuitename = test[0:(test.find("#"))]
    testsuitename=testsuitename.replace("_",".")
    testname=test[(test.find("#"))+1:]
    if testsuitename[-4:] == ".sah":
        standalonetests.append(testname)
    if testsuitename[-4:] == ".csv":
        datatests.append(test)
    if testsuitename[-6:] == ".suite":
        suitetests.append(test)

print("printing standalone then data then suite")
print(standalonetests)
print(datatests)
print(suitetests)
print("printed sets")

for test in suitetests:
    print(test)

    testsuitename = test[0:(test.find("#"))]
    testsuitename=testsuitename.replace("_",".")
    testname=test[(test.find("#"))+1:]
    print(testname)
    print(testsuitename)

    f=open(testsuitename, "r")
    fl =f.readlines()
    for line in fl:
        #print(line)
        if testname in line:
            values = line.split()
            for i, value in enumerate(values):
                if testname in value:
                    values[i] = find(testname)

            print(values)
            row = " ".join(values)
            print(row)
            standalonerows.append(row)
            print('Found {}'.format(row))

print(standalonerows)

f= open("temp.suite","w+")
for row in standalonerows:
    f.write(row + '\n')

print(standalonetests)
for test in standalonetests:
    f.write(find(test) + '\n')

f.close()


for test in datatests:
    print(test)
    testsuitename = test[0:(test.find("#"))]
    testsuitename=testsuitename.replace("_",".")
    testname=test[(test.find("#"))+1:]
    print(testname)
    print(testsuitename)

    with open(testsuitename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            #print(row)
            if testname in row:
                print ('Found: {}'.format(row))
                for i, column in enumerate(row):
                    if testname in column:
                        row[i] = find(testname)
                rows.append(row)


with open('temp.dd.csv', 'w') as outf:
    writer = csv.writer(outf)
    for row in rows:
        writer.writerow(row)
    tempsuite = ["temp.suite"]
    writer.writerow(tempsuite)
