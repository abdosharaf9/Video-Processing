import cv2
import tkinter as tk
import threading
from tkinter import filedialog

file_path: str = None
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def chooseFile():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Video files", ".mp4;.avi")])
    print(f"Path = {file_path}")

def apply_filter(frame):
    # Example filter: Convert frame to grayscale
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def process_file():
    cap = cv2.VideoCapture(file_path)

    # # Get video properties
    # fps = int(cap.get(cv2.CAP_PROP_FPS))
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # # Create VideoWriter object to save the filtered video
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # output_path = "filtered_video.mp4"
    # out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)  # Set isColor=False for grayscale

    # process1 = threading.Thread(target= process_frames(cap, out))
    # process1.start()
    # process1.join()

    process_video(cap)
    
    cap.release()
    # out.release()
    cv2.destroyAllWindows()


def process_frames(video, output):
     # Process each frame in the video
    while True:
        ret, frame = video.read()

        if not ret: break

        filtered_frame = apply_filter(frame)

        # Display the filtered frame
        cv2.imshow('Filtered Video', filtered_frame)

        # Write the filtered frame to the output video file
        output.write(filtered_frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'): break


def process_video(video):
    while video.isOpened():
        ret, frame = video.read()
        if not ret: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the frame with face detection
        cv2.imshow('Face Detection', frame)


if __name__ == "__main__":
    window = tk.Tk()
    window.geometry("600x600")


    btn = tk.Button(master=window, text="Browse Files", width=30, background="light blue", command=chooseFile)
    btn.pack()


    btn = tk.Button(master=window, text="Start", width=30, background="light blue", command=process_file)
    btn.pack()


    window.mainloop()