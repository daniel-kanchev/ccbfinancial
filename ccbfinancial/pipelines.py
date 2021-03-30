from itemadapter import ItemAdapter
import sqlite3


class DatabasePipeline:
    # Database setup
    conn = sqlite3.connect('ccbfinancial.db')
    c = conn.cursor()

    def open_spider(self, spider):
        self.c.execute(""" DROP TABLE IF EXISTS articles """)

        self.c.execute(""" CREATE TABLE articles (
        title text, 
        link text, 
        content text
        ) """)

    def process_item(self, item, spider):
        self.c.execute("""SELECT rowid FROM articles WHERE title = ?""",
                       (item.get('title'), ))
        duplicate = self.c.fetchone()
        if duplicate:
            self.c.execute("""UPDATE articles SET title = ?, link = ?, content = ? WHERE rowid = ?""",
                           (item.get('title'), item.get('link'), item.get('content'), duplicate[0]))

            if 'link' in item.keys():
                print(f"Updated Article: {item['link']}")
            else:
                print(f"Updated Article: {item['title']}")

        else:
            # Insert values
            self.c.execute("INSERT INTO articles ("
                           "title, "
                           "link, "
                           "content)"
                           " VALUES (?,?,?)",
                           (item.get('title'),
                            item.get('link'),
                            item.get('content')
                            ))

            if 'link' in item.keys():
                print(f"New Article: {item['link']}")
            else:
                print(f"New Article: {item['title']}")

        self.conn.commit()  # commit after every entry

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
