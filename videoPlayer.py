#! /usr/bin/env python3

import cv2

class ProducerConsumer:

    def extract_frames(userFile, queue):
        count = 0
        video_file = cv2.VideoCapture(userFile)

        success, image = video_file.read()

        while success:
            queue.put(image)

            success, image = video_file.read()
            count += 1

        queue.put('\U0001F920')

    def convert_grayscale(color, gray):
        count = 0

        colorFrame = color.get()

        while colorFrame is not '\U0001F920':
            grayFrame = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)

            gray.put(grayFrame)
            count += 1

            colorFrame = color.get()

        gray.put('\U0001F920')

        
