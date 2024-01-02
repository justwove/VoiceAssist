import speech_recognition as sr
from subprocess import run, PIPE
import os

def rename_file(file_path):
    # Get the directory and filename from the file path
    directory, filename = os.path.split(file_path)

    # Replace spaces with underscores in the filename
    new_filename = filename.replace(' ', '_')

    # Create the new file path with the renamed filename
    new_file_path = os.path.join(directory, new_filename)

    # Rename the file
    os.rename(file_path, new_file_path)
    return new_file_path

def create_subtitles_with_ai(file_path, language=["fr", 'fr-FR']):
    # Code to process the video or audio file and generate subtitles using AI
    R = sr.Recognizer()
    
    file_path = rename_file(file_path)

    if file_path.endswith('.mp3'):
        run(f'ffmpeg -i {file_path} -acodec pcm_s16le -ac 1 -ar 16000 {file_path.replace(".mp3", ".wav")}'.split(' '), stdout=PIPE)
    elif file_path.endswith('.mp4'):
        run(f'ffmpeg -i {file_path} -vn -acodec pcm_s16le -ac 1 -ar 16000 {file_path.replace(".mp4", ".wav")}'.split(' '), stdout=PIPE)
    file_path = file_path.replace('.mp4', '.wav').replace('.mp3', '.wav')
    with sr.AudioFile(file_path) as source:
        audio = R.record(source)  # Read the entire audio file

    try:
        print('Processing audio file with OpenAI Whisper...')
        text_whisper = R.recognize_whisper(audio, 'large', language=language[0])  
        print('Processing audio file with Google Speech Recognition...')
        text_legacy_google = R.recognize_google(audio, language=language[1]) # Use Google Speech Recognition API to convert audio to text
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

    # Return the generated subtitles
    return {
        'text_whisper': text_whisper,
        'text_legacy_google': text_legacy_google
    }

dict = create_subtitles_with_ai('./MAX AP KARTHUS INSTANT ONE SHOT.mp4')

print('\n\n'.join([f'{key}: {value}\n' for key, value in dict.items()]))

