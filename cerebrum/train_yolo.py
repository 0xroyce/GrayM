# train_yolo.py
from ultralytics import YOLO
import os
import yaml
import torch

def train_yolo_model(data_dir, model_output_dir, epochs=100):
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

    # Use YOLOv8n model
    model = YOLO('yolov8n.pt')

    # Determine the device
    if torch.cuda.is_available():
        num_gpus = torch.cuda.device_count()
        if num_gpus > 1:
            print(f"Using {num_gpus} GPUs")
            device = [f'cuda:{i}' for i in range(num_gpus)]
        else:
            print("Using single GPU")
            device = 'cuda:0'
    elif torch.backends.mps.is_available():
        device = 'mps'  # Use MPS for Mac M1/M3
        print("Using MPS (Metal Performance Shaders)")
    else:
        device = 'cpu'
        print("Using CPU")

    # Adjust batch size based on device and number of GPUs
    base_batch_size = 16
    if isinstance(device, list):
        batch_size = base_batch_size * len(device)
    elif device.startswith('cuda'):
        batch_size = base_batch_size * 2
    else:
        batch_size = base_batch_size

    print(f"Using batch size: {batch_size}")

    results = model.train(
        data=data_file_path,
        epochs=epochs,
        imgsz=640,
        batch=batch_size,
        name='custom_petr_model',
        patience=20,
        save=True,
        save_period=10,
        device=device,
        lr0=0.01,
        lrf=0.001,
        warmup_epochs=3,
        cos_lr=True,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,
        degrees=10,
        translate=0.1,
        scale=0.5,
        fliplr=0.5,
        mosaic=1.0,
        amp=True,  # Enable mixed precision training
        cache=True,  # Cache images for faster training
        workers=8,  # Increase number of workers for data loading
        project=model_output_dir,
        plots=True,  # Generate training plots
        exist_ok=True,  # Overwrite existing project folder
        multi_scale=True,  # Enable multi-scale training
        sync_bn=True if isinstance(device, list) else False,  # Sync BatchNorm for multi-GPU training
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
    train_yolo_model(data_dir, model_output_dir, epochs=100)