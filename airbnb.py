'''
Flow for seeding the database:
    - Take advantage of infinite scoll on random Airbnb pages
    and save the HTML to .txt files
    - Run load_data() function, which outputs a .tsv with all
    of the captured rooms and descriptions
    - Paste the tsv data into google spreadsheets, adding a col
    to load the rooms' images
    - Add indicator variable for whether or not to include the room
    - Filter down to ones worth including, and then paste that data
    to the .tsv file generated earlier

Now, the parse_data() function will parse each line of the .tsv. Its
JSON output is used directly by the chrome extension.

Later on, I should be able to add to the JSON output from just
the Airbnb room number. This function should simply scrape the page
per usual and then add the data to the .json file.
    ** FIRST, it needs to make sure that the json data does not
    already include this soon-to-be-added room.
'''

import requests
import re
import json
from bs4 import BeautifulSoup as bs
from time import sleep

'''
These functions are relics from an ancient time, when I needed to
seed the database from HTML files taken straight from Airbnb.com
'''
def load_file(file):
    raw = open(file).read()
    return bs(raw)

def load_files(files):
    return [load_file(file) for file in files]

def get_rooms_from_files(bs_objs):
    rooms = []
    for bs_obj in bs_objs:
        for link in bs_obj.find_all('a'):
            href = link.get('href')
            if href and 'rooms' in href:
                rooms.append(href)
    return rooms


def get_room(room):
    link = 'https://www.airbnb.com' + room
    data = requests.get(link).text
    return bs(data)

def get_img(data):
    img = data.find('meta', {'property': 'og:image'})

    if img:
        img = img.get('content')
        img = re.sub(r'aki_policy.*$', 'aki_polity=xx_large', img)
        return img

def get_title(data):
    return data.title.string.encode('utf-8').strip()

def get_desc(data):
    desc = data.find('meta', {'name':'description'})

    if desc:
        return desc.get('content').encode('utf-8').strip()

def load_data():
    loaded_files = load_files(['airbnb1.txt', 'airbnb2.txt'])
    all_rooms = get_rooms_from_files(loaded_files)
    return set(all_rooms)

'''
new stuff
'''
def load_rooms():
    all_rooms = [line.rstrip() for line in open('rooms.txt')]
    return set(all_rooms)

def fetch_rooms(all_rooms):
    print 'there are %s rooms' % len(all_rooms)
    with open('rooms-out.tsv', 'w') as out:
        for i, room in enumerate(all_rooms):
            print i, room
            try:
                room_data = get_room(room)
                room_img = get_img(room_data)
                room_title = get_title(room_data)
                room_desc = get_desc(room_data)
                out.write('%s\t%s\t%s\t%s\n' % (room, room_img, room_title, room_desc))
            except Exception as e:
                print e
            sleep(.1)

def parse_data():
    parsed = []

    re_location = re.compile('(for rent in\s)(.*)$', re.IGNORECASE)
    re_price = re.compile('(for \$)(\d+)(.\s)', re.IGNORECASE)
    with open('rooms-out.tsv') as data:
        for line in data:
            line_split = line.split('\t', 3)

            if len(line_split) == 4:
                id = line_split[0]
                img = line_split[1]
                title = ' - '.join(line_split[2].split(' - ')[:-1])
                location = re_location.search(line_split[2])
                lat_lng = []
                price = re_price.search(line_split[3])

                if location:
                    location = location.group(2)
                    lat_lng = json.loads(requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=[ENV_API_KEY]' % location.replace(' ', '+')).text)
                    if lat_lng and lat_lng['results'] and lat_lng['results'][0]:
                        if lat_lng['results'][0]['geometry']:
                            lat_lng = lat_lng['results'][0]['geometry']['location']
                            lat_lng = [lat_lng['lat'], lat_lng['lng']]
                    sleep(0.2)
                if price:
                    price = price.group(2)

                parsed.append({
                    'id': id,
                    'img': img,
                    'title': title,
                    'location': location,
                    'latlng': lat_lng,
                    'price': price
                })
                print 'added %s' % id

    with open('rooms-parsed.json', 'w') as file:
        json.dump(parsed, file)

def main():
    # rooms = load_data()   # load from raw HTML
    #rooms = load_rooms()    # load from rooms.txt
    #fetch_rooms(rooms)      # generate the rooms-out.tsv
    parse_data()

if __name__ == '__main__':
    main()
