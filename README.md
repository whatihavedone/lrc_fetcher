# Generates .lrc files for your music library
This script scans your music library (mp3, flac, m4a) and using the song data (artist, track name and duration) it fetches and generate a [lrc file](https://en.wikipedia.org/wiki/LRC_(file_format)) using the song's duration to spread the lyrics uniformly in the generated file.

The generated files are stored in the same place and using the same name of the original audio file.

## Execution
1. Install [python 3](https://www.python.org/downloads/)
2. Install [Scrapy](https://scrapy.org/) - `pip install Scrapy`
3. Install [Mutagen](https://mutagen.readthedocs.io/en/latest/) - `pip install mutagen`
4. Execute: `scrapy runspider lyrics_fetcher.py`

The script will look for all files below it, so assuming a structure like `Documents/Music/Artist/Album/song.flac`:
 - if you execute the script from the `Music` level it will fetch the lyrics for all songs (all artists and albuns) that are contained in the `Music` folder
 - if you execute the script from the `Album` level it will fetch the lyrics for all albuns of that artist
 - if you execute the script from the `song.flac` level it will fetch the lyrics only for that album

## Debugging
Sometimes the URl built from the data in the audio file does not match the actual url used to host the lyrics, in this case you will probablly observe a `404` error associated with the url in the terminal output and this should allow debbuging any issue.
