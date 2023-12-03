import cv2
import concurrent.futures
import numpy as np

def process_frame(frame):
    # Apply your processing scheme to the frame
    # Replace the following line with your processing code
    #processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Unsharp Masking
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    processed_frame = cv2.filter2D(frame, -1, kernel)
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
output_video_path = "C:\\Users\\ziad2\\Desktop\\Video-Processing-main\\output.mp4"
#parallel_process_video_all_frames(input_video_path, output_video_path)
parallel_process_video_each_sec(input_video_path, output_video_path)