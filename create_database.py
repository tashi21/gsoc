"""
Create a PostgreSQL database.
"""
import json
import uuid

import psycopg2

# establishing the connection
connection = psycopg2.connect(
    dbname="gsoc",
    user="tashi",
    password="tashi",
    port="5432"
)
connection.autocommit = True

# creating the cursor
cursor = connection.cursor()

# execute initial queries
sql = "CREATE TABLE IF NOT EXISTS Organizations(id UUID PRIMARY KEY, name VARCHAR (200), year SMALLINT, tech_stack TEXT, topics TEXT, short_desc TEXT, link VARCHAR (200), img_url VARCHAR (200), website VARCHAR (200) );"
cursor.execute(sql)
print("Database created successfully")
sql = 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
cursor.execute(sql)
print("Extension created successfully")


with open("data.json", "r") as f:
    data = json.load(f)

for year in data:
    for org in data[year]:
        for name in org:
            ID = uuid.uuid4()
            NAME = name.replace('\'', '\'\'')

            tech_stack = org[name]["tech_stack"] if org[name]["tech_stack"] else None
            string1 = ""
            if tech_stack:
                for tech in tech_stack:
                    string1 += f"{tech}, ".replace('\'', '\'\'')
                string1 = string1[:-2]
                tech_stack = string1

            topics = org[name]["topics"] if org[name]["topics"] else None
            string2 = ""
            if topics:
                for topic in topics:
                    string2 += f"{topic}, ".replace('\'', '\'\'')
                string2 = string2[:-2]
                topics = string2

            short_desc = org[name]["short_description"].replace(
                '\'', '\'\'') if org[name]["short_description"] else None
            link = org[name]["link"] if org[name]["link"].replace(
                '\'', '\'\'') else None
            img_url = org[name]["img_url"].replace(
                '\'', '\'\'') if org[name]["img_url"] else None
            website = org[name]["website"].replace(
                '\'', '\'\'') if org[name]["website"] else None

            sql = f"INSERT INTO Organizations values('{ID}', '{NAME}', {year}, '{tech_stack}', '{topics}', '{short_desc}', '{link}', '{img_url}', '{website}');"
            cursor.execute(sql)
print("Data added successfully")

# closing the connection
connection.close()
print("Connection closed successfully")
