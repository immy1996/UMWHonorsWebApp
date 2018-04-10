DROP DATABASE honors_program;

CREATE DATABASE honors_program;

\c honors_program;

-- add extension
CREATE EXTENSION pgcrypto;

CREATE TABLE user_info
(
   userid varchar(25) NOT NULL PRIMARY KEY,
   password varchar(5000) NOT NULL,
   isadmin varchar(1) NOT NULL
);

CREATE TABLE announcements
(
   postid serial NOT NULL PRIMARY KEY,
   announcement_title varchar(100),
   announcement_text varchar(500),
   post_date date
);

CREATE TABLE student_info
(
   lastname varchar(45),
   firstname varchar(45),
   id integer,
   email varchar(75),
   admitted_date varchar(45),
   dupont_code varchar(45),
   student_status varchar(45),
   comments varchar(45),
   term varchar(45),
   co_cur_1 varchar(100),
   date_1 varchar(45),
   fsem_hn varchar(45),
   fsem_date varchar(45),
   hn_course_1 varchar(45),
   hn_course_1_date varchar(45),
   hn_course_2 varchar(45),
   hn_course_2_date varchar(45),
   hn_course_3 varchar(45),
   hn_course_3_date varchar(45),
   hn_course_4 varchar(45),
   hn_course_4_date varchar(45),
   hn_course_5 varchar(45),
   hn_course_5_date varchar(45),
   research_course varchar(45),
   research_course_date varchar(45),
   capstone_course varchar(45),
   capstone_course_date varchar(45),
   honr_201 varchar(45),
   honr_201_date varchar(45),
   leadership varchar(45),
   mentoring varchar(45),
   gpa_fall_year_1 integer,
   gpa_spring_year_1 integer,
   gpa_fall_year_2 integer,
   gpa_spring_year_2 integer,
   gpa_fall_year_3 integer,
   gpa_spring_year_3 integer,
   gpa_fall_year_4 integer,
   gpa_spring_year_4 integer,
   honr_portfolio_1 varchar(45),
   honr_portfolio_2 varchar(45),
   honr_portfolio_3 varchar(45),
   honr_portfolio_4 varchar(45),
   exit_interview varchar(45)
);

DROP ROLE umwhonors;
CREATE ROLE umwhonors WITH LOGIN;
ALTER ROLE umwhonors WITH PASSWORD 'umw';

GRANT ALL ON user_info, announcements, student_info TO umwhonors;

GRANT USAGE, SELECT ON SEQUENCE announcements_postid_seq TO umwhonors;

INSERT into user_info values ('Adam', 'password', 'y');
INSERT into user_info values ('Jack', 'password', 'n');