#Imports

from tkinter import *
import threading
from pyautogui import screenshot
import numpy as np
import cv2
import pyaudio
import wave
import os









# Video

video_recording = True

fourcc = cv2.VideoWriter_fourcc(*'XVID')
videoWriter = None

def start_video_recording():
	global videoWriter
	videoWriter = cv2.VideoWriter('C:\\Users\\Mita\\AppData\\Local\\Temp\\video.avi', fourcc, 20, (1366, 768))
	while video_recording:
		img = np.array(screenshot())
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		videoWriter.write(img)
		img = cv2.resize(img, (int(img.shape[1]/1.3), int(img.shape[0]/1.3)))
		cv2.waitKey(1)
	cv2.destroyAllWindows()

def stop_video_recording():
	global video_recording
	video_recording = False
	videoWriter.release()






# Audio

# Constants
chunk = 1024
sample_format = pyaudio.paInt16
channels = 2
fs = 48000

p = None
stream = None
frames = None

audio_recording = True

def start_audio_recording():
	global p, stream, frames
	p = pyaudio.PyAudio()
	stream = p.open(format=sample_format,channels=channels,rate=fs,frames_per_buffer=chunk,input=True)
	frames = []
	while audio_recording:
		data = stream.read(chunk)
		frames.append(data)


def stop_audio_recording():
	global audio_recording, p, stream, frames
	audio_recording = False
	put_into_file()




def put_into_file():
	stream.stop_stream()
	stream.close()
	p.terminate()
	wf = wave.open('C:\\Users\\Mita\\AppData\\Local\\Temp\\audio.wav', 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(sample_format))
	wf.setframerate(fs)
	wf.writeframes(b''.join(frames))
	wf.close()



# Combining audio and video

def combine():
	import ffmpeg
	video = ffmpeg.input('C:\\Users\\Mita\\AppData\\Local\\Temp\\video.avi')
	audio = ffmpeg.input('C:\\Users\\Mita\\AppData\\Local\\Temp\\audio.wav')
	video_path = 'C:\\Users\\Mita\\AppData\\Local\\Temp\\output.mp4'
	out = ffmpeg.output(video, audio, video_path, vcodec='copy', acodec='aac', strict='experimental')
	out.run()

def ask_to_save_file():
	from tkinter import filedialog
	filepath = filedialog.asksaveasfilename(title='Save Recording', filetypes=(('MP4 File', '*.mp4'),))
	if filepath.endswith('.mp4'):
		pass
	else:
		filepath = filepath + '.mp4'
	file = open(filepath, 'wb')
	outpath = 'C:\\Users\\Mita\\AppData\\Local\\Temp\\output.mp4'
	out = open(outpath, 'rb')
	outcont = out.read()
	file.write(outcont)
	file.close()
	out.close()





# Main Program

root = Tk()
root.title('Screen Recorder')
root.geometry('400x250')

def start_recording():
	stop_recording_button['state'] = NORMAL
	threading.Thread(target=start_video_recording).start()
	threading.Thread(target=start_audio_recording).start()
	label.config(text='Recording...')

def stop_recording():
	stop_video_recording()
	stop_audio_recording()
	stop_recording_button['state'] = DISABLED
	label.config(text='Finished Recording!')
	try:
		os.remove('C:\\Users\\Mita\\AppData\\Local\\Temp\\output.mp4')
	except:
		pass
	combine()
	ask_to_save_file()
	try:
		os.remove('C:\\Users\\Mita\\AppData\\Local\\Temp\\video.avi')
		os.remove('C:\\Users\\Mita\\AppData\\Local\\Temp\\audio.wav')
		os.remove('C:\\Users\\Mita\\AppData\\Local\\Temp\\output.mp4')
	except:
		pass
	root.destroy()
	exit()

start_recording_button = Button(root, text='Start Recording', font=('Comic Sans Ms', 15), fg='green', borderwidth=5, command=start_recording)
start_recording_button.pack()

stop_recording_button = Button(root, text='Stop Recording', font=('Comic Sans Ms', 15), fg='red', state=DISABLED, borderwidth=5, command=stop_recording)
stop_recording_button.pack()

label = Label(root)
label.pack()

root.mainloop()