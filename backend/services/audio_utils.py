from pydub import AudioSegment
import os

def convert_to_wav(input_path, output_path):
    # Detect input format from extension
    ext = os.path.splitext(input_path)[1].lower()

    # Load file with pydub
    if ext == ".mp3":
        audio = AudioSegment.from_mp3(input_path)
    elif ext == ".mp4" or ext == ".m4a":
        audio = AudioSegment.from_file(input_path, "mp4")
    else:
        # fallback for other audio formats
        audio = AudioSegment.from_file(input_path)

    # Export audio as wav (16kHz mono recommended)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(output_path, format="wav")
    return output_path
