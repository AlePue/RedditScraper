from moviepy.editor import *
from os.path import join

def create_video_from_audio_and_image(audio_file, image_file, output_file):
    # Load the audio and image
    audio_clip = AudioFileClip(audio_file)
    image_clip = ImageClip(image_file)

    # Set image duration to match audio length
    image_clip = image_clip.set_duration(audio_clip.duration)

    # Set the audio to the video
    video_clip = image_clip.set_audio(audio_clip)

    # Write the video to file
    video_clip.write_videofile(output_file, fps=24)

# Example usage
if __name__ == "__main__":
    create_video_from_audio_and_image("audio/reddit_post.mp3", "images/technology_image.jpg", "output_videos/technology_video.mp4")
