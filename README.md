# Subscription Migration - API Helper Scripts

This is a project to assist customers in the case where they need to move a subscription from one 
platform to another.  If you intend to use this code you should seek guidance from your Technical Account Manager
and a Qualys Security Solutions Architect.  Subscription migrations are a very complicated issue and should not be
entered into without consultation.

The code and documentation stored in this project are provided as-is and without any warranty. Qualys technical support 
does not support the contents of the code provided here.  This code is provided as a reference for customers wishing to
use the API to help drive their migration between Qualys subscriptions.   

Each automatable aspect of migration covered by these scripts has two associated files - a processor and a test script.
The processor handles the task of data gathering from the source subscription, transformation of that data (where 
necessary) into 'create' requests, and the submission of those requests to the target subscription.

Various parts of the migration process have interdependencies.  For example, you must create scanner appliances in the new subscription before Scan Schedules are created.
Similarly you cannot create Asset Groups without the IP addresses being added to the subscription.  The main test 
script (test.py) demonstrates the correct order of execution for the scripts.

Each test script has a 'simulate' mode (activated with the '-s' argument to the script) which will read in the source
data but will not make the subsequent API calls to write the data to the target subscription.  Instead, the 
intended API calls are printed to the console.
