import scrapy
import os
import re
import unicodedata
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

# To execute it, install the dependencies:
# Install python
# pip install Scrapy
# pip install mutagen
# and run:
# execute "scrapy runspider lyrics_fetcher.py"

OVERWRITE_EXISTING_LYRICS = False

def sanitize_values_for_url(value):
    no_parenthesis = re.sub(r'\(.*?\)', "", value)
    no_square = re.sub(r'\[.*?\]', "", no_parenthesis)
    no_dots = no_square.replace("'", "").replace(
        "&", "and").replace(".", "").replace("+", "")
    no_accents = ''.join(c for c in unicodedata.normalize('NFD', no_dots)
                         if unicodedata.category(c) != 'Mn')
    no_spaces = " ".join(no_accents.split())
    return re.sub(r'[^A-Za-z0-9 ]+', ' ', no_spaces).strip(' ').strip('-').replace(' ', '-').lower()

def add_lrc_extension(value):
    return value.removesuffix(".flac").removesuffix(".m4a").removesuffix(".mp3") + ".lrc"

class BlogSpider(scrapy.Spider):
    print("Scaning library...")
    name = 'genius spider'
    urls = []
    values = {}
    for subdir, dirs, files in os.walk('.'):
        for file in files:
            path = os.path.join(subdir, file)
            artistName = ""
            trackName = ""
            duration = 0.0
            if OVERWRITE_EXISTING_LYRICS or not os.path.exists(add_lrc_extension(path)):
                if file.endswith(".flac"):
                    fileInfo = FLAC(path)
                    artistName = fileInfo["albumartist"][0] if "albumartist" in fileInfo == "" else fileInfo["artist"][0]
                    trackName = fileInfo["title"][0] if "title" in fileInfo else ""
                    duration = fileInfo.info.length
                elif file.endswith(".m4a"):
                    fileInfo = MP4(path)
                    artistName = fileInfo['aART'][0] if 'aART' in fileInfo else fileInfo['\xa9ART'][0]
                    trackName = fileInfo['\xa9nam'][0] if '\xa9nam' in fileInfo else ""
                    duration = fileInfo.info.length
                elif file.endswith(".mp3"):
                    fileInfo = EasyID3(path)
                    artistName = fileInfo['albumartist'][0] if 'albumartist' in fileInfo else fileInfo['artist'][0]
                    trackName = fileInfo['title'][0] if 'title' in fileInfo else ""
                    duration = MP3(path).info.length
                if artistName != "" and trackName != "":
                    parsedArtistName = sanitize_values_for_url(artistName)
                    parsedTrack = sanitize_values_for_url(trackName)
                    url = "https://genius.com/" + parsedArtistName + "-" + parsedTrack + "-lyrics"
                    urls.append(url)
                    values[url.lower()] = (duration, path)
    start_urls = urls

    def parse(self, response):
        key = response.url if response.url in self.values else response.request.meta.get('redirect_urls')[0]
        duration = self.values[key][0]
        file_path = self.values[key][1]
        lyrics = "\n".join(response.xpath(
            '//div[@data-lyrics-container="true"]/text() | //div[@data-lyrics-container="true"]/a/span/text() | //div[@data-lyrics-container="true"]/i/text()').getall())
        lines = lyrics.count("\n") + 1
        time_per_line = duration / lines
        new_lyrics = lyrics.split("\n")
        final_lyrics = []
        time = 0
        for line in new_lyrics:
            minutes = int(time // 60)
            seconds = int(time % 60)
            final_lyrics.append(
                "[" + "{:02d}".format(minutes) + ":" + "{:02d}".format(seconds) + ".00]" + line)
            time = time + time_per_line
        f = open(add_lrc_extension(file_path), "w+", encoding='utf-8')
        f.write("\n".join(final_lyrics))
        f.close()
