# # importing the multiprocessing module 
# import multiprocessing 
# import os 

# def worker1(): 
#     # printing process id 
#     print(f"ID of process running worker1: {os.getpid()}")
#     for _ in range(1000):
#         print("p1")
    

# def worker2(): 
#     # printing process id 
#     print(f"ID of process running worker2: {os.getpid()}")
#     for _ in range(1000):
#         print("p2")

# if __name__ == "__main__": 
#     # printing main program process id 
#     print("ID of main process: {}".format(os.getpid())) 

#     # creating processes 
#     p1 = multiprocessing.Process(target=worker1) 
#     p2 = multiprocessing.Process(target=worker2) 

#     # starting processes 
#     p1.start() 
#     p2.start() 

#     # process IDs 
#     print("ID of process p1: {}".format(p1.pid)) 
#     print("ID of process p2: {}".format(p2.pid)) 

#     # wait until processes are finished 
#     p1.join() 
#     p2.join() 

#     # both processes finished 
#     print("Both processes finished execution!") 

#     # check if processes are alive 
#     print("Process p1 is alive: {}".format(p1.is_alive())) 
#     print("Process p2 is alive: {}".format(p2.is_alive())) 



import cv2

# Function to apply a filter to a frame
def apply_filter(frame):
    # Example filter: Convert frame to grayscale
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Open the video file
video_path = "test.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter object to save the filtered video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_path = "filtered_video.mp4"
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)  # Set isColor=False for grayscale

# Process each frame in the video
while True:
    ret, frame = cap.read()

    if not ret:
        break  # Break the loop if the video is finished

    # Apply the filter to the frame
    filtered_frame = apply_filter(frame)

    # Display the filtered frame
    cv2.imshow('Filtered Video', filtered_frame)

    # Write the filtered frame to the output video file
    # out.write(filtered_frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and VideoWriter objects
cap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
