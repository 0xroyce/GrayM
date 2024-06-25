# capture_images.py
import cv2
import os
import json
import time


def capture_images(output_dir, num_images=300, interval=0.2):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    object_name = input("Enter object name (e.g., Petr): ")
    metadata = {}

    print(f"Capturing {num_images} images. Press 'q' to quit early.")

    count = 0
    last_capture_time = time.time()

    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)

        current_time = time.time()
        if current_time - last_capture_time >= interval:
            image_name = f"{object_name}_{count:03d}"
            image_path = os.path.join(output_dir, f"{image_name}.jpg")
            cv2.imwrite(image_path, frame)
            print(f"Image saved as {image_path}")
            metadata[image_name] = object_name
            count += 1
            last_capture_time = current_time

            # Draw a rectangle to indicate capture
            cv2.rectangle(frame, (0, 0), (640, 480), (0, 255, 0), 10)
            cv2.imshow('frame', frame)
            cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Save metadata
    with open(os.path.join(output_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f)

    print(f"Captured {count} images.")


if __name__ == "__main__":
    output_dir = "captured_images"
    capture_images(output_dir)
