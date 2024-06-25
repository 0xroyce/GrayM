### Thalamus (`thalamus/thalamus.py`)
# Acts as a relay station for sensory and motor signals to the cerebral cortex
# Receives visual, auditory, and sensory inputs and directs them to appropriate areas for processing
# thalamus/thalamus.py

# thalamus/thalamus.py

import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from cerebrum.occipital_lobe import OccipitalLobe
from cerebrum.temporal_lobe import TemporalLobe
from cerebrum.frontal_lobe import FrontalLobe


class Thalamus:
    def __init__(self, use_voice=True):
        self.visual_input = None
        self.auditory_input = None
        self.sensory_input = None
        self.frontal_lobe = FrontalLobe(sensory_data={})

        # Correct paths for OccipitalLobe
        custom_model_path = os.path.join(project_root, 'cerebrum', 'runs', 'detect', 'custom_petr_model', 'weights',
                                         'best.pt')
        data_yaml_path = os.path.join(project_root, 'cerebrum', 'yolo_dataset', 'data.yaml')

        self.occipital_lobe = OccipitalLobe(custom_model_path=custom_model_path, data_yaml_path=data_yaml_path)
        self.temporal_lobe = TemporalLobe(frontal_lobe=self.frontal_lobe, use_voice=use_voice)

    def relay_visual_input(self):
        print("Relaying visual input to Occipital Lobe...")
        self.occipital_lobe.process_visual_input()

    def relay_auditory_input(self):
        print("Relaying auditory input to Temporal Lobe...")
        self.auditory_input = self.temporal_lobe.process_speech_input()
        return self.auditory_input

    def relay_sensory_input(self, data):
        self.sensory_input = data
        print(f"Relaying sensory input: {data}")
        return self.sensory_input

    def perform_speech(self, text):
        print("Performing speech...")
        self.frontal_lobe.speak(text)

    def generate_and_speak_response(self, prompt):
        print("Generating and performing response...")
        response = self.frontal_lobe.generate_response(prompt)
        print("Generated response:", response)
        if self.temporal_lobe.use_voice:
            self.frontal_lobe.speak(response)
        else:
            print("Response:", response)

    def process_auditory_and_generate_response(self):
        while True:
            # Relay auditory input
            print("Processing auditory input...")
            auditory_data = self.relay_auditory_input()
            print("Auditory data received:", auditory_data)

            # Generate response based on the auditory input
            self.generate_and_speak_response(auditory_data)


if __name__ == "__main__":
    thalamus = Thalamus(use_voice=True)
    thalamus.relay_visual_input()
    thalamus.perform_speech("System activated. Ready to tackle today's tasks?")
    thalamus.process_auditory_and_generate_response()
