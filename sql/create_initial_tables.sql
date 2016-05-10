-- Create Schema
create schema google;

-- Create Table
drop table if exists google.session_notes_pageview_counts;
create table google.session_notes_pageview_counts (
        pagepath varchar
      , date date
      , hour int
      , minute int
      , pageviews int);

drop table if exists google.ep_user_device_counts;
create table google.ep_user_device_counts (
     global_user_id varchar
   , device_category varchar
   , date date
   , hour_of_day int
   , total_pageviews int
   , total_events int );

drop table if exists google.ep_pageview_counts;
create table google.ep_pageview_counts (
     global_user_id varchar
   , page_path varchar
   , date date
   , hour_of_day int
   , total_pageviews int );

drop table if exists google.ep_event_counts;
create table google.ep_event_counts (
     global_user_id varchar
   , event_category varchar
   , event_label varchar
   , event_action varchar
   , date date
   , hour_of_day int
   , minute_of_hour int
   , total_events int );

drop table if exists google.ep_event_nolabel_counts;
create table google.ep_event_nolabel_counts (
     global_user_id varchar
   , event_category varchar
   , event_action varchar
   , date date
   , hour_of_day int
   , minute_of_hour int
   , total_events int );

drop table if exists google.ep_app_event_counts;
create table google.ep_app_event_counts (
     application_id varchar
   , global_user_id varchar
   , event_category varchar
   , event_label varchar
   , event_action varchar
   , date date
   , hour_of_day int
   , total_events int);
   
drop table if exists google.ep_app_pageview_counts;
create table google.ep_app_pageview_counts (
     application_id varchar
   , global_user_id varchar
   , page_path varchar
   , date date
   , hour_of_day int
   , total_pageviews int);

drop table if exists google.ep_app_event_nolabel_counts;
create table google.ep_app_event_nolabel_counts (
     application_id varchar
   , global_user_id varchar
   , event_category varchar
   , event_action varchar
   , date date
   , hour_of_day int
   , total_events int );

drop table if exists google.ep_pageview_survey;
create table google.ep_pageview_survey (
     global_user_id varchar
   , page_path varchar
   , survey_id int
   , date date
   , hour_of_day int
   , total_pageviews int);
   
drop table if exists google.ep_pageview_survey_item;
create table google.ep_pageview_survey_item (
     global_user_id varchar
   , page_path varchar
   , survey_id int
   , item_id int
   , date date
   , hour_of_day int
   , total_pageviews int);

drop table if exists google.ep_app_pageview_survey;
create table google.ep_app_pageview_survey (
     application_id varchar
   , global_user_id varchar
   , page_path varchar
   , survey_id int
   , date date
   , hour_of_day int
   , total_pageviews int);
   
drop table if exists google.ep_app_pageview_survey_item;
create table google.ep_app_pageview_survey_item (
     application_id varchar
   , global_user_id varchar
   , page_path varchar
   , survey_id int
   , item_id int
   , date date
   , hour_of_day int
   , total_pageviews int);
