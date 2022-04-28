See - https://github.com/Appsurify/AppsurifyTestScript

# Appsurify Script Installation

## Index
- [Installation Instructions](#install)
- [Available Arguments](#available_arguments)
  - [Required Arguments](#required_arguments)
  - [Recommended Arguments](#recommended_arguments)
- [Tests To Run](#teststorun)
- [Example Usage](#example_usage)
- [Additional Arguments](#additional_arguments)
  - [Build Failure Arguments](#build_failure_arguments)


## <a id="install"></a>Installation Instructions

### Requirements

Python 3.6+

### Installation Command

pip install appsurifyci --upgrade

## <a id="available_arguments"></a>Available Arguments
 
### <a id="required_arguments"></a>Required Arguments 

| argument | options |
| --- | --- |
| apikey | Apikey from appsurify |
| url | Url of the appsurify instance i.e. "https://dummy.appsurify.com"|
| project | Name of the project |
| testsuite | Name of the testsuite |
| branch | Name of the branch the tests are running against |
| commit | SHA of the commit |

### <a id="recommended_arguments"></a>Recommended Arguments
| argument | options |
| --- | --- |
| runtemplate  | Options - all tests, no tests (used just to push results from the prior command), prioritized tests (requires --percentage argument to be added and the percentage of tests to be run.  See [below](#teststorun) for details |
| testtemplate | Options - mvn, cucumber mvn, sahi testrunner, sahi ant, testim, mocha, pytest, rspec, robotframework, cyprus, mstest, vstest, katalon, opentest.  For additional integrations talk to the Appsurify team |
| runcommand | Command to execute tests in the target environment, if command is custom to your test suite |
| report | Location of xml reports created by the test run if this is not the default location for the test type |


## <a id="teststorun"></a>Parameter Details - Tests Execution  

| Option | Details |
| --- | --- |
| all tests | Will run all tests.  Will fail on any failure.  Recommended for nightly or weekly test executions |
| no tests | Will run no tests.  Will fail on any failure.  Recommended when starting with Appsurify to just upload data |
| prioritized tests | Requires the percentage argument.  Will only fail the build on new/reopened defects.  Recommended for your most frequent run type |


## <a id="example_usage"></a>Example Usage

runtestswithappsurify --url "https://dummy.appsurify.com" --apikey "apikeyvalue" --project "Test" --testsuite "Test" --runtemplate "prioritized tests" --testtemplate "mvn" --percentage "20"

## <a id="additional_arguments"></a>Additional Arguments - For Customization

| argument | default | options/details |
| --- | --- | --- |
| fail | newdefects, reopeneddefects | options newdefects, reopeneddefects, flakybrokentests, newflaky, reopenedflaky, failedtests, brokentests |
| rerun | "false" | whether failed tests should be rerun |
| maxrerun | 3 | the number of times failed tests should be rerun |
| failfast | "false" | whether after each set of test runs to determine if the build has failed (tests will still be rerun if this has been selected) |
| executioncommand | "" | Command to be executed following completion of the script [[teststorun]] will be replaced with the formatted list of tests to run |
| percentage | "" | Percentage of tests to be run if prioritized tests is selected in the runtemplate |

For CI specific integrations please contact Appsurify

