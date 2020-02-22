#!/bin/bash
#
#
# Script combines given JUnit XML files into one.
#
# Script assumes that file begins with XML header.
# Script will copy content between <testsuite> tags
# to new file with XML header and <testsuites> tags.
# Script will not affect original files, but it will
# overwrite output file contents. Script searches all
# *.xml files from input directory.
#
# -h         - Help
# -i [DIR]   - Input directory
# -o [FILE]  - Output file
#
# Author: Jarno Tuovinen <jarno.tuovinen@bitbar.com>
#
# License: MIT
#

INPUTDIR=""
OUTPUTFILE=""

# arg 1 = input file
function striphead() {
    sed 1,$(expr $(grep -m1 -n "<testsuite" $1 | cut -f1 -d:) - 1)d $1
}

function error() {
    echo "ERROR: $*"
    exit -1
}

function help() {
    echo "$0"
    echo "HELP:"
    echo -e "\t-h\tHelp"
    echo -e "\t-i\tInput dir [mandatory]"
    echo -e "\t-o\tOutput file [mandatory]"
    exit 0
}

# Handle parameters
while getopts "hi:o:" opt; do
    case $opt in
    h) help ;;
    i) INPUTDIR="$OPTARG" ;;
    o) OUTPUTFILE="$OPTARG" ;;
    \?) error ;;
    esac
done

# Input dir must be given
if [[ -z ${INPUTDIR} ]]; then
    error "Input dir not given"
fi

# Output file must be given
if [[ -z ${OUTPUTFILE} ]]; then
    error "Output file not given"
fi

echo '<?xml version="1.0" encoding="UTF-8"?>' > ${OUTPUTFILE}
echo '<testsuites>' >> ${OUTPUTFILE}
for f in ${INPUTDIR}/*.xml
do
    echo $(striphead ${f}) >> ${OUTPUTFILE}
done

echo '</testsuites>' >> ${OUTPUTFILE}
