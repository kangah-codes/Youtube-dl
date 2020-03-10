from guizero import App, Window, MenuBar
import guizero
import requests
from PIL import Image
from io import BytesIO
from pytube import YouTube
import pytube
import os
import threading

# global variables
selected_quality = None
video_link = None
video_box = None
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

class MainThread(threading.Thread):
	def __init__(self, download_thread):
		self.selected_quality = None
		self.video_link = None
		self.video_box = None
		self.display_width = 500
		self.download_thread = download_thread

		self.app = App(title="Youtube-dl", width=self.display_width, height=600)
		self.menubar = MenuBar(app,toplevel=["Download", "About"],options=[
		  [ ["Select a download location", self.dest_function] ],
		  [ ["About Youtube-dl", self.about_function] ]
		])

	def dest_function(self):
		print("LOL")

	def about_function(self):
		print("LOL")

	def main(self):
		guizero.Text(app, text=" ")
		guizero.Text(app, text="Youtube Video Downloader")
		guizero.Text(app, text=" ")
		guizero.Text(app, text="Insert the video link below")
		guizero.Text(app, text=" ")
		self.video_link = guizero.TextBox(app, width=int(display_width*0.1))
		guizero.Text(app, text=" ")
		guizero.PushButton(app, text="Search Video", command=self.download_thread.get_video)
		self.video_box = guizero.Box(app, width="fill", height="fill")
		self.app.display()

	def run(self):
		self.main()
		#self.app.display()



class DownloadThread(threading.Thread):
	def get_link_val(self):
		return self.video_link.value

	def get_video(self):
		link = get_link_val()
		try:
			video = YouTube(str(link))
			title = video.title
			thumbnail_response = requests.get(video.thumbnail_url)
			img = Image.open(BytesIO(thumbnail_response.content))
			quality = video.streams.filter(progressive=True)
			self.selected_quality = quality[-1]
		except pytube.exceptions.RegexMatchError:
			#global video_box
			video_box.width = "fill"
			guizero.Text(video_box, text=" ")
			guizero.Text(video_box, text="Please enter a valid YouTube video link")
		else:
			#global video_box
			thumbnail = guizero.Picture(video_box, image=img, align="left", width=100, height=100)



# def main():
# 	guizero.Text(app, text=" ")
# 	guizero.Text(app, text="Youtube Video Downloader")
# 	guizero.Text(app, text=" ")
# 	guizero.Text(app, text="Insert the video link below")
# 	guizero.Text(app, text=" ")
# 	global video_link
# 	video_link = guizero.TextBox(app, width=int(display_width*0.1))
# 	guizero.Text(app, text=" ")
# 	guizero.PushButton(app, text="Search Video", command=get_video)
# 	global video_box
# 	video_box = guizero.Box(app, width="fill", height="fill")


# def get_link_val():
# 	return video_link.value

# def get_video():
# 	link = get_link_val()
# 	try:
# 		video = YouTube(str(link))
# 		title = video.title
# 		thumbnail_response = requests.get(video.thumbnail_url)
# 		img = Image.open(BytesIO(thumbnail_response.content))
# 		quality = video.streams.filter(progressive=True)
# 		global selected_quality
# 		selected_quality = quality[-1]
# 	except pytube.exceptions.RegexMatchError:
# 		#global video_box
# 		video_box.width = "fill"
# 		guizero.Text(video_box, text=" ")
# 		guizero.Text(video_box, text="Please enter a valid YouTube video link")
# 	else:
# 		#global video_box
# 		thumbnail = guizero.Picture(video_box, image=img, align="left", width=100, height=100)



# def download_video(stream, destination, title):
# 	stream.download(os.path.join(destination, title))


if __name__ == "__main__":
	d = DownloadThread()
	a = MainThread(d)
	a.run()