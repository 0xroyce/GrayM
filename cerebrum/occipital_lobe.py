# cerebrum/occipital_lobe.py

import os
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'  # To suppress the macOS warning

from ultralytics import YOLO
import cv2
import logging
import yaml

# Disable logging
logging.getLogger("ultralytics").setLevel(logging.CRITICAL)

# Try to import FrontalLobe, if it fails, create a mock class
try:
    from frontal_lobe import FrontalLobe
except ImportError:
    print("Warning: FrontalLobe not imported. Running in standalone mode.")
    class FrontalLobe:
        def __init__(self, sensory_data):
            pass
        def generate_response(self, prompt):
            return "Mock response"
        def speak(self, text):
            print(f"Mock speak: {text}")

class OccipitalLobe:
    def __init__(self, custom_model_path='trained_model/best_model.pt', data_yaml_path='yolo_dataset/data.yaml'):
        # Load custom model
        if os.path.exists(custom_model_path):
            self.custom_model = YOLO(custom_model_path)
            print(f"Custom model loaded from: {custom_model_path}")
            print(f"Custom model task: {self.custom_model.task}")
            print(f"Custom model names: {self.custom_model.names}")
        else:
            print(f"Custom model not found at {custom_model_path}. Using only pre-trained model.")
            self.custom_model = None

        # Load pre-trained model
        self.pretrained_model = YOLO('yolov8n.pt')
        print("Pre-trained YOLOv8n model loaded")
        print(f"Pre-trained model names: {self.pretrained_model.names}")

        # Load custom names from data.yaml
        if os.path.exists(data_yaml_path):
            with open(data_yaml_path, 'r') as f:
                data_yaml = yaml.safe_load(f)
            self.custom_names = data_yaml.get('names', ['petr'])
        else:
            self.custom_names = ['petr']
        print(f"Loaded custom class names: {self.custom_names}")

        # Initialize FrontalLobe
        self.frontal_lobe = FrontalLobe(sensory_data={})

    def process_visual_input(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        petr_detected = False

        while True:
            success, img = cap.read()
            if not success:
                print("Failed to grab frame")
                break

            # Run inference with custom model
            if self.custom_model:
                custom_results = self.custom_model(img, conf=0.1, imgsz=640)
                self.draw_results(img, custom_results, self.custom_model.names, color=(255, 0, 0))

                # Check for petr detection
                petr_detected_now = any(self.custom_model.names[int(box.cls[0])] == 'petr' for box in custom_results[0].boxes)
                if petr_detected_now and not petr_detected:
                    print("petr detected")
                    petr_detected = True
                    # Generate and speak greeting
                    greeting = self.frontal_lobe.generate_response("Generate a short greeting for petr who just appeared.")
                    print(f"Generated greeting: {greeting}")
                    self.frontal_lobe.speak(greeting)
                elif not petr_detected_now:
                    petr_detected = False

            # Run inference with pre-trained model
            pretrained_results = self.pretrained_model(img, conf=0.25, imgsz=640)
            self.draw_results(img, pretrained_results, self.pretrained_model.names, color=(0, 255, 0))

            cv2.imshow('Webcam', img)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def draw_results(self, img, results, names, color):
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                confidence = box.conf[0].item()
                cls = int(box.cls[0])
                class_name = names[cls] if cls < len(names) else f"Unknown ({cls})"
                label = f"{class_name} {confidence:.2f}"
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    def test_custom_model(self, test_image_path):
        if self.custom_model:
            if os.path.exists(test_image_path):
                img = cv2.imread(test_image_path)
                results = self.custom_model(img, conf=0.1)
                print(f"Test image results: {results}")
                self.draw_results(img, results, self.custom_model.names, color=(255, 0, 0))
                cv2.imshow('Test Image', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print(f"Test image not found at {test_image_path}")

if __name__ == "__main__":
    custom_model_path = 'runs/detect/custom_petr_model/weights/best.pt'
    data_yaml_path = 'yolo_dataset/data.yaml'
    test_images = False  # Set this to True if you want to run image tests

    try:
        occipital_lobe = OccipitalLobe(custom_model_path=custom_model_path, data_yaml_path=data_yaml_path)

        if test_images:
            # Test on multiple images
            test_image_paths = ['captured_images/petr_001.jpg', 'captured_images/petr_100.jpg', 'captured_images/petr_200.jpg']
            for img_path in test_image_paths:
                print(f"\nTesting on image: {img_path}")
                occipital_lobe.test_custom_model(img_path)

        print("\nStarting live video feed...")
        occipital_lobe.process_visual_input()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")