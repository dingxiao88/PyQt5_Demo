
# origin add:
# https://raspberrypi.stackexchange.com/questions/125184/play-an-audio-stream-internet-radio-and-start-again-automatically-after-wi-fi

#!/usr/bin/env python3

import vlc
import time

# char * arrayURL[8] = {
#   "http://jenny.torontocast.com:8134/stream",
  
#   "http://188.165.212.154:8478/stream",
#   "https://igor.torontocast.com:1025/;.mp3",
#   "http://streamer.radio.co/s06b196587/listen",
   
  
#   "http://media-ice.musicradio.com:80/ClassicFMMP3",
#   "http://naxos.cdnstream.com:80/1255_128",
#   "http://149.56.195.94:8015/steam",
#   "http://ice2.somafm.com/christmas-128-mp3"
# };

url = 'http://jenny.torontocast.com:8134/stream'

#define VLC instance
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

#Define VLC player
player=instance.media_player_new()

#Define VLC media
media=instance.media_new(url)

#Set player media
player.set_media(media)

#Play the media
player.play()

# Checks whether playing, but doesn't work,
# because is_playing returns True when VLC is open and idle.
while True:
  time.sleep(10)
  try:
    while player.is_playing():
      time.sleep(10)
    else:
      time.sleep(10)
# Tries to start playing again.
  except:
    try:
      player.play()
      time.sleep(10)
    except:
      time.sleep(10)

# -------------------------------------------------------------------

# import requests
# import time
# import datetime
# print(datetime.datetime.now())
# import re


# url = 'http://jenny.torontocast.com:8134/stream'
# encoding = 'latin1'
# info = ''

# radio_session = requests.Session()

# while True:

#     radio = radio_session.get(url, headers={'Icy-MetaData': '1'}, stream=True)

#     metaint = int(radio.headers['icy-metaint'])

#     stream = radio.raw

#     audio_data = stream.read(metaint)
#     meta_byte = stream.read(1)

#     if (meta_byte):
#         meta_length = ord(meta_byte) * 16

#         meta_data = stream.read(meta_length).rstrip(b'\0')

#         stream_title = re.search(br"StreamTitle='([^']*)';", meta_data)


#         if stream_title:

#             stream_title = stream_title.group(1).decode(encoding, errors='replace')

#             if info != stream_title:
#                 print('Now playing: ', stream_title)
#                 info = stream_title
#             else:
#                 pass

#         else:
#             print('No StreamTitle!')

#     time.sleep(1)