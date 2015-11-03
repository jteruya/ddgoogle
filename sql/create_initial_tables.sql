-- Create Schema
create schema google;

-- Create Table
create table google.session_notes_pageview_counts (
        pagepath varchar
      , date date
      , hour int
      , minute int
      , pageviews int);
