# cerebrum/frontal_lobe.py
# Reasoning, Planning, Problem-solving, Voluntary movement control, Talking

from google.cloud import texttospeech
from google.oauth2 import service_account
import openai
from dotenv import load_dotenv
import os
import os
import tempfile
import pygame


class FrontalLobe:
    def __init__(self, sensory_data):
        self.sensory_data = sensory_data

        # Path to your service account key JSON file
        SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'graym-426618-3e2d718be5f8.json')

        # Set up Google Cloud client with credentials
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
        self.client = texttospeech.TextToSpeechClient(credentials=credentials)

        self.voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # OpenAI API key
        openai.api_key = 'your-openai-api-key'

    def reasoning(self, inputs):
        # Basic reasoning logic using sensory data
        reasoned_output = "Processed: " + " and ".join(inputs)
        print(f"Reasoning with inputs: {inputs} -> {reasoned_output}")
        return reasoned_output

    def planning(self, goal):
        # Basic planning logic
        planned_steps = f"Step 1: Analyze goal {goal}, Step 2: Develop strategy, Step 3: Execute plan"
        print(f"Planning for goal: {goal} -> {planned_steps}")
        return planned_steps

    def problem_solving(self, problem):
        # Basic problem-solving logic
        solution = f"Solved problem: {problem} using reasoning and planning"
        print(f"Solving problem: {problem} -> {solution}")
        return solution

    def control_movement(self, movement_command):
        # Basic voluntary movement control
        executed_movement = f"Executing: {movement_command}"
        print(f"Controlling movement: {movement_command} -> {executed_movement}")
        return executed_movement

    def speak(self, text):
        # Speech synthesis using Google Cloud Text-to-Speech
        input_text = texttospeech.SynthesisInput(text=text)
        response = self.client.synthesize_speech(
            input=input_text, voice=self.voice, audio_config=self.audio_config
        )

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(response.audio_content)
            tmp_file_path = tmp_file.name
            print(f"Audio content written to temporary file '{tmp_file_path}'")

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(tmp_file_path)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Remove the temporary file
        os.remove(tmp_file_path)
        print(f"Temporary file '{tmp_file_path}' deleted")

    ##Temporary LLMs implementation as an off-ramp to General Intelligence
    def generate_response(self, prompt):
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        # Generate a response using OpenAI API
        response = openai.chat.completions.create(
            model=os.getenv('LLM_MODEL'),
            messages=[{
                "role": "system",
                "content": "You're helpful agent"
            }, {
                "role": "user",
                "content": prompt
            }]
        )

        # print(response.choices[0].message.content)
        return response.choices[0].message.content


# Usage example
if __name__ == "__main__":
    frontal_lobe = FrontalLobe(sensory_data={})

    # Test speech synthesis
    frontal_lobe.speak("System activated. Ready to tackle today's tasks?")

    # Test generating a response using OpenAI API
    response = frontal_lobe.generate_response("How are you?")
    print("Generated response:", response)
    frontal_lobe.speak(response)