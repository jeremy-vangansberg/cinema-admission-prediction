# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re




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
                print('***cleaning done***')

        # Removing white spaces
        entries = adapter.get('entries')
        adapter['entries'] = entries.replace(" ", "")
        
        return item
