# Script to run Katalon tests with Appsurify

# inputs
# link to test suite with all tests
# will create copy of testsuite with all tests called temp.ts
# list of tests with format testname,
# i.e. #teststorun = "Test Cases/New Test Case 2, Test Cases/New Test Case"

import csv
import os
from shutil import copyfile
import sys
from xml.etree.ElementTree import ElementTree

#Copy xml file with all tests
# Source path 
source = sys.argv[1]

full_path = os.path.realpath(source)
  
# Destination path 
destination = os.path.join(os.path.dirname(full_path),"temp.ts")

print(destination)
copyfile(source, destination)

#remove tests not in test list
teststorun = sys.argv[2]
testlist = teststorun.split(',')

tree = ElementTree()
tree.parse(destination)
    
root = tree.getroot()
for test in root.findall('testCaseLink'):
    testids = test.findall('testCaseId')
    for testid in testids:
        print(testid.text)
        if testid.text not in testlist:
            root.remove(test)

tree.write(destination)
testtemplatearg2 = "C:\\Katalon\\Test\\Test Project\\Test Project.prj"
testtemplatearg3 = "Test Suites/New Test Suite"
testtemplatearg1 = "c:\\katalon\\test.xml"
testtemplatearg4 = "fgsdfgsdfg"

testseparator=","
reporttype="file"
full_path = os.path.realpath(testtemplatearg2)
report = testtemplatearg1
head_tail = os.path.split(testtemplatearg1) 
report_folder = head_tail[0]
report_file = head_tail[1]
# Destination path 
destination = os.path.join(os.path.dirname(full_path),"temp.ts")
os.path.join(testtemplatearg2, testtemplatearg3)
head_tail = os.path.split(testtemplatearg3) 
startrunspecific="katalonc -noSplash -runMode=console -projectPath='" + testtemplatearg2 + "' -testSuitePath='" + "'" + os.path.join(head_tail[0], "temp.ts") + "' -apiKey='" + testtemplatearg4 +"' -reportFolder='" + report_folder + " -reportFileName='" + report_file + "'"
startrunall="katalonc -noSplash -runMode=console -projectPath='" + testtemplatearg2 + "' -testSuitePath='" + "'" + testtemplatearg3 + "' -apiKey='" + testtemplatearg4 +"' -reportFolder='" + report_folder + " -reportFileName='" + report_file + "'"
generatefile="katalon"
print(startrunspecific)