from pytube import YouTube

class Video:
    def __init__(self, link, mode, resolution, save_location):
        self.link = link
        self.mode = mode
        self.resolution = resolution
        self.save_location = save_location
    
    def __str__(self):
        return f"Link: {self.link}, Mode: {self.mode}, Resolution: {self.resolution}"

def download(video):
    yt = YouTube(video.link)
    ys = ''
    stream_info = []
    if video.mode == "Audio":
        stream_info = yt.streams.filter(only_audio=True)
        stream_info = stream_info.order_by(attribute_name="abr")
        stream_info = stream_info.last()
        print("Downloading...")
        stream_info.download(video.save_location)
        print("Download finished!")
    else:
        stream_info = yt.streams.filter(only_video=True)


def main():
    link = input("Video link: ")
    mode = input("Audio / Video: ")
    resolution = ''

    if mode == "Video":
        resolution = input("Video resolution to download: ")

    save_location = input("Input location to save video: ")

    video = Video(link, mode, resolution, save_location)
    download(video)
    

if __name__ == "__main__":
    main()