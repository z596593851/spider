from datetime import datetime
from elasticsearch_dsl import Document, Date, Nested, Boolean, \
    analyzer, InnerDoc, Completion, Keyword, Text,connections

connections.create_connection(hosts=['localhost'])

class Douban(Document):
    url = Keyword()
    title = Text(analyzer="ik_max_word")
    time = Date()
    director = Keyword()
    area = Keyword()
    language = Text(analyzer="ik_max_word")
    nickname = Text(analyzer="ik_max_word")
    score = Keyword()
    introduction = Text(analyzer="ik_max_word")
    front_image_url = Keyword()
    front_image_path = Keyword()

    class Meta:
        doc_type="info"

    class Index:
        name = "douban"
        #doc_type="info"
        # settings = {
        #     "number_of_shards": 2,
        # }

if __name__ == '__main__':
    Douban.init()