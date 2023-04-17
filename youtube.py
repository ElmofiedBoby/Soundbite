from youtube_search import YoutubeSearch as yts
from yt_dlp import YoutubeDL as ytd
import os

def search(artist, song, channel):

    if channel is not None:
        query = f"{artist} - {song} karaoke channel:\"{channel}\""
        results = yts(query, max_results=10).to_dict()

        songs = []
        for item in results:
            if item['channel'] == channel and song in item['title']:
                songs.append(item)
        
        return songs
    else:
        query = f"{artist} - {song} (Audio)"
        results = yts(query, max_results=10).to_dict()

        songs = []
        for item in results:
            if song in item['title']:
                songs.append(item)
        
        return songs

def download(search_result, audioOnly):
    if audioOnly:
        ydl_opts = {
            'default_search': 'ytsearch',
            'ignoreerrors': True,
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': True,
            'outtmpl': os.path.join(os.getcwd(), 'videos', '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
    else:
        ydl_opts = {
            'default_search': 'ytsearch',
            'ignoreerrors': True,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': True,
            'outtmpl': os.path.join(os.getcwd(), 'videos', '%(title)s.%(ext)s')
        }

    with ytd(ydl_opts) as ydl:
        ydl.download(['https://youtube.com'+search_result['url_suffix']])

result = search('Taylor Swift', 'Love Story', 'Sing King')
download(result[0], False)