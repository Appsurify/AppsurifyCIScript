#!/bin/bash -x
if [[ $reporttype == "directory" && $importtype != "trx" ]] ; then
    for fileName in `ls -1 $report*.xml`
        do
            echo "call api for $fileName" ''
            import=""
            if [[ $repository == "git" ]] ; then
                import=`curl -X POST "$url/api/external/import/" -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' -H "token: $apiKey" -F "file=@$fileName" -F 'project_name'="$project" -F 'test_suite_name'="$testsuite" -F 'type'=$importtype -F 'commit'=$commitId`
            ; fi
            if [[ $repository != "git" ]] ; then
                import=`curl -X POST "$url/api/external/import/" -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' -H "token: $apiKey" -F "file=@$fileName" -F 'project_name'="$project" -F 'test_suite_name'="$testsuite" -F 'type'=$importtype -F 'commit'=$commitId  -F 'repo'=$repository`
            ; fi
            echo $import
            #get testrun id
            var=`echo $import | sed 's/\\\\\//\//g' | sed 's/[{}]//g' |tr "," "\n" | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' |  sed '10p;d' `
            echo $var
            if [[ $run_id == "" ]] ; then run_id=`echo $var | sed 's/test_run_id:/test_run\=/g' ` ; fi
            #print testrun name
            echo $run_id
        done ; fi

if [[ $reporttype == "directory" && $importtype == "trx" ]] ; then
    for fileName in `ls -1 $report*.trx`
        do
            echo "call api for $fileName" ''
            import=""
            if [[ $repository == "git" ]] ; then
                import=`curl -X POST "$url/api/external/import/" -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' -H "token: $apiKey" -F "file=@$fileName" -F 'project_name'="$project" -F 'test_suite_name'="$testsuite" -F 'type'=$importtype -F 'commit'=$commitId`
            ; fi
            if [[ $repository != "git" ]] ; then
                import=`curl -X POST "$url/api/external/import/" -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' -H "token: $apiKey" -F "file=@$fileName" -F 'project_name'="$project" -F 'test_suite_name'="$testsuite" -F 'type'=$importtype -F 'commit'=$commitId  -F 'repo'=$repository`
            ; fi
            echo $import
            #get testrun id
            var=`echo $import | sed 's/\\\\\//\//g' | sed 's/[{}]//g' |tr "," "\n" | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' |  sed '10p;d' `
            echo $var
            if [[ $run_id == "" ]] ; then run_id=`echo $var | sed 's/test_run_id:/test_run\=/g' ` ; fi
            #print testrun name
            echo $run_id
        done ; fi

if [[ $reporttype == "file" ]] ; then
    import=""
    if [[ $repository == "git" ]] ; then
        import=`curl -X POST "$url/api/external/import/" -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' -H "token: $apiKey" -F "file=@$fileName" -F 'project_name'="$project" -F 'test_suite_name'="$testsuite" -F 'type'=$importtype -F 'commit'=$commitId`
    ; fi
    if [[ $repository != "git" ]] ; then
        import=`curl -X POST "$url/api/external/import/" -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' -H "token: $apiKey" -F "file=@$fileName" -F 'project_name'="$project" -F 'test_suite_name'="$testsuite" -F 'type'=$importtype -F 'commit'=$commitId  -F 'repo'=$repository`
    ; fi
    echo $import
    #get testrun id
    var=`echo $import | sed 's/\\\\\//\//g' | sed 's/[{}]//g' |tr "," "\n" | sed 's/\"\:\"/\|/g' | sed 's/[\,]/ /g' | sed 's/\"//g' |  sed '10p;d' `
    echo $var
    if [[ $run_id == "" ]] ; then run_id=`echo $var | sed 's/test_run_id:/test_run\=/g' ` ; fi
    #print testrun name
    echo $run_id ; fi