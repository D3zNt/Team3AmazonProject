"""
YOLOv8 Pre-trained Model Testing Script

This script demonstrates how to use YOLOv8 for object detection using the pre-trained model.
No custom training required - works out of the box!

Make sure to install the required dependencies first:
    pip install ultralytics

The pre-trained model can detect 80 different classes including:
person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, etc.
"""

from ultralytics import YOLO
import cv2
import os
from pathlib import Path

def test_with_sample_image():
    """Test YOLOv8 with a sample image from the internet"""
    
    print("Loading pre-trained YOLOv8 model...")
    # Load pre-trained YOLOv8 model (will download automatically if not present)
    model = YOLO('yolov8n.pt')
    
    print("Testing with sample image from Ultralytics...")
    # Use Ultralytics' sample image (will download automatically)
    results = model('https://ultralytics.com/images/bus.jpg')
    
    # Display results
    for r in results:
        # Plot results image
        im_array = r.plot()  # plot a BGR numpy array of predictions
        
        # Save the result
        cv2.imwrite('detection_result.jpg', im_array)
        print("Detection result saved as 'detection_result.jpg'")
        
        # Print detected objects
        print("\nDetected objects:")
        for box in r.boxes:
            # Get class name
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])
            
            print(f"- {class_name}: {confidence:.2f} confidence")
    
    return results

def test_with_webcam():
    """Test YOLOv8 with webcam (real-time detection)"""
    
    print("Loading pre-trained YOLOv8 model...")
    model = YOLO('yolov8n.pt')
    
    print("Starting webcam detection...")
    print("Press 'q' to quit")
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            break
        
        # Run YOLOv8 inference on the frame
        results = model(frame)
        
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        
        # Display the annotated frame
        cv2.imshow("YOLOv8 Detection", annotated_frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

def test_with_local_image(image_path):
    """Test YOLOv8 with a local image file"""
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found")
        return
    
    print(f"Loading pre-trained YOLOv8 model...")
    model = YOLO('yolov8n.pt')
    
    print(f"Testing with local image: {image_path}")
    results = model(image_path)
    
    # Display results
    for r in results:
        # Plot results image
        im_array = r.plot()
        
        # Create output filename
        output_path = f"detection_{Path(image_path).stem}.jpg"
        cv2.imwrite(output_path, im_array)
        print(f"Detection result saved as '{output_path}'")
        
        # Print detected objects
        print("\nDetected objects:")
        for box in r.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])
            
            print(f"- {class_name}: {confidence:.2f} confidence")

def list_all_classes():
    """Display all classes that the pre-trained model can detect"""
    
    model = YOLO('yolov8n.pt')
    
    print("Pre-trained YOLOv8 can detect the following 80 classes:")
    print("=" * 60)
    
    for i, class_name in model.names.items():
        print(f"{i:2d}: {class_name}")

def main():
    """Main function with menu options"""
    
    print("YOLOv8 Pre-trained Model Test")
    print("=" * 40)
    print("Choose an option:")
    print("1. Test with sample image from internet")
    print("2. Test with webcam (real-time)")
    print("3. Test with local image file")
    print("4. List all detectable classes")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            test_with_sample_image()
            break
        elif choice == '2':
            test_with_webcam()
            break
        elif choice == '3':
            image_path = input("Enter path to your image file: ").strip()
            test_with_local_image(image_path)
            break
        elif choice == '4':
            list_all_classes()
            break
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main() 