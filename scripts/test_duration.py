from mutagen.mp3 import MP3
audio = MP3("./songs/California love.mp3")
audio_info = audio.info    
print(int(audio_info.length))