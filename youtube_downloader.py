from pytube import YouTube
import sys
import moviepy.editor as mp
from os import remove, path
import validators
import requests

class Video:
    def __init__(self, link, mode, resolution, save_location, audio):
        self.link = link
        self.mode = mode
        self.resolution = resolution
        self.save_location = save_location
        self.audio = audio
        self.title = ''

    @property
    def mode(self):
        return self._mode
    @mode.setter
    def mode(self, inp):
        if inp != "Video" and inp != "Audio":
            raise ValueError("Invalid input: select Audio or Video.")
        self._mode = inp

    @property
    def resolution(self):
        return self._resolution
    @resolution.setter
    def resolution(self, res):
        valid = ["144p", "240p", "360p", "480p", "720p", "1080p"]
        if res not in valid:
            raise ValueError("Invalid resolution. Supported resolutions are 144p, 240p, 360p, 480p, 720p, 1080p.")
        self._resolution = res

    @property
    def audio(self):
        return self._audio
    @audio.setter
    def audio(self, inp):
        if inp != "Yes" and inp != "No":
            raise ValueError("Invalid input.")
        self._audio = inp
    
    @property
    def link(self):
        return self._link
    @link.setter
    def link(self, url):
        if validators.url(url) != True:
            raise ValueError("Invalid link.")
        if "www.youtube.com" not in url:
            raise ValueError("Invalid link.")

        r = requests.get(url)
        pattern = '"playabilityStatus":{"status":"ERROR"'

        if pattern in r.text:
            raise ValueError("Video is unavailable")
        self._link = url

    @property
    def save_location(self):
        return self._save_location
    @save_location.setter
    def save_location(self, save_path):
        if not path.exists(save_path):
            raise ValueError("Path does not exist")
        self._save_location = save_path


    def __str__(self):
        return f"Link: {self.link}, Mode: {self.mode}, Resolution: {self.resolution}"
    
def download(video):

    try:
        yt = YouTube(video.link)
        video.title = yt.title
        
        stream_info = []
        if video.audio == "Yes":
            stream_info = yt.streams.filter(only_audio=True, mime_type="audio/mp4")
            stream_info = stream_info.order_by(attribute_name="abr")
            stream_info = stream_info.first()
            print("Downloading audio...")
            file = video.title + " - Audio" + ".mp4"
            stream_info.download(output_path=video.save_location, filename=file)
            print("Download finished.")

        if video.mode == "Video":
            stream_info = yt.streams.filter(only_video=True, mime_type="video/mp4", resolution=video.resolution)
            stream_info = stream_info.first()
            print("Downloading video...")
            file = video.title + " - Video" + ".mp4"
            stream_info.download(output_path=video.save_location, filename=file)
            print("Download finished.")
    except:
        sys.exit("Download failed. Please try again")
        

def mix(video):
    try:
        print("Mixing...This might take a while")
        video_name = video.save_location + "/" + video.title + " - Video" + ".mp4"
        clip = mp.VideoFileClip(video_name)
        audio_name = video.save_location + "/" + video.title + " - Audio" + ".mp4"
        audio = mp.AudioFileClip(audio_name)
        final = clip.set_audio(audio)

        final_name = video.save_location + "/" + video.title + ".mp4"
        final.write_videofile(final_name)
        remove(video_name)
        remove(audio_name)

        print("Video is ready")
    except:
        sys.exit("Could not mix files. Please try again.")



def main():
    link = input("Video link: ")
    mode = input("Audio / Video: ")
    resolution = "144p"
    audio = "No"
    mix_video = "No"

    if mode == "Video":
        resolution = input("Video resolution to download(max 1080p): ")
        audio = input("Download audio too?(Yes / No): ")
    
    if mode == "Audio":
        audio = "Yes"


    save_location = input("Input location to save video: ")

    video = Video(link, mode, resolution, save_location, audio)
    download(video)

    if video.audio == "Yes" and video.mode == "Video":
        mix_video = input("Do you want to mix audio and video?(Yes / No): ")
    
    if mix_video == "Yes":
        mix(video)

if __name__ == "__main__":
    main()