import cv2
import customtkinter as ctk
from tkinter import filedialog
from enum import Enum

class Options(Enum):
    FACE = 1,
    AGE = 2,
    GENDER = 3,
    FILTERS = 4


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
options_list: list[Options] = []


def choose_file_path():
    input_path.set(filedialog.askopenfilename(title="Choose Input File", filetypes=[("Video Files", ".mp4;.avi")]))
    print(f"Choosen input path = {input_path.get()}")


def choose_output_path():
    output_path.set(filedialog.askdirectory(title="Choose Output Directory") + "/filtered video.mp4")
    print(f"Choosen output path = {output_path.get()}")
    
    
def open_files():
    print(f"Choosen input path = {input_path.get()}")
    print(f"Choosen output path = {output_path.get()}")
    
    cap = cv2.VideoCapture(input_path.get())
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter(output_path.get(), fourcc, fps, (width, height), isColor=False)
    return cap, output


def process_frames(video: cv2.VideoCapture, output: cv2.VideoWriter):
    while True:
        ret, frame = video.read()
        
        if not ret: break
        if cv2.waitKey(1) & 0xFF == ord('q'): break
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Real Time Video Processing", gray_frame)
        output.write(gray_frame)
        
    video.release()
    output.release()
    
    cv2.destroyAllWindows()
    is_processing = False
    

def set_user_options():
    options_list.append(Options.AGE)
    options_list.append(Options.FACE)
    options_list.append(Options.GENDER)
    options_list.append(Options.FILTERS)
    
    
def handle_face_check():
    if Options.FACE in options_list:
        options_list.remove(Options.FACE)
        print(options_list)
    else:
        options_list.append(Options.FACE)
        print(options_list)
    
    
def handle_age_check():
    if Options.AGE in options_list:
        options_list.remove(Options.AGE)
        print(options_list)
    else:
        options_list.append(Options.AGE)
        print(options_list)
    
    
def handle_gender_check():
    if Options.GENDER in options_list:
        options_list.remove(Options.GENDER)
        print(options_list)
    else:
        options_list.append(Options.GENDER)
        print(options_list)
    
    
def handle_filters_check():
    if Options.FILTERS in options_list:
        options_list.remove(Options.FILTERS)
        print(options_list)
    else:
        options_list.append(Options.FILTERS)
        print(options_list)



def start_processing():
    if input_path.get() != None and output_path.get() != None:
        video, output = open_files()
        process_frames(video, output)



######################################################################
#                           Main Code                                #
######################################################################


window = ctk.CTk()
window.title("Video Processing")
window.geometry("700x450")
window.resizable(width=False, height=False)

frame_1 = ctk.CTkFrame(master=window, width=500, height=300)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = ctk.CTkLabel(master=frame_1, text="Video Processing System", font=("Roboto", 30))
label_1.pack(pady=14, padx=10)


# Input 
input_label = ctk.CTkLabel(master=frame_1, text="Input Path", anchor="w", font=("Roboto", 16))
input_label.pack(fill="x", padx=60)

input_frame = ctk.CTkFrame(master=frame_1, fg_color="transparent")
input_frame.pack(padx=60, fill="x", expand=True)
input_frame.columnconfigure(index=0, weight=3)
input_frame.columnconfigure(index=1, weight=1)


input_path = ctk.StringVar()
input_entry = ctk.CTkEntry(master=input_frame, placeholder_text="Input Path", textvariable=input_path)
input_entry.grid(row=0, column=0, sticky="ew")

input_btn = ctk.CTkButton(master= input_frame, text= "Browse", command=choose_file_path, width=50)
input_btn.grid(row=0, column=1)


# Output 
input_label = ctk.CTkLabel(master=frame_1, text="Output Path", anchor="w", font=("Roboto", 16))
input_label.pack(fill="x", padx=60)

output_frame = ctk.CTkFrame(master=frame_1, fg_color="transparent")
output_frame.pack(padx=60, fill="x", expand=True)
output_frame.columnconfigure(index=0, weight=3)
output_frame.columnconfigure(index=1, weight=1)

output_path = ctk.StringVar()
output_entry = ctk.CTkEntry(master=output_frame, placeholder_text="Output Path", textvariable=output_path)
output_entry.grid(row=0, column=0, sticky="ew")

output_btn = ctk.CTkButton(master= output_frame, text= "Browse", command=choose_output_path, width=50)
output_btn.grid(row=0, column=1)


# Options
options_frame = ctk.CTkFrame(master=frame_1, fg_color="transparent")
options_frame.pack(pady=8, padx=60, fill="both", expand=True)
options_frame.grid_columnconfigure(index=0, weight=1)
options_frame.grid_columnconfigure(index=1, weight=1)

face_cb = ctk.CTkCheckBox(master= options_frame, text= "Face Detection", border_width=1, command=handle_face_check)
face_cb.grid(pady=14, row=0, column=0, sticky="w")

age_cb = ctk.CTkCheckBox(master= options_frame, text= "Age Detection", border_width=1, command=handle_age_check)
age_cb.grid(pady=14, row=0, column=1, sticky="w")

gender_cb = ctk.CTkCheckBox(master= options_frame, text= "Gender Detection", border_width=1, command=handle_gender_check)
gender_cb.grid(pady=14, row=1, column=0, sticky="w")

filter_cb = ctk.CTkCheckBox(master= options_frame, text= "Add Filters", border_width=1, command=handle_filters_check)
filter_cb.grid(pady=14, row=1, column=1, sticky="w")


# Start Button
start_btn = ctk.CTkButton(master= frame_1, text= "Start", command=start_processing, font=("Roboto", 16), height=30)
start_btn.pack(padx=100, pady=20, fill="x")


# choose_file_path()
# choose_output_path()
# set_user_options()

window.mainloop()