"""
YOLOv8 Object Detection Training Script

This script trains a YOLOv8 model on a custom dataset.
Make sure to install the required dependencies first:
    pip install ultralytics

Dataset structure should be:
/dataset
    /train
        /images
        /labels
    /val
        /images
        /labels
"""

from ultralytics import YOLO

def main():
    """Main training function"""
    
    print("Starting YOLOv8 training...")
    
    # Load a pre-trained YOLOv8 model
    # yolov8n.pt is the nano version (smallest and fastest)
    # Other options: yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
    model = YOLO('yolov8n.pt')
    
    # Train the model
    results = model.train(
        data='data.yaml',           # path to dataset YAML
        epochs=100,                 # number of training epochs
        imgsz=640,                  # input image size
        batch=16,                   # batch size (adjust based on your GPU memory)
        device='auto',              # automatically select device (GPU if available, else CPU)
        project='runs/detect',      # project directory
        name='yolov8_custom',       # experiment name
        save=True,                  # save model checkpoints
        verbose=True,               # verbose output
        plots=True,                 # generate training plots
    )
    
    print("Training completed!")
    print(f"Best model saved at: {results.save_dir}")
    
    # Optional: Validate the trained model
    print("\nValidating the trained model...")
    metrics = model.val()
    print(f"Validation results: {metrics}")

if __name__ == "__main__":
    main() 