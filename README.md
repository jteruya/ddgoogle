# google

Google Analytics Initial API Setup Process:

Google Developer Console (https://console.developers.google.com/project):
1.) Created a new project: DD Data Platform
2.) On the main menu (left hand menu):
       - APIs & auth -> Credentials
3.) On the "Credentials" main page:
       - “Add credentials” -> Service Account -> P12 Key Type -> Create -> Note the Service Email (“230482720110-lht3ditrnuhjr7sh3eesm40bv0r6u1l4@developer.gserviceaccount.com”) displayed on your screen.          It will be used later. 
4.) After completing 3.) a .p12 key is downloaded to your computer.  Note the password ("notasecret") displayed on your screen when this occurs.  It will be used later.
5.) On the main menu left hand menu):
       - APIs & auth -> API
6.) On the main page:
       - Use the text box "Search all 100+ APIs" to search for "Analytics" -> Click on "Analytics API"
7.) On the "Analytics API" main page
       - Click "Enable API"

Google Analytics (https://www.google.com/analytics/web/?hl=en#report/content-pages/a47831496w93537502p97407136/):
1.) Asked Julia Graham for “Manage Users” permissions to our Google Analytics account.  This allows us to add/delete users to the account which will be required for the next step.
2.) On the main menu (top bar):
       - Admin 
3.) On the main page:
       - Under the "Account" column -> "User Management" -> Use the text box with the label "Add permission for:" and add the service email account with "Read & Analyze" permissions.

DD Batman (10.223.176.157) Development Environment:
1.) Created a "google" project on Batman.
2.) Installed the following python libraries: google-api-python-client, pyopenssl, pycrypto
       - su - datadawgs (sudo into the datadawgs user)
       - sudo pip install — upgrade [library name] (install/upgrade the library)
3.) Create a .pem Certificate File
       - openssl pkcs12 -in client_secrets.p12 -out client_secrets.crt.pem -clcerts -nokeys (asks for password from above) 
4.) Create a .pem Key File 
       - openssl pkcs12 -in client_secrets.p12 -out client_secrets.key.pem -nocerts -nodes (asks for password from above) 


NOTE: As of 5/10/2016, the code to pull from GA is now using the datadawg's generic email account: dd.product.analytics@gmail.com

The following information is associated with this gmail account and should be used as opposed to the info in the instructions above:
Service Email: dd-google-analytics-service-ac@dd-data-platform-1307.iam.gserviceaccount.com
Auth Files: DD_Data_Platform* 

Additionally, because there were changes to the corresponding python modules the following version need to be set in the environment that this script is run:

oauth2client: 1.5.1
google-api-python-client: 1.4.2
pycrypto: 2.6.1

To install these specific versions use the following commands:
sudo pip install oauth2client==1.5.1
sudo pip install google-api-python-client==1.4.2
sudo pip install pycrypto==2.6.1

You can check these versions with the following commands:
pip show oauth2client | grep Version
pip show google-api-python-client | grep Version
pip show pycrypto | grep Version