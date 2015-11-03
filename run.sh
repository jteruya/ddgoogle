#!/bin/bash

# Inital Script Variables
base="$HOME/google"

# Archive CSV Files
#if [ -f "$base/csv/*.csv" ];
#then 
#  mv $base/csv/*.csv $base/csv/archive/
#fi

# Robin Connection 
robin='psql -h 10.223.192.6 -p 5432 -A -t analytics etl'

# Get Start Date from Session Notes Table
start_date=`$robin -c "select coalesce(max(date),'2015-01-01') from google.session_notes_pageview_counts"` 
start_date=`date -d "$start_date" +'%Y-%m-%d'`

# Get End Date 
end_date=`date +'%Y-%m-%d'`
echo $end_date

# Delete Incomplete Data
$robin -c "delete from google.session_notes_pageview_counts where date >= '${start_date}'"

increment_date=`date -d "${start_date}" +'%Y-%m-%d'`

while [[ "$increment_date" < "$end_date" ]] || [[ "$increment_date" == "$end_date" ]];
do
   # Establish CSV File Name
   land="$base/csv/pageview_${increment_date}.csv"
   
   # Pull from Google Analytics into CSV
   python $base/SessionNotesPageViewCounts.py $increment_date $increment_date

   # Push CSV into Robin
   $robin -c "\COPY google.session_notes_pageview_counts FROM '"$land"' DELIMITER ',' CSV HEADER;"

   increment_date=`date -d "$increment_date 1 day" +"%Y-%m-%d"` 
done

