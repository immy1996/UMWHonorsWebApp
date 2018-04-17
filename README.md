# [UMW Honors Program Web Application](https://honorsprogram.herokuapp.com)

## Client

Ms. Jeanne Campbell, Email: jcampbe2@umw.edu

## Project Background

The UMW Honors Program Web Application is a replacement for the current system that
is being used by the Honors Program. The honors students information are currently only
accessible by visiting the physical location of the Honors Program office on the
Fredericksburg Campus of the University of Mary Washington.

The Web Application must allow students from anywhere with internet access to be
able to view their program check sheet. It shall allow the students who are a part of the
UMW Honors Program to view their progress per semester and see what requirements
they have satisfied. The honors students shall be able to view announcements that are
posted by the Honors Program administrator which allows the administrators to keep in
touch with the students and up to date of any news from the Honors Program.

The administrators for the Honors Web Application shall be able to post
announcements. Both administrators and students must be able to change their
passwords and view the announcements. Administrators must be able to upload a CSV file
for a particular student and it must update the student’s information. This should
automatically create accounts for new students and update accounts for continuing
students. Administrators must be able to access all of the student information by searching
for them.

## Installation Instruction

### Start with
sudo apt-get update
<br />
<br />
sudo apt-get upgrade

### Packages
sudo easy_install flask markdown
<br />
<br />
sudo apt-get install python-setuptools 
<br />
<br />
sudo apt-get install postgresql 
<br />
<br />
sudo apt-get install python-psycopg2

## For PostgreSQL
### First time logging in PostgreSQL
sudo sudo -u postgres psql

### Setting password in postgres
\password (The password you want it to be)

<br />
### Importing the SQL file
cd "directory with sql file"
sudo psql -U postgres -h localhost
\i server.sql

<b>Created by Imran Ahmed, Shane McSally, and Luke Payne</b>