from gtts import gTTS

def synthesize_speech(text, output_audio_path):
    # Create a gTTS object
    tts = gTTS(text=text, lang='en')

    # Save the audio to a file
    tts.save(output_audio_path)
    print(f"Audio content written to file {output_audio_path}")

# Example usage
if __name__ == "__main__":
    text = "This is a Reddit post about the latest technology trends."
    output_path = "audio/reddit_post.mp3"
    synthesize_speech(text, output_path)
