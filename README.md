# Generates .lrc files for your music library
This script scans your music library (mp3, flac, m4a, ogg, opus) and using the song data (artist, track name and duration) fetches and generate a [lrc file](https://en.wikipedia.org/wiki/LRC_(file_format)) spreading the lyrics uniformly across the song's length.

There is also an option to generate a txt file containing only the lyrics without the time tags.

The generated files are stored in the same place and using the same name of the original audio file.
`song_01.flac` -> `song_01.lrc`

## Execution
1. Install [python 3](https://www.python.org/downloads/)
2. Install [Scrapy](https://scrapy.org/) - `pip install Scrapy`
3. Install [Mutagen](https://mutagen.readthedocs.io/en/latest/) - `pip install mutagen`
4. Execute: `scrapy runspider lyrics_fetcher.py`

The script will look for all files below it, so assuming a structure like `Documents/Music/Artist/Album/song.flac`:
 - if you execute the script from the `Music` level it will fetch the lyrics for all songs (all artists and albums) that are contained in the `Music` folder
 - if you execute the script from the `Album` level it will fetch the lyrics for all albuns of that artist
 - if you execute the script from the `song.flac` level it will fetch the lyrics only for that album

## Debugging
Sometimes the URl built from the data in the audio file does not match the actual url used to host the lyrics, in this case you will probablly observe a `404` error associated with the url in the terminal output, it should be possible to debug most of the issues with this info.
