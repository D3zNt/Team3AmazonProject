"""
Quick YOLOv8 Test - One-liner for immediate testing
"""

from ultralytics import YOLO

# Load pre-trained model and test with sample image
model = YOLO('yolov8n.pt')
results = model('https://ultralytics.com/images/bus.jpg')  # Download and test with sample image
results[0].show()  # Display the result 