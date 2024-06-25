# main.py

import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

from thalamus.thalamus import Thalamus
from memory.memory_storage import MemoryStorage
import threading

def auditory_processing_thread(thalamus):
    thalamus.process_auditory_and_generate_response()

def main(use_voice=True):
    # Initialize thalamus with the use_voice parameter
    thalamus = Thalamus(use_voice=use_voice)

    # Perform speech before processing auditory input
    thalamus.perform_speech("System activated. Ready to tackle today's tasks!")

    # Start thread for auditory processing
    auditory_thread = threading.Thread(target=auditory_processing_thread, args=(thalamus,))
    auditory_thread.start()

    # Process visual input in the main thread
    thalamus.relay_visual_input()

    # Wait for the auditory thread to complete
    auditory_thread.join()

    # Relay sensory data through thalamus and process in parietal lobe
    sensory_data = "Sensory data from skin"
    relayed_sensory = thalamus.relay_sensory_input(sensory_data)

    # Memory storage example
    memory_storage = MemoryStorage()
    memory_storage.store_learning('Learning to solve problem X')
    learning_data = memory_storage.retrieve_learning()
    print("Retrieved learning data:", learning_data)
    memory_storage.close()

if __name__ == "__main__":
    main(use_voice=True)  # Set use_voice to True or False as needed
