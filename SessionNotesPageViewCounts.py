"""A simple example of how to access the Google Analytics API."""

import argparse

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

from sys import argv
import csv

def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
  """Get a service that communicates to a Google API.

  Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.

  Returns:
    A service that is connected to the specified API.
  """

  f = open(key_file_location, 'rb')
  key = f.read()
  f.close()

  credentials = SignedJwtAssertionCredentials(service_account_email, key,
    scope=scope)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service


def get_results(service, profile_id, startdate, enddate):
 
  # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions within the past seven days.
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=startdate,
      end_date=enddate,
      metrics='ga:pageviews',
      dimensions='ga:pagePath, ga:date, ga:hour, ga:minute',
      sort='-ga:pageviews',
      max_results=10000).execute()
  #return 1 

def print_data_table(results):
  # Print headers.
  output = []
  for header in results.get('columnHeaders'):
    output.append('%30s' % header.get('name'))
  print ''.join(output)

  # Print rows.
  if results.get('rows', []):
    for row in results.get('rows'):
      output = []
      for cell in row:
        output.append('%30s' % cell)
      print ''.join(output)
  else:
    print 'No Results Found'

def print_results(results, startdate, enddate):
  """Prints out the results.

  This prints out the profile name, the column headers, and all the rows of
  data.

  Args:
    results: The response returned from the Core Reporting API.
  """

  print()
  print('Profile Name: %s' % results.get('profileInfo').get('profileName'))
  print()

  # Open a file.
  filepath = '/home/jteruya/google/csv/'     #change this to your actual file path
  filename = 'pageview'         #change this to your actual file name
  f = open(filepath + '/' + filename + '_' + startdate + '.csv', 'wt')

  # Wrap file with a csv.writer
  writer = csv.writer(f, lineterminator='\n')
  
  # Write header.
  header = [h['name'][3:] for h in results.get('columnHeaders')] #this takes the column headers and gets rid of ga: prefix
  writer.writerow(header)
  print(''.join('%30s' %h for h in header))

  # Write data table.
  if results.get('rows', []):
    for row in results.get('rows'):
      writer.writerow(row)
      print(''.join('%30s' %r for r in row))
    
  else:
    print ('No Rows Found')

  # Close the file.
  f.close()


def main():
  # Get Start and End Dates
  startdate=argv[1]
  enddate=argv[2] 
 
  # View ID
  profile='97407136'

  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly'] 

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
  service_account_email = '230482720110-lht3ditrnuhjr7sh3eesm40bv0r6u1l4@developer.gserviceaccount.com'
  key_file_location = '/home/jteruya/google/auth/client_secrets.key.pem'

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
  
  print_results(get_results(service, profile, startdate, enddate), startdate, enddate)

if __name__ == '__main__':
  main()
