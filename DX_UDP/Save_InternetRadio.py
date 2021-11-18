# origin add:
# https://stackoverflow.com/questions/4247248/record-streaming-and-saving-internet-radio-in-python


import requests

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

stream_url = 'http://jenny.torontocast.com:8134/stream'

r = requests.get(stream_url, stream=True)

with open('stream.mp3', 'wb') as f:
    try:
        for block in r.iter_content(1024):
            f.write(block)
    except KeyboardInterrupt:
        pass