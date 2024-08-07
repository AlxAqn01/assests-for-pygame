#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import copy
import time
import itertools

import cv2 as cv
import numpy as np
import mediapipe as mp
from picamera2 import Picamera2

from model import KeyPointClassifier

class GestureRecognition:
    def __init__(self, target_gestures):
        self.target_gestures = target_gestures
        self.current_gesture = "None"
        self.last_detected_gesture = "None"
        self.gesture_start_time = None
        self.detection_duration = 2.0  # Duration in seconds to confirm gesture

        # Initialize Mediapipe and KeyPointClassifier
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )
        self.keypoint_classifier = KeyPointClassifier()

        # Read labels
        with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
            keypoint_classifier_labels = csv.reader(f)
            self.keypoint_classifier_labels = [row[0] for row in keypoint_classifier_labels]

        # Initialize Picamera2
        self.picam2 = Picamera2()
        camera_config = self.picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (600, 480)})
        self.picam2.configure(camera_config)
        self.picam2.start()

    def detect_gesture(self):
        detected_gesture = "None"
        
        while True:
            frame = self.picam2.capture_array()
            image = frame[:, :, :3]  # Remove alpha channel
            image = cv.flip(image, 1)  # Mirror display
            debug_image = copy.deepcopy(image)

            # Detection implementation
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

            image.flags.writeable = False
            results = self.hands.process(image)
            image.flags.writeable = True

            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    # Bounding box calculation
                    brect = self.calc_bounding_rect(debug_image, hand_landmarks)
                    # Landmark calculation
                    landmark_list = self.calc_landmark_list(debug_image, hand_landmarks)

                    # Conversion to relative coordinates / normalized coordinates
                    pre_processed_landmark_list = self.pre_process_landmark(landmark_list)

                    # Hand sign classification
                    hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list)
                    detected_gesture = self.keypoint_classifier_labels[hand_sign_id]

                    # Check if the detected gesture matches any of the target gestures
                    if detected_gesture in self.target_gestures:
                        # Check if the gesture is held for the required duration
                        if detected_gesture == self.last_detected_gesture:
                            if self.gesture_start_time is None:
                                self.gesture_start_time = time.time()
                            elif (time.time() - self.gesture_start_time) >= self.detection_duration:
                                self.current_gesture = detected_gesture
                                self.picam2.stop()
                                cv.destroyAllWindows()
                                return self.current_gesture
                        else:
                            self.gesture_start_time = time.time()
                            self.last_detected_gesture = detected_gesture
                    else:
                        self.gesture_start_time = None
                        self.last_detected_gesture = detected_gesture

                    # Draw bounding box
                    debug_image = self.draw_bounding_rect(debug_image, brect)

            else:
                self.last_detected_gesture = "None"
                self.gesture_start_time = None

            # Display the camera feed
            cv.putText(debug_image, f'Gesture: {self.current_gesture}', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
            cv.imshow('Hand Gesture Recognition', debug_image)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        self.picam2.stop()
        cv.destroyAllWindows()
        return self.current_gesture

    def calc_bounding_rect(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_array = np.empty((0, 2), int)

        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point = [np.array((landmark_x, landmark_y))]

            landmark_array = np.append(landmark_array, landmark_point, axis=0)

        x, y, w, h = cv.boundingRect(landmark_array)

        return [x, y, x + w, y + h]

    def calc_landmark_list(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]

        landmark_point = []

        # Keypoint
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)

            landmark_point.append([landmark_x, landmark_y])

        return landmark_point

    def pre_process_landmark(self, landmark_list):
        temp_landmark_list = copy.deepcopy(landmark_list)

        # Convert to relative coordinates
        base_x, base_y = 0, 0
        for index, landmark_point in enumerate(temp_landmark_list):
            if index == 0:
                base_x, base_y = landmark_point[0], landmark_point[1]

            temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
            temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

        # Convert to a one-dimensional list
        temp_landmark_list = list(itertools.chain.from_iterable(temp_landmark_list))

        # Normalization
        max_value = max(list(map(abs, temp_landmark_list)))

        def normalize_(n):
            return n / max_value

        temp_landmark_list = list(map(normalize_, temp_landmark_list))

        return temp_landmark_list

    def draw_bounding_rect(self, image, brect):
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]), (255, 255, 255), 2)
        return image
