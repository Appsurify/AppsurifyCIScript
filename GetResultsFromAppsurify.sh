#get results
finalRes=`curl --header "token: $apiKey" "$url/api/external/output/?${run_id}" ` ; echo $finalRes
new_defects=`echo $finalRes | sed 's/\\\\\//\//g' | sed 's/[{}]//g' |tr "," "\n" | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' |  grep -w new_defects ` ; echo $new_defects
reopened_defects=`echo $finalRes | sed 's/\\\\\//\//g' | sed 's/[{}]//g' |tr "," "\n" | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' |  grep -w reopened_defects ` ; echo $reopened_defects
flaky_defects=`echo $finalRes | sed 's/\\\\\//\//g' | sed 's/[{}]//g' |tr "," "\n" | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' |  grep -w flaky_defects ` ; echo $flaky_defects
reopened_flaky_defects=`echo $finalRes | sed 's/\\\\\//\//g' | sed 's/[{}]//g' |tr "," "\n" | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' |  grep -w reopened_flaky_defects ` ; echo $reopened_flaky_defects
flaky_failures_breaks=`echo $finalRes | sed 's/\\\\\//\//g' | sed 's/[{}]//g' |tr "," "\n" | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' |  grep -w flaky_failures_breaks ` ; echo $flaky_failures_breaks
failed_test=`echo $finalRes | sed 's/\\\\\//\//g' | sed 's/[{}]//g' |tr "," "\n" | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' |  grep -w new_defects ` ; echo $failed_test
broken_test=`echo $finalRes | sed 's/\\\\\//\//g' | sed 's/[{}]//g' |tr "," "\n" | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' |  grep -w new_defects ` ; echo $broken_test

failnew="false"
failreopened="false"
failnewflaky="false"
failreopenflaky="false"
failflakytests="false"
failfailedtests='false'
failbrokentests="false"

#newdefects, reopeneddefects, flakybrokentests, newflaky, reopenedflaky, failedtests, brokentests

#alternative substring https://unix.stackexchange.com/questions/370889/test-if-a-string-contains-a-substring

if [[ $fail == *newdefects* ]] ; then failnew="true" ; fi
if [[ $fail == *reopeneddefects* ]] ; then failreopened="true" ; fi
if [[ $fail == *flakybrokentests* ]] ; then failflakytests="true" ; fi
if [[ $fail == *newflaky* ]] ; then failnewflaky="true" ; fi
if [[ $fail == *reopenedflaky* ]] ; then failreopenflaky="true" ; fi
if [[ $fail == *failedtests* ]] ; then failfailedtests="true" ; fi
if [[ $fail == *brokentests* ]] ; then failbrokentests="true" ; fi

#echo $failnew
#echo $failreopened
#echo $failflakytests
#echo $failnewflaky
#echo $failreopenflaky
#echo $failfailedtests
#echo $failbrokentests

if [[ $new_defects != "new_defects:0" && $failnew != "false" ]] ; then exit 1 ; fi
if [[ $reopened_defects != "reopened_defects:0" && $failreopened != "false" ]] ; then exit 1 ; fi
if [[ $flaky_defects != "flaky_defects:0" && $failnewflaky != "false" ]] ; then exit 1 ; fi
if [[ $reopened_flaky_defects != "reopened_flaky_defects:0" && $failreopenflaky != "false" ]] ; then exit 1 ; fi
if [[ $flaky_failures_breaks != "flaky_failures_breaks:0" && $failflakytests != "false" ]] ; then exit 1 ; fi
if [[ $failed_test != "failed_test:0" && $failfailedtests != "false" ]] ; then exit 1 ; fi
if [[ $broken_test != "broken_test:0" && $failbrokentests != "false" ]] ; then exit 1 ; fi