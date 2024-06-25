# train_yolo.py
from ultralytics import YOLO
import os
import yaml

def train_yolo_model(data_dir, model_output_dir, epochs=200):
    data_file_path = os.path.abspath(os.path.join(data_dir, "data.yaml"))
    if not os.path.exists(data_file_path):
        raise FileNotFoundError(f"{data_file_path} does not exist. Make sure to prepare the dataset first.")

    # Print the contents of data.yaml
    with open(data_file_path, 'r') as file:
        data_yaml = yaml.safe_load(file)
        print("Loaded data.yaml:")
        print(data_yaml)

    # Verify the dataset structure
    train_path = os.path.join(data_dir, data_yaml['train'])
    val_path = os.path.join(data_dir, data_yaml['val'])
    print(f"Number of training images: {len(os.listdir(train_path))}")
    print(f"Number of validation images: {len(os.listdir(val_path))}")

    model = YOLO('yolov8n.pt')  # Start with a pre-trained model
    results = model.train(
        data=data_file_path,
        epochs=300,  # Increase epochs since we have more data
        imgsz=640,
        batch=16,
        name='custom_petr_model',
        patience=50,
        save=True,
        save_period=10,
        device='cpu',  # Use 'cuda:0' if you have a compatible GPU
        lr0=0.01,
        lrf=0.001,
        warmup_epochs=5,
        cos_lr=True,
        hsv_h=0.015,  # Hue augmentation
        hsv_s=0.7,  # Saturation augmentation
        hsv_v=0.4,  # Value augmentation
        degrees=10,  # Rotation augmentation
        translate=0.1,  # Translation augmentation
        scale=0.5,  # Scale augmentation
        fliplr=0.5,  # Horizontal flip
        mosaic=1.0  # Mosaic augmentation
    )

    # The best model is automatically saved during training
    best_model_path = os.path.join(model_output_dir, 'custom_petr_model', 'weights', 'best.pt')
    if os.path.exists(best_model_path):
        print(f"Training completed. Best model saved to {best_model_path}")
    else:
        print("Training completed, but best model file not found at the expected location.")

    # Print final metrics
    print("Final training metrics:")
    if hasattr(results, 'maps'):
        print(f"mAP: {results.maps}")
    else:
        print("mAP information not available")

    # Print all available attributes of the results object
    print("\nAll available results attributes:")
    for attr in dir(results):
        if not attr.startswith('_'):
            try:
                value = getattr(results, attr)
                print(f"{attr}: {value}")
            except Exception as e:
                print(f"{attr}: Error accessing attribute - {str(e)}")

if __name__ == "__main__":
    data_dir = "yolo_dataset"
    model_output_dir = "runs/detect"
    train_yolo_model(data_dir, model_output_dir, epochs=200)