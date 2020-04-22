#!/usr/bin/env python3

import psycopg2

print('This tool will be used to get some reports about ' +
      'questions listed below.')
print('1. What are the most popular three articles of all time? \n'
      '2. Who are the most popular article authors of all time?\n'
      '3. On which days did more than 1% of requests lead to errors?')

# Referenced some queries from forums and github repos to get more
# understanding and other different possible ways that could be done

popular_articles_query = ("SELECT title, count(*) as views FROM articles \n"
                          "JOIN log\n"
                          "ON articles.slug = substring(log.path, 10)\n"
                          "GROUP BY title ORDER BY views DESC LIMIT 3;"
                          )

popular_authors_query = ("SELECT authors.name, count(*) as views\n"
                         "FROM articles \n"
                         "JOIN authors\n"
                         "ON articles.author = authors.id \n"
                         "JOIN log \n"
                         "ON articles.slug = substring(log.path, 10)\n"
                         "WHERE log.status LIKE '200 OK'\n"
                         "GROUP BY authors.name ORDER BY views DESC LIMIT 3;"
                         )

error_query = ("SELECT errorLogs.date, ROUND(100.0*errorcount/logcount,2)\n"
               "AS percentage FROM allLogs, errorLogs WHERE \n"
               "allLogs.date = errorLogs.date AND errorcount > logcount/100;")


def getPopularArticlesAndAuthors(query):
    try:
        # Connecting to the news DB
        items_to_display = []
        connection = psycopg2.connect("dbname=news")
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        items_to_display.append(record)
        for item in items_to_display:
            # getting item indexes and extracting the tuples
            print('{} -- {} views'.format(item[0][0], item[0][1]))
            print('{} -- {} views'.format(item[1][0], item[1][1]))
            print('{} -- {} views'.format(item[2][0], item[2][1]))

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def getHighErrorDates(error_query):
    try:
        # Connecting to the news DB
        connection = psycopg2.connect("dbname=news")
        cursor = connection.cursor()
        cursor.execute(error_query)
        records = cursor.fetchall()
        for day in records:
            print('{} -- {} % errors'.format(day[0], day[1]))
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# method to perform action and display result based on user input
def performAction():
    user_input = input('Please enter 1, 2 or 3 based on which ' +
                       'report you would like to see:  ')

    # only accept the below 3 options
    options = ['1', '2', '3']
    while user_input not in options:
        user_input = input('Please enter 1, 2 or 3 and try again:  ')
    if user_input == options[0]:
        print('Getting the top 3 most popular articles....')
        getPopularArticlesAndAuthors(popular_articles_query)
    elif user_input == options[1]:
        print('Getting the 3 most popular authors....')
        getPopularArticlesAndAuthors(popular_authors_query)
    elif user_input == options[2]:
        print('Getting the dates where there are above 1% of request....')
        getHighErrorDates(error_query)


performAction()
