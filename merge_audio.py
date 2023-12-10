from moviepy.editor import VideoFileClip, AudioFileClip
import os

def merge_audio_with_video(video_path_without_audio, video_path_with_audio, output_path):
    # Load video without audio
    video_without_audio = VideoFileClip(video_path_without_audio)
    
    # Load audio from the video with audio
    audio_clip = AudioFileClip(video_path_with_audio)
    
    # Set the audio of the video without audio to the loaded audio
    video_with_audio = video_without_audio.set_audio(audio_clip)

    # Write the merged video to the output path
    video_with_audio.write_videofile(output_path, codec='libx264', audio_codec='aac', bitrate='1000k')

    os.remove(video_path_without_audio)
    
    # Close the video clips
    video_without_audio.close()
    video_with_audio.close()
    audio_clip.close()