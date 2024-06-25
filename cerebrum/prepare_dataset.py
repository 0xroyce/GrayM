# prepare_dataset.py
import os
import shutil
import yaml


def prepare_yolo_dataset(image_dir, output_dir):
    images_output_dir = os.path.join(output_dir, "images")
    labels_output_dir = os.path.join(output_dir, "labels")
    train_dir = os.path.join(images_output_dir, "train")
    val_dir = os.path.join(images_output_dir, "val")

    for dir in [train_dir, val_dir, os.path.join(labels_output_dir, "train"), os.path.join(labels_output_dir, "val")]:
        os.makedirs(dir, exist_ok=True)

    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.png')]

    for i, img_file in enumerate(image_files):
        # Decide if this image goes to train or val set
        subset = "val" if i % 5 == 0 else "train"

        # Copy image
        shutil.copy(os.path.join(image_dir, img_file), os.path.join(images_output_dir, subset, img_file))

        # Create label file (assuming all images are of class 'Petr' with ID 0)
        label_file = os.path.splitext(img_file)[0] + '.txt'
        with open(os.path.join(labels_output_dir, subset, label_file), 'w') as f:
            # Format: <class> <x_center> <y_center> <width> <height>
            # This is a placeholder. You should replace these values with actual bounding box coordinates
            f.write('0 0.5 0.5 0.5 0.5\n')

    # Create the data.yaml file
    data_yaml = {
        "path": os.path.abspath(output_dir),
        "train": "images/train",
        "val": "images/val",
        "nc": 1,
        "names": ['petr']
    }

    with open(os.path.join(output_dir, "data.yaml"), "w") as f:
        yaml.dump(data_yaml, f, default_flow_style=False)


if __name__ == "__main__":
    image_dir = "captured_images"
    output_dir = "yolo_dataset"
    prepare_yolo_dataset(image_dir, output_dir)