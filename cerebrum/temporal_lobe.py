# Responsible for auditory processing (e.g. listening)
#SERVICE_ACCOUNT_FILE = '/graym-426618-3e2d718be5f8.json'

import os
import io
from google.cloud import speech
from google.oauth2 import service_account
import speech_recognition as sr

class TemporalLobe:
    def __init__(self, frontal_lobe=None, use_voice=True):
        self.frontal_lobe = frontal_lobe
        self.use_voice = use_voice

    def process_speech_input(self):
        # Path to your service account key JSON file
        SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'graym-426618-3e2d718be5f8.json')

        # Set up Google Cloud client with credentials
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        client = speech.SpeechClient(credentials=credentials)

        # Capture audio from microphone using SpeechRecognition
        recognizer = sr.Recognizer()

        while True:
            with sr.Microphone() as source:
                print("Say something:")
                audio = recognizer.listen(source)
                sample_rate = source.SAMPLE_RATE  # Get the sample rate from the microphone source

            # Save audio to a temporary file
            with open("temp_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())

            # Read the audio file
            with io.open("temp_audio.wav", "rb") as audio_file:
                content = audio_file.read()

            # Configure audio settings
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sample_rate,
                language_code="en-US"
            )

            # Perform speech recognition
            response = client.recognize(config=config, audio=audio)

            # Process the results
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "

            # Clean up the temporary file
            os.remove("temp_audio.wav")

            # Output the transcript
            if self.frontal_lobe and self.use_voice:
                #self.frontal_lobe.speak(transcript.strip())
                print("Transcript:", transcript.strip())
            else:
                print("Transcript:", transcript.strip())

            return transcript.strip()

if __name__ == "__main__":
    temporal_lobe = TemporalLobe(use_voice=False)  # Set use_voice to False for testing without voice output
    while True:
        processed_data = temporal_lobe.process_speech_input()
        print("Processed data:", processed_data)


