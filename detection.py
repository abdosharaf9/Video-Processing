import cv2
import concurrent.futures
import filters
from options import Options

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
gender_list = ['Male', 'Female']
font = cv2.FONT_HERSHEY_SIMPLEX
options_list: list[Options] = []


# Load pre-trained age and gender prediction models
age_net = cv2.dnn.readNetFromCaffe('data/deploy_age.prototxt', 'data/age_net.caffemodel')
gender_net = cv2.dnn.readNetFromCaffe('data/deploy_gender.prototxt', 'data/gender_net.caffemodel')
face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def process_face(face):
    # Create a blob from the face image for input to the pre-trained models
    blob = cv2.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

    output = ""
    
    # Predict gender
    if Options.GENDER in options_list:
        gender_net.setInput(blob)
        gender_preds = gender_net.forward()
        gender = gender_list[gender_preds[0].argmax()]
        output += f"{gender} "

    # Predict age
    if Options.AGE in options_list:
        age_net.setInput(blob)
        age_preds = age_net.forward()
        age = age_list[age_preds[0].argmax()]
        output += age

    return output


def process_frame(frame):
    if Options.FACE_DETECTION in options_list:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
        gray_frame = cv2.equalizeHist(gray_frame) 
        faces = face_cascade.detectMultiScale(image=gray_frame, scaleFactor=1.1, minNeighbors=7)
    
    frame = filters.filter_frame(frame= frame, options_list=options_list)
    
    if Options.FACE_DETECTION in options_list:
        futures = []

        # Process each detected face
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            face_img = frame[y:y + h, x:x + w].copy()

            # Process face image and detect age & gender
            if Options.AGE in options_list or Options.GENDER in options_list:
                futures.append(process_face(face_img))

        # Retrieve results from the futures
        if Options.AGE in options_list or Options.GENDER in options_list:
            for future, (x, y, w, h) in zip(futures, faces):
                frame = cv2.putText(frame, future, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
    return frame


def parallel_process_video_each_sec(video: cv2.VideoCapture, fps: int, total_frames: int, output: cv2.VideoWriter, selected_options_list: list[Options]):
    global options_list
    options_list = selected_options_list
    with concurrent.futures.ThreadPoolExecutor() as executor:
        processed_frames = []

        # Iterate through each second
        for second in range(0, total_frames // fps):
            start_frame = second * fps
            end_frame = start_frame + fps

            # Read frames for the current second
            frames = [video.read()[1] for _ in range(start_frame, end_frame)]

            # Process frames in parallel
            processed_frames.extend(list(executor.map(process_frame, frames)))

        for frame in processed_frames: output.write(frame)
        
    video.release()
    output.release()