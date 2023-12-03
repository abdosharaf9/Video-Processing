import cv2
import concurrent.futures
import numpy as np

# Open the video file for capturing frames
# cap = cv2.VideoCapture("test.mp4")
cap = cv2.VideoCapture("test3.mp4")
# cap = cv2.VideoCapture(0)
cap.set(3, 480)  # set width
cap.set(4, 640)  # set height

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
gender_list = ['Male', 'Female']

def initialize_models():
    # Load pre-trained age and gender prediction models
    age_net = cv2.dnn.readNetFromCaffe(
        'data/deploy_age.prototxt',
        'data/age_net.caffemodel')

    gender_net = cv2.dnn.readNetFromCaffe(
        'data/deploy_gender.prototxt',
        'data/gender_net.caffemodel')

    return age_net, gender_net

def process_face(face):
    """
    Function to process gender and age prediction for a single face.
    """
    # Create a blob from the face image for input to the pre-trained models
    blob = cv2.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

    # Predict gender
    gender_net.setInput(blob)
    gender_preds = gender_net.forward()
    gender = gender_list[gender_preds[0].argmax()]

    # Predict age
    age_net.setInput(blob)
    age_preds = age_net.forward()
    age = age_list[age_preds[0].argmax()]

    return gender, age

def read_from_camera_parallel(age_net, gender_net):
    font = cv2.FONT_HERSHEY_SIMPLEX

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            # Read a frame from the video capture
            ret, image = cap.read()

            # Load the face cascade for detecting faces
            face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Detect faces in the grayscale frame
            faces = face_cascade.detectMultiScale(gray, 1.1, 7)

            # Print the number of faces found
            if len(faces) > 0:
                print("Found {} faces".format(len(faces)))

            # List to store futures (results) of face processing tasks
            futures = []

            # Process each detected face concurrently
            for (x, y, w, h) in faces:
                # Draw a rectangle around the face
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)
                face_img = image[y:y + h, x:x + w].copy()

                # Submit face processing tasks to the ThreadPoolExecutor
                futures.append(executor.submit(process_face, face_img))

            # Retrieve results from the futures
            for future, (x, y, w, h) in zip(futures, faces):
                gender, age = future.result()
                overlay_text = "%s %s" % (gender, age)
                cv2.putText(image, overlay_text, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Display the frame with rectangles and information
            cv2.imshow('frame', image)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

# Entry point of the script
if __name__ == "__main__":
    # Initialize pre-trained models
    age_net, gender_net = initialize_models()

    # Start processing frames from the camera in parallel
    read_from_camera_parallel(age_net, gender_net)