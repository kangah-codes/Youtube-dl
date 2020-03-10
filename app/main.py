from guizero import App, Window, MenuBar, ListBox
import guizero
import requests
from PIL import Image
from io import BytesIO
from pytube import YouTube
import pytube
import os
import threading
import urllib

# global variables
selected_quality = None
video_link = None
video_box = None
push_btn = None
try_again = None
loading_text = None
qualities = '360p'
display_width = 500

app = App(title="Youtube-dl", width=display_width, height=600)


def dest_function():
	print('LOL')

def about_function():
	print("LOL")

menubar = MenuBar(app,toplevel=["Download", "About"],options=[
  [ ["Select a download location", dest_function] ],
  [ ["About Youtube-dl", about_function] ]
])
#main_window = Window(app, title="Youtube-dl")

"""
https://www.youtube.com/watch?v=uLls8mRFhZQ
"""


def main():
	guizero.Text(app, text=" ")
	guizero.Text(app, text="Youtube Video Downloader")
	guizero.Text(app, text=" ")
	guizero.Text(app, text="Insert the video link below")
	guizero.Text(app, text=" ")
	global video_link
	video_link = guizero.TextBox(app, width=int(display_width*0.1))
	guizero.Text(app, text=" ")
	global push_btn
	push_btn = guizero.PushButton(app, text="Search Video", command=start_download_thread)
	global video_box
	video_box = guizero.Box(app, width=int(display_width-100), height=100)


def get_link_val():
	return video_link.value

def get_video():
	link = get_link_val()
	try:
		video = YouTube(str(link))
		title = video.title
		thumbnail_response = requests.get(video.thumbnail_url)
		img = Image.open(BytesIO(thumbnail_response.content))
		quality = video.streams.filter(progressive=True)
		global selected_quality
		selected_quality = [items.resolution for items in quality]
	except pytube.exceptions.RegexMatchError:
		#global video_box
		video_box.width = "fill"
		guizero.Text(video_box, text=" ")
		txt = guizero.Text(video_box, text="Please enter a valid YouTube video link")
	except urllib.error.URLError:
		video_box.width = "fill"
		guizero.Text(video_box, text=" ")
		txt = guizero.Text(video_box, text="Please check your internet connection and try again")
		guizero.Text(video_box, text=" ")
		global try_again
		try_again = guizero.PushButton(app, text="Try again", command=start_download_thread)
		guizero.Text(app, text=" ")
	else:
		#global video_box
		picture_box = guizero.Box(video_box, align="left", width=100, height="fill")
		info_box = guizero.Box(video_box, align="right", width=display_width-100, height="fill")
		thumbnail = guizero.Picture(picture_box, image=img, align="left", width=100, height=100)
		title = guizero.Text(info_box, text=title, width="fill")
		download_box = guizero.Box(info_box, width=75, height=50)
		global qualities
		download_btn = guizero.PushButton(download_box, text="Download", command=download_video, args=[quality[selected_quality.index(qualities.value)], os.getcwd(), title])
		qualities = guizero.ListBox(info_box, items=[item.resolution for item in quality], width=100, height=100)
	loading_text.destroy()

def start_download_thread():
	download_thread = threading.Thread(target=get_video)
	download_thread.start()
	push_btn.destroy()
	global loading_text
	loading_text = guizero.Text(app, text="Loading...")
	if not download_thread.isAlive():
		print("DONE")
	try:
		try_again.destroy()
		loading_text = guizero.Text(app, text="Loading...")
	except:
		pass

def download_video(stream, destination, title):
	stream.download(os.path.join(destination, f"{title}.mp4"))



if __name__ == "__main__":

	main()
	app.display()