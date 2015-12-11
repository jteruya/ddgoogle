#!/usr/bin/python

from datetime import datetime
from datetime import timedelta
import time
import argparse
import re
import subprocess
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


def get_results(service, profile_id, startdate, enddate, metricsparam, dimensionsparam, sortparam, filterparam, maxresultsparam):

  # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions within the past seven days.

  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=startdate,
      end_date=enddate,
      metrics=metricsparam,
      dimensions=dimensionsparam,
      sort=sortparam,
      filters=filterparam,
      max_results=maxresultsparam).execute()

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

def print_results(results, filepath, filename):
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
  f = open(filepath + '/' + filename, 'wt') 

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

  # Initial Variables
  currentpath = '/home/jteruya/google/'
  csvpath = currentpath + 'csv/' 
  currentdate = time.strftime("%Y-%m-%d")
  pg_connect = 'psql -h 10.223.192.6 -p 5432 -A -t analytics etl'  
 
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly'] 

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
  service_account_email = '230482720110-lht3ditrnuhjr7sh3eesm40bv0r6u1l4@developer.gserviceaccount.com'
  key_file_location = '/home/jteruya/google/auth/client_secrets.key.pem'

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
  
  # Initialize counter.  
  i = 0
 
  # Open parameter file and process each line (except the header line).
  with open('googleAnalyticsQueries.parameters', 'rb') as f:
     for line in f:
        # Don't read in header record. 
        if i > 0:
           # Read in a line from parameter file.
           split_line = line.split("\n",1)[0].split("|",8)
           
           # Split the line into different parameters.   
           schema_name = split_line[0]
           db_table_name = split_line[1]
           profile_id = split_line[2]
           metrics_param = split_line[3]
           dimension_param = split_line[4]
           sort_param = split_line[5]
           filter_param = split_line[6]
           max_results_param = int(split_line[7])

           # Get the max date (start date for google analytics pul) for the data in the db table.
           startdate = subprocess.check_output(pg_connect + ' -c "select coalesce(max(date),\'2015-01-01\') from ' + schema_name + '.' + db_table_name + '"', shell = True).split("\n",1)[0]

           # Delete all data from the db table that is associated with the max date.
           subprocess.call(pg_connect + ' -c "delete from ' + schema_name + '.' + db_table_name + ' where date >= \'' + startdate + '\'"', shell = True) 

           # Convert startdate and currentdate from string to datetime type. 
           startdatetime = datetime.strptime(startdate, '%Y-%m-%d')
           currentdatetime = datetime.strptime(currentdate, '%Y-%m-%d') 
           
           # Loop through all of the days between start date and current date. 
           while startdatetime <= currentdatetime: 
              # Create string version of current date 
              iterate_date = startdatetime.strftime('%Y-%m-%d')
               
              # Output File Name 
              output_file = split_line[8].split(".",1)[0] + '_' + iterate_date + '.csv'
              
              # Pull the results for the current date and print to the csv file. 
              print_results(get_results(service, profile_id, iterate_date, iterate_date, metrics_param, dimension_param, sort_param, filter_param, max_results_param), csvpath, output_file) 
             
              # Load CSV into the db table.
              subprocess.call(pg_connect + ' -c "\\copy ' + schema_name + '.' + db_table_name + ' from \'' + csvpath + output_file + '\' delimiter \',\' csv header"', shell = True) 
 
              # Iterate the current date by one day 
              startdatetime = startdatetime + timedelta(days=1) 

        # Increment Counter
        i = i + 1
 
   
if __name__ == '__main__':
  main()
