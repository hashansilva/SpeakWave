import speech_recognition as speech_recognition
from googletrans import Translator, LANGUAGES
from pydub import AudioSegment

def convert_audio_to_wav(input_file, output_file='converted.wav'):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format='wav')
    return output_file

def speech_to_text(audio_file_path):
    recognizer = speech_recognition.Recognizer()
    translator = Translator()

    audio_file = convert_audio_to_wav(audio_file_path)

    with speech_recognition.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, show_all=True)
        if not text or 'alternative' not in text:
            print("No transcript could be detected")
            return

        final_text = []
        for alt in text['alternative']:
            detected_text = alt['transcript']
            detected_language = translator.detect(detected_text).lang
            
            if detected_language != 'en':
                translated_text = translator.translate(detected_text, sr=detected_language ,dest='en').text
                final_text.append("f{translated_text} ({detected_text})")
            else:
                final_text.append(detected_text)
        print ("\nTranscript:")
        print(" ".join(final_text))
    except speech_recognition.UnknownValueError:
        print("Google Web Speech API could not understand the audio")
        return 'Unable to recognize speech', ''
    except speech_recognition.RequestError as error:
        print(f"Could not request results from Google Web Speech API; {error}")
        return 'Unable to recognize speech', ''

file_path = 'test.m4a'  # Replace with your file path
speech_to_text(file_path)