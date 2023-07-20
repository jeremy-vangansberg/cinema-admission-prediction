# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import pyodbc
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(dotenv_path='/home/jeremy/Documents/projects/cinema-admission-prediction/data_collection/.env')





class BoxOfficePipeline:
    def duration_cleaner(self, list_duree):
        duree = ''.join(list_duree).replace(' ', '')
        duree = duree.strip()
        list_hour = re.findall(r'(\d+)', duree)

        hour = 0
        minutes = 0

        if len(list_hour) == 2:
            hour = int(list_hour[0]) * 60
            minutes = int(list_hour[1])
        elif len(list_hour) == 0:
            return 0
        else:
            if 'm' in duree:
                print('min in duree')
                minutes = int(list_hour[0])
            else:
                hour = int(list_hour[0]) * 60

        return hour + minutes

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Transforming list into string
        duration = adapter.get('duration')
        adapter['duration'] = self.duration_cleaner(duration)

        field_names = adapter.field_names()

        # strip the strings
        for field_name in field_names:
            if field_name != "duration" :
                value = adapter.get(field_name)
                if value is not None :
                    adapter[field_name] = value.strip()

        # Removing white spaces
        entries = adapter.get('entries')
        adapter['entries'] = int(entries.replace(" ", ""))

        # convert to date
        date = adapter.get('release_date')
        date_format = '%d/%m/%Y'
        adapter['release_date'] = datetime.strptime(date, date_format)
        
        return item

class SaveAzureSQLPipeline:

    def __init__(self) -> None:
        try:
            self.server = os.getenv('DB_HOST')
            self.database = os.getenv('DB_NAME')
            self.username = os.getenv('DB_USER')
            self.password = os.getenv('DB_PASSWORD')

            self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';ENCRYPT=yes;UID='+self.username+';PWD='+ self.password)
            self.cursor = self.cnxn.cursor()

            self.cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='boxoffice' and xtype='U')
            BEGIN
                CREATE TABLE boxoffice(
                    id INT NOT NULL IDENTITY(1,1),
                    title VARCHAR(255),
                    original_title VARCHAR(255),
                    entries INTEGER,
                    director VARCHAR(255),
                    release_date DATE,
                    duration INTEGER,
                    PRIMARY KEY (id)
                    )
                END
            """)
            self.cnxn.commit()

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def process_item(self, item, spider):
        try:
            ## Define insert statement
            self.cursor.execute(""" INSERT INTO boxoffice (
                title, 
                original_title, 
                entries, 
                director,
                release_date,
                duration
                ) values (?, ?, ?, ?, ?, ?)""", (
                item["title"],
                item["original_title"],
                item["entries"],
                item["director"],
                item["release_date"],
                item["duration"]
            ))

            ## Execute insert of data into database
            self.cnxn.commit()

        except Exception as e:
            print(f"An error occurred when inserting data: {str(e)}")
        return item

    def close_spider(self, spider):
        try:
            ## Close cursor & connection to database 
            self.cursor.close()
            self.cnxn.close()

        except Exception as e:
            print(f"An error occurred when closing the connection: {str(e)}")
