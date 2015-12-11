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

drop table if exists google.cms_pageview_counts;
create table google.cms_pageview_counts (
        pagepath varchar
      , device_category varchar
      , global_user_id varchar
      , previous_pagepath varchar
      , date date
      , hour int
      , pageviews int);
