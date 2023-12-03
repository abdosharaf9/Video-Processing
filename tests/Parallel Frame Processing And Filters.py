import cv2
import concurrent.futures
import numpy as np


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

# Gaussian  Blur Kernel
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
def night_vision_filter(frame):
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

def process_frame(frame):
    # Apply your processing scheme to the frame
    processed_frame=frame
    #processed_frame = unsharp_masking(processed_frame)
    #processed_frame = blur(processed_frame)
    #processed_frame = edge_detection(processed_frame)
    #processed_frame = sharpen(processed_frame)
    #processed_frame = emboss(processed_frame)
    #processed_frame = gaussian_blur(processed_frame)
    #processed_frame = black_and_white(processed_frame) 
    #processed_frame = night_vision_filter(processed_frame) 
    #processed_frame = sepia(processed_frame)
    return processed_frame

def parallel_process_video_all_frames(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Read all frames
        frames = [cap.read()[1] for _ in range(total_frames)]

        # Process frames in parallel, independently for each second
        processed_frames = list(executor.map(process_frame, frames))

        # Write processed frames to output video
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
        for frame in processed_frames:
            out.write(frame)

        out.release()

    cap.release()

def parallel_process_video_each_sec(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        processed_frames = []

        # Iterate through each second
        for second in range(0, total_frames // fps):
            start_frame = second * fps
            end_frame = start_frame + fps

            # Read frames for the current second
            frames = [cap.read()[1] for _ in range(start_frame, end_frame)]

            # Process frames in parallel
            processed_frames.extend(list(executor.map(process_frame, frames)))

        # Write processed frames to output video
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
        for frame in processed_frames:
            out.write(frame)
        
        out.release()

    cap.release()

# Example usage
input_video_path = "C:\\Users\\ziad2\\Desktop\\Video-Processing-main\\test.mp4"
output_video_path = "C:\\Users\\ziad2\\Desktop\\Video-Processing-main\\output without audio.mp4"
#parallel_process_video_all_frames(input_video_path, output_video_path)
parallel_process_video_each_sec(input_video_path, output_video_path)