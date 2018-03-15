DROP DATABASE honors_program;

CREATE DATABASE honors_program;

\c honors_program;

CREATE TABLE user_info
(
   userid varchar(25) NOT NULL PRIMARY KEY,
   password varchar(5000) NOT NULL,
   isadmin varchar(1) NOT NULL
);

CREATE TABLE announcements
(
   postid serial NOT NULL PRIMARY KEY,
   announcement varchar(500),
   post_date date
);

CREATE TABLE student_info
(
   lastname varchar(45),
   firstname varchar(45),
   id integer,
   email varchar(45),
   admitted_date date,
   dupont_code integer,
   student_status varchar(45),
   term varchar(45),
   co_cur_1 varchar(45),
   date_1 date,
   fsem_hn varchar(45),
   fsem_date date,
   hn_course_1 varchar(45),
   hn_course_1_date date,
   hn_course_2 varchar(45),
   hn_course_2_date date,
   hn_course_3 varchar(45),
   hn_course_3_date date,
   hn_course_4 varchar(45),
   hn_course_4_date date
);

DROP ROLE umwhonors;
CREATE ROLE umwhonors WITH LOGIN;
ALTER ROLE umwhonors WITH PASSWORD 'umw';

GRANT ALL ON user_info, announcements, student_info TO umwhonors;


INSERT into user_info values ('Adam', 'password', 'y');
INSERT into user_info values ('Jack', 'password', 'n');