# capture_images.py
import cv2
import os
import json
import time
import numpy as np


def draw_circle_guide(frame, center, radius, color=(0, 255, 0), thickness=2):
    cv2.circle(frame, center, radius, color, thickness)


def apply_circular_focus(frame, center, radius, alpha=0.5):
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)

    # Create a dimmed version of the frame
    dimmed = frame.copy()
    dimmed = cv2.addWeighted(dimmed, alpha, np.zeros_like(dimmed), 1 - alpha, 0)

    # Combine the original frame (inside the circle) with the dimmed frame (outside the circle)
    result = np.where(mask[:, :, None] == 255, frame, dimmed)

    return result


def capture_images(output_dir, num_images=600, interval=0.05):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    object_name = input("Enter object name (e.g., Petr): ")
    metadata = {}

    # Setup circle guide
    frame_center = (320, 240)  # Center of 640x480 frame
    circle_radius = 150  # Adjust this value to change the size of the circular guide

    print("Position your face within the circle and press 'c' to start capturing. Press 'q' to quit.")

    capturing = False
    count = 0
    last_capture_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Apply circular focus effect
        frame_with_focus = apply_circular_focus(frame, frame_center, circle_radius)

        # Draw circle guide
        draw_circle_guide(frame_with_focus, frame_center, circle_radius)

        if capturing:
            cv2.putText(frame_with_focus, f"Capturing: {count}/{num_images}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
        else:
            cv2.putText(frame_with_focus, "Press 'c' to start capturing", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)

        cv2.imshow('frame', frame_with_focus)
        key = cv2.waitKey(1)

        if key & 0xFF == ord('c') and not capturing:
            capturing = True
            print(f"Capturing {num_images} images. Press 'q' to quit early.")

        if capturing:
            current_time = time.time()
            if current_time - last_capture_time >= interval:
                # Create a circular mask
                mask = np.zeros(frame.shape[:2], dtype=np.uint8)
                cv2.circle(mask, frame_center, circle_radius, (255, 255, 255), -1)

                # Apply the mask to the frame
                masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

                image_name = f"{object_name}_{count:03d}"
                image_path = os.path.join(output_dir, f"{image_name}.jpg")
                cv2.imwrite(image_path, masked_frame)
                print(f"Image saved as {image_path}")
                metadata[image_name] = object_name
                count += 1
                last_capture_time = current_time

                # Visual feedback for capture
                cv2.circle(frame_with_focus, frame_center, circle_radius, (0, 255, 0), 10)
                cv2.imshow('frame', frame_with_focus)
                cv2.waitKey(1)

                if count >= num_images:
                    break

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