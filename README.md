# Hand Tracking with OpenCV and MediaPipe

A real-time hand-tracking module built using Python, OpenCV, and MediaPipe. It detects hands, tracks 21 hand landmarks, estimates raised fingers, and calculates distances between landmarks.

## Features

- Real-time hand landmark detection using a webcam
- Drawing hand landmarks and connections
- Extracting landmark coordinates and bounding boxes
- Detecting raised fingers
- Calculating distances between hand landmarks

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy

## Installation

Install the required libraries:

```bash
pip install opencv-python mediapipe numpy
```

## How to Run

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python HandTrackingModule.py
```

4. Allow access to your webcam.
5. Press `q` to close the webcam window.

## Main Functions

- `findHands()` — Detects hands and optionally draws landmarks.
- `findPosition()` — Returns landmark coordinates and a bounding box.
- `fingersUp()` — Estimates which fingers are raised.
- `findDistance()` — Calculates the distance between two landmarks.
- `box()` — Draws a bounding box around detected hands.

## Notes

A working webcam and compatible Python and MediaPipe versions are required. The finger-detection logic in this project is based on landmark positions and may need adjustment for different hand orientations.

## Author

Developed as a computer vision learning project.
