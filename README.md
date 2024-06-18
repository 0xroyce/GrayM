# GrayM Project

The GrayM Project aims to simulate the main parts of the brain and their functionalities using Python, with the ultimate goal of creating an Artificial Intelligence brain. The project is organized into different modules, each representing a distinct part of the brain.

## Project Structure

```
brain_project/
│
├── cerebrum/
│   ├── __init__.py
│   ├── frontal_lobe.py
│   ├── parietal_lobe.py
│   ├── temporal_lobe.py
│   └── occipital_lobe.py
│
├── cerebellum/
│   ├── __init__.py
│   └── cerebellum.py
│
├── brainstem/
│   ├── __init__.py
│   ├── midbrain.py
│   ├── pons.py
│   └── medulla_oblongata.py
│
├── thalamus/
│   ├── __init__.py
│   └── thalamus.py
│
├── hypothalamus/
│   ├── __init__.py
│   └── hypothalamus.py
│
├── limbic_system/
│   ├── __init__.py
│   ├── hippocampus.py
│   └── amygdala.py
│
├── basal_ganglia/
│   ├── __init__.py
│   └── basal_ganglia.py
│
├── memory/
│   ├── __init__.py
│   └── memory_storage.py
│
├── image_storage/
│   ├── __init__.py
│   └── image_handler.py
│
├── main.py
└── README.md
```


## Module Responsibilities

### Cerebrum
The cerebrum is divided into four lobes, each responsible for different high-level brain functions.

- **Frontal Lobe (`cerebrum/frontal_lobe.py`)**
  - Reasoning
  - Planning
  - Problem-solving
  - Voluntary movement control

- **Parietal Lobe (`cerebrum/parietal_lobe.py`)**
  - Processing sensory information (touch, temperature, pain)
  - Spatial orientation

- **Temporal Lobe (`cerebrum/temporal_lobe.py`)**
  - Auditory processing
  - Memory
  - Speech comprehension

- **Occipital Lobe (`cerebrum/occipital_lobe.py`)**
  - Visual processing

### Cerebellum (`cerebellum/cerebellum.py`)
- Coordination of voluntary movements
- Balance and posture
- Speech coordination

### Brainstem
The brainstem connects the brain to the spinal cord and manages basic life functions.

- **Midbrain (`brainstem/midbrain.py`)**
  - Vision
  - Hearing
  - Eye movement
  - Body movement

- **Pons (`brainstem/pons.py`)**
  - Breathing control
  - Communication between brain parts
  - Sensations (hearing, taste, balance)

- **Medulla Oblongata (`brainstem/medulla_oblongata.py`)**
  - Autonomic functions (breathing, heart rate, blood pressure)

### Thalamus (`thalamus/thalamus.py`)
- Relay station for sensory and motor signals to the cerebral cortex
- Regulation of consciousness, sleep, and alertness

### Hypothalamus (`hypothalamus/hypothalamus.py`)
- Temperature regulation
- Hunger and thirst control
- Sleep and emotional activity regulation
- Controls the pituitary gland (link between nervous and endocrine systems)

### Limbic System
The limbic system manages emotions and memory.

- **Hippocampus (`limbic_system/hippocampus.py`)**
  - Formation of new memories
  - Learning processes

- **Amygdala (`limbic_system/amygdala.py`)**
  - Emotion regulation (fear and pleasure responses)

### Basal Ganglia (`basal_ganglia/basal_ganglia.py`)
- Regulation of voluntary motor movements
- Procedural learning
- Routine behaviors or habits

### Memory (`memory/memory_storage.py`)
- Stores and retrieves learned data
- Uses SQLite for data persistence

### Image Storage (`image_storage/image_handler.py`)
- Stores images for future recognition
- Uses OpenCV for image recognition
- Uses Pillow for image handling

## Getting Started

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    ```

2. **Run the main script:**
    ```sh
    python main.py
    ```

3. **Explore the modules:**
    - Each module can be extended with additional functions to simulate more detailed behaviors of the respective brain parts.


4. **Add your Google Cloud JSON file to cerebrum/ folder**
   - Generate your Google Cloud JSON file for Speech to Text and Text to Speech and add it to /cerebrum folder. Then update temporal_lobe.py with name of your file.

## Contributions

Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

## License

This project is licensed under the MIT License. See the LICENSE file for details.