import cv2
import numpy as np
from options import Options

# Unsharp Masking Kernel
def unsharp_masking(frame):
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    processed_frame = cv2.filter2D(frame, -1, kernel)
    return processed_frame
    
    
# Blur Kernel
def blur(frame):
    kernel = np.array([[1/9, 1/9, 1/9],
                       [1/9, 1/9, 1/9],
                       [1/9, 1/9, 1/9]])
    processed_frame = cv2.filter2D(frame, -1, kernel)
    return processed_frame


# Edge Detection Kernel (Laplacian)
def edge_detection(frame):
    kernel = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]])
    processed_frame = cv2.filter2D(frame, -1, kernel)
    return processed_frame


# Sharpen Kernel
def sharpen(frame):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    processed_frame = cv2.filter2D(frame, -1, kernel)
    return processed_frame


# Emboss Kernel
def emboss(frame):
    kernel = np.array([[-2, -1, 0],
                       [-1,  1, 1],
                       [ 0,  1, 2]])
    processed_frame = cv2.filter2D(frame, -1, kernel)
    return processed_frame


# Gaussian Blur Kernel
def gaussian_blur(frame):
    kernel = np.array([[1/16, 1/8, 1/16],
                       [1/8, 1/4, 1/8],
                       [1/16, 1/8, 1/16]])
    processed_frame = cv2.filter2D(frame, -1, kernel)
    return processed_frame


# Black And White Kernel
def black_and_white(frame):
    processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_GRAY2BGR)
    return processed_frame


# Night Vision Kernel (Cool)
def night_vision(frame):
    kernel = np.array([[0.393, 0.769, 0.189],
                       [0.349, 0.686, 0.168],
                       [0.272, 0.534, 0.131]])
    processed_frame = cv2.transform(frame, kernel)
    return processed_frame


# Sepia Kernel (Warm)
def sepia(frame):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    processed_frame = cv2.transform(frame, kernel)
    return processed_frame

def filter_frame(frame, options_list: list[Options]):
    # Apply your processing scheme to the frame
    processed_frame=frame
    if Options.UNSHARPEN in options_list: processed_frame = unsharp_masking(processed_frame)
    if Options.BLUR in options_list: processed_frame = blur(processed_frame)
    if Options.EDGE_DETECTION in options_list: processed_frame = edge_detection(processed_frame)
    if Options.SHARPEN in options_list: processed_frame = sharpen(processed_frame)
    if Options.EMBOSS in options_list: processed_frame = emboss(processed_frame)
    if Options.GAUSSIAN_BLUR in options_list: processed_frame = gaussian_blur(processed_frame)
    if Options.BLACK_AND_WHITE in options_list: processed_frame = black_and_white(processed_frame)
    if Options.NIGHT_VISION in options_list: processed_frame = night_vision(processed_frame)
    if Options.SEPIA in options_list: processed_frame = sepia(processed_frame)
    return processed_frame