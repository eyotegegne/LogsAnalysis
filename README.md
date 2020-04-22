# Udacity Full Stack Web Developer Nanodegree -- Logs Analysis Project

## DESCRIPTION
This project is all about gathering some informative reports by querying through multiple tables from a news database. It is interactive command line tool that displays the answer for the below three question based on the user input.

1.What are the most popular three articles of all time?
2.Who are the most popular article authors of all time?
3.On which days did more than 1% of requests lead to errors?


## HOW TO RUN THE PROGRAM
This program is built on a virtual machine that has PostgreSQL alredy installed up on booting. You might need to download vagrant and virtualbox to run it on your virtual machine. After setting up your vagrantfile correctly to install all necessary softwares, you need to type `vagrant up` and then `vagrant ssh` to login to the instance. 

If you run into some errors when you are trying to ssh to the vagrant instance, try the below commands
`vagrant halt`
`vagrant destroy`
`vagrant up`
`vagrant ssh`

Download the news data. Unzip the file in order to extract newsdata.sql and move it to your vagrant folder.

### To load the database type `psql -d news -f newsdata.sql`

### To connect to the database  type `psql -d news`

### To run the Python program type `python3 logsAnalysis.py`

A sample output file `output.txt` is added for a reference with the main python source code `logsAnalysis.py`. 

## CREATED VIEWS FOR QUESTION 3

CREATE VIEW allLogs AS
SELECT to_char(time,'DD-MON-YYYY') as Date, count(*) as LogCount
FROM log
GROUP BY Date;

CREATE VIEW errorLogs AS
SELECT to_char(time,'DD-MON-YYYY') as Date, count(*) as ErrorCount
FROM log
WHERE STATUS NOT LIKE '200 OK'
GROUP BY Date;
