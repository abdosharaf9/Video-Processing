import cv2
import customtkinter as ctk
import detection
import merge_audio
from options import Options
from tkinter import filedialog


options_list: list[Options] = []


def choose_file_path():
    input_path.set(filedialog.askopenfilename(title="Choose Input File", filetypes=[("Video Files", ".mp4;.avi")]))
    print(f"Choosen input path = {input_path.get()}")


def choose_output_path():
    output_path.set(filedialog.askdirectory(title="Choose Output Directory") + "/filtered video temp.mp4")
    print(f"Choosen output path = {output_path.get()}")
    
    
def open_files():
    print(f"Choosen input path = {input_path.get()}")
    print(f"Choosen output path = {output_path.get()}")
    
    cap = cv2.VideoCapture(input_path.get())
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output = cv2.VideoWriter(output_path.get(), fourcc, fps, (width, height))
    return cap, fps, total_frames, output
    

def handle_option_check(option: Options):
    if option in options_list:
        options_list.remove(option)
    else:
        options_list.append(option)
    print(options_list)


def start_processing():
    if input_path.get() != None and output_path.get() != None:
        video, fps, total_frames, output = open_files()
        print("Loading.......")
        detection.parallel_process_video_each_sec(video=video, fps = fps, total_frames= total_frames, output=output, selected_options_list= options_list)
        merge_audio.merge_audio_with_video(output_path.get(), input_path.get(), output_path.get().replace(" temp.mp4", ".mp4"))
        print("Finished")
        #window.destroy()



######################################################################
#                           Main Code                                #
######################################################################


window = ctk.CTk()
window.title("Video Processing")
window.geometry("650x700")
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

# Filters
unsharp_masking_cb = ctk.CTkCheckBox(master= options_frame, text= "Unsharp Masking", border_width=1, command=lambda: handle_option_check(Options.UNSHARPEN))
unsharp_masking_cb.grid(pady=8, row=0, column=0, sticky="w")

blur_cb = ctk.CTkCheckBox(master= options_frame, text= "Blur", border_width=1, command=lambda: handle_option_check(Options.BLUR))
blur_cb.grid(pady=8, row=1, column=0, sticky="w")

edge_detection_cb = ctk.CTkCheckBox(master= options_frame, text= "Edge Detection (Laplacian)", border_width=1, command=lambda: handle_option_check(Options.EDGE_DETECTION))
edge_detection_cb.grid(pady=8, row=2, column=0, sticky="w")

sharpen_cb = ctk.CTkCheckBox(master= options_frame, text= "Sharpen", border_width=1, command=lambda: handle_option_check(Options.SHARPEN))
sharpen_cb.grid(pady=8, row=3, column=0, sticky="w")

emboss_cb = ctk.CTkCheckBox(master= options_frame, text= "Emboss", border_width=1, command=lambda: handle_option_check(Options.EMBOSS))
emboss_cb.grid(pady=8, row=4, column=0, sticky="w")

gaussian_blur_cb = ctk.CTkCheckBox(master= options_frame, text= "Gaussian Blur", border_width=1, command=lambda: handle_option_check(Options.GAUSSIAN_BLUR))
gaussian_blur_cb.grid(pady=8, row=5, column=0, sticky="w")

black_and_white_cb = ctk.CTkCheckBox(master= options_frame, text= "Black And White", border_width=1, command=lambda: handle_option_check(Options.BLACK_AND_WHITE))
black_and_white_cb.grid(pady=8, row=6, column=0, sticky="w")

night_vision_filter_cb = ctk.CTkCheckBox(master= options_frame, text= "Night Vision (Cool)", border_width=1, command=lambda: handle_option_check(Options.NIGHT_VISION))
night_vision_filter_cb.grid(pady=8, row=7, column=0, sticky="w")

sepia_cb = ctk.CTkCheckBox(master= options_frame, text= "Sepia (Warm)", border_width=1, command=lambda: handle_option_check(Options.SEPIA))
sepia_cb.grid(pady=8, row=8, column=0, sticky="w")


# Detections
face_cb = ctk.CTkCheckBox(master= options_frame, text= "Face Detection", border_width=1, command=lambda: handle_option_check(Options.FACE_DETECTION))
face_cb.grid(pady=8, row=0, column=1, sticky="w")

age_cb = ctk.CTkCheckBox(master= options_frame, text= "Age Detection", border_width=1, command=lambda: handle_option_check(Options.AGE))
age_cb.grid(pady=8, row=1, column=1, sticky="w")

gender_cb = ctk.CTkCheckBox(master= options_frame, text= "Gender Detection", border_width=1, command=lambda: handle_option_check(Options.GENDER))
gender_cb.grid(pady=8, row=2, column=1, sticky="w")


# Start Button
start_btn = ctk.CTkButton(master= frame_1, text= "Start", command=start_processing, font=("Roboto", 16), height=30)
start_btn.pack(padx=100, pady=20)


window.mainloop()