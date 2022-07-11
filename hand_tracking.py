import cv2
import mediapipe as mp

from constants import *


class HandDetector:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.hands_mp = mp.solutions.hands
        self.hands = self.hands_mp.Hands(static_image_mode=False, min_detection_confidence=0.7,
                                         min_tracking_confidence=0.7, max_num_hands=2)

        self.player1 = 0
        self.player2 = 0

    def getNewPositions(self):
        _, img = self.cap.read()
        image_height, image_width, _ = img.shape
        results = self.hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks != None:

            for hand_landmarks in results.multi_hand_landmarks:
                xPos = hand_landmarks.landmark[self.hands_mp.HandLandmark.INDEX_FINGER_TIP].x
                yPos = hand_landmarks.landmark[self.hands_mp.HandLandmark. INDEX_FINGER_TIP].y

                if xPos > 0.5:
                    self.player1 = yPos
                else:
                    self.player2 = yPos

            print(f"Player 1: {self.player1}\nPlayer 2: {self.player2}")

        # Display the image
        if SHOW_CAMERA:
            cv2.line(img, (image_width//2, 0), (image_width//2, image_height), (255, 0, 255))
            cv2.imshow('Pong Controls', cv2.flip(img, 1))

        return self.player1, self.player2
