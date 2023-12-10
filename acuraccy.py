import cv2

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
gender_list = ['Male', 'Female']
font = cv2.FONT_HERSHEY_SIMPLEX


# Load pre-trained age and gender prediction models
age_net = cv2.dnn.readNetFromCaffe('data/deploy_age.prototxt', 'data/age_net.caffemodel')
gender_net = cv2.dnn.readNetFromCaffe('data/deploy_gender.prototxt', 'data/gender_net.caffemodel')
face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def process_face(face):
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


def process_frame(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.equalizeHist(gray_frame)
    faces = face_cascade.detectMultiScale(image=gray_frame, scaleFactor=1.1, minNeighbors=7)
    
    futures = []

    # Process each detected face
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        face_img = frame[y:y + h, x:x + w].copy()

        # Process face image and detect age & gender
        futures.append(process_face(face_img))

    # Retrieve results from the futures
    for future, (x, y, w, h) in zip(futures, faces):
        gender, age = future
        overlay_text = "%s %s" % (gender, age)
        print(overlay_text)
        frame = cv2.putText(frame, overlay_text, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
    return frame


# height = image.shape[0]
# width = image.shape[1]
# ratio = height/width

# if height > 720:
#     height = 720
#     width = int(height / ratio)

# print(image.shape)
# image_resized = cv2.resize(image, (width, height))
# cv2.imshow("output", process_frame(image_resized))
# image = cv2.imread("./images/train/51-60/11.jpg")
image = cv2.imread("../images/test9.jpg")
processed_image = process_frame(image)
cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.imshow("output", processed_image)
cv2.waitKey(0)