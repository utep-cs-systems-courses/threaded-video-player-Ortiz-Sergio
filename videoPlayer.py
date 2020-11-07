#! /usr/bin/env python3

import cv2

class ProducerConsumer:

    def extract_frames(userFile, queue):
        count = 0;
        video_file = cv2.VideoCapture(userFile)

        success, image = video_file.read()

        while success:
            queue.put(image)

            success, image = video_file.read()
            count += 1

        queue.put('\U0001F920')
