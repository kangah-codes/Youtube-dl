from guizero import App, Window
import pytube
import requests
from PIL import Image
from io import BytesIO
import os

# global variables
selected_quality = None

app = App(title="Youtube-dl", width=500, height=600)
main_window = Window(app, title="Youtube-dl")

def main():
	guizero.Text(app, text=" ")
	guizero.Text(app, text="Youtube Video Downloader")
	guizero.Text(app, text="Insert the video link below")

	video_link = guizero.TextBox(app)


def get_video(link):
	video = pytube.Youtube(str(link))
	title = video.title
	thumbnail_response = requests.get(video.thumbnail_url)
	img = Image.open(BytesIO(thumbnail_response.content))
	quality = video.streams.filter(progressive=True).all()
	global selected_quality
	selected_quality = quality[-1]

def download_video(stream, destination, title):
	stream.download(os.path.join(destination, title))


if __name__ == "__main__":
	main()
	app.display()