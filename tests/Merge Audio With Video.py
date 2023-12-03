from moviepy.editor import VideoFileClip, AudioFileClip

def merge_video_with_audio(video_path_without_audio, video_path_with_audio, output_path):
    # Load video without audio
    video_without_audio = VideoFileClip(video_path_without_audio)
    
    # Load audio from the video with audio
    audio_clip = AudioFileClip(video_path_with_audio)
    
    # Set the audio of the video without audio to the loaded audio
    video_with_audio = video_without_audio.set_audio(audio_clip)
    
    # Write the merged video to the output path
    video_with_audio.write_videofile(output_path, codec='libx264', audio_codec='aac', bitrate='11496k')
    
    # Close the video clips
    video_without_audio.close()
    video_with_audio.close()
    audio_clip.close()

# Replace 'video1.mp4', 'video2.mp4', and 'output_video.mp4' with your actual file paths
video_path_without_audio = "C:\\Users\\ziad2\\Desktop\\Video-Processing-main\\output without audio.mp4"
video_path_with_audio = "C:\\Users\\ziad2\\Desktop\\Video-Processing-main\\test.mp4"
output_video_path = "C:\\Users\\ziad2\\Desktop\\Video-Processing-main\\output with audio.mp4"
merge_video_with_audio(video_path_without_audio, video_path_with_audio, output_video_path)