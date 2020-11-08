#! /usr/bin/env python3

import cv2
import threading

class ProducerConsumer:
    def __init__(self):
        self.queue = []
        self.lock = threading.Lock()
        self.full = threading.Semaphore(0)
        self.empty = threading.Semaphore(24)

    def put(self, frame):
        self.empty.acquire()
        self.lock.acquire()
        self.queue.append(frame)
        self.lock.release()
        self.full.release()

    def get(self):
        self.full.acquire()
        self.lock.acquire()
        frame = self.queue.pop(0)
        self.lock.release()
        self.empty.release()
        return frame

def extract_frames(userFile, queue):
    count = 0
    video_file = cv2.VideoCapture(userFile)

    success, image = video_file.read()

    while success:
        queue.put(image)

        success, image = video_file.read()
        count += 1

    queue.put('end')

def convert_grayscale(color, gray):
    count = 0

    colorFrame = color.get()

    while colorFrame is not 'end':
        grayFrame = cv2.cvtColor(colorFrame, cv2.COLOR_BGR2GRAY)

        gray.put(grayFrame)
        count += 1

        colorFrame = color.get()

    gray.put('end')

def display_frames(frames):
    count = 0
    currentFrame = frames.get()

    while currentFrame is not 'end':
        cv2.imshow('Video', currentFrame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break
        count += 1

        currentFrame = frames.get()

    cv2.destroyAllWindows()

        
color_frames = ProducerConsumer()
gray_frames = ProducerConsumer()

extract = threading.Thread(target = extract_frames, args = ('clip.mp4', color_frames))
convert = threading.Thread(target = convert_grayscale, args = (color_frames, gray_frames))
display = threading.Thread(target = display_frames, args = (gray_frames,))

extract.start()
convert.start()
display.start()
