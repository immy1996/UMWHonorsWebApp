CREATE DATABASE honors_program;
\c honors_program;

CREATE TABLE user_info
(
   userid varchar(25) NOT NULL PRIMARY KEY,
   password varchar(25) NOT NULL,
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





	

	
	