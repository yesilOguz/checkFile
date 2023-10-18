import re
import requests
import sqlite3

mainUrl = "https://virusshare.com/"
response = requests.get("https://virusshare.com/hashes")

html = response.text

pattern = r'<a\s+href="([^"]+\.md5)"[^>]*>'

md5_links = re.findall(pattern, html)

connection = sqlite3.connect('md5Database.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS md5 (
        id INTEGER PRIMARY KEY,
        key TEXT NOT NULL
    )
''')

connection.commit()

i = 1

for link in md5_links:
    if "unpacked_hashes" in link:
        continue

    print("Start")

    getHashResponse = requests.get(mainUrl + link)
    md5s = getHashResponse.text.split("\n")
    for md5 in md5s:
        if md5 == '' or md5.startswith('#'):
            continue
        
        data_to_insert = (i, md5)
        cursor.execute("INSERT INTO md5 (id, key) VALUES (?, ?)", data_to_insert)
        connection.commit()

        i += 1
    
    print("Finish")
    print("------------")
    
print("The whole operation is over!!")
connection.close()
    
