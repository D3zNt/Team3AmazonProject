"""
Custom Indoor/Night Object Detection Training Script

This script trains YOLOv8 on your custom dataset for indoor/night object detection.
Make sure to:
1. Place your training images in datasets/custom/images/train/
2. Place your training labels in datasets/custom/labels/train/
3. Place your validation images in datasets/custom/images/val/
4. Place your validation labels in datasets/custom/labels/val/
5. Update data.yaml with your specific class names
"""

from ultralytics import YOLO
import os

def check_dataset_structure():
    """Check if the dataset structure is correct"""
    
    required_dirs = [
        'datasets/custom/images/train',
        'datasets/custom/images/val',
        'datasets/custom/labels/train',
        'datasets/custom/labels/val'
    ]
    
    print("🔍 Checking dataset structure...")
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            file_count = len([f for f in os.listdir(dir_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.txt'))])
            print(f"✅ {dir_path} - {file_count} files")
        else:
            print(f"❌ {dir_path} - NOT FOUND")
    
    # Check data.yaml
    if os.path.exists('data.yaml'):
        print("✅ data.yaml found")
    else:
        print("❌ data.yaml NOT FOUND")

def train_custom_model():
    """Train YOLOv8 on custom indoor/night dataset"""
    
    print("🌙 Starting Custom Indoor/Night Object Detection Training...")
    print("=" * 60)
    
    # Load pre-trained YOLOv8 model for transfer learning
    model = YOLO('yolov8n.pt')  # Start with nano model for faster training
    
    # Train the model
    results = model.train(
        data='data.yaml',           # Custom dataset configuration
        epochs=20,                  # Adjust based on your dataset size
        imgsz=640,                  # Input image size
        batch=8,                    # Smaller batch for custom training
        device='cpu',                 # Use GPU 0 (your RTX 3080)
        project='runs/custom',      # Custom project directory
        name='indoor_night',        # Experiment name
        save=True,                  # Save model checkpoints
        plots=True,                 # Generate training plots
        verbose=True,               # Verbose output
        patience=10,                # Early stopping patience
        save_period=10,             # Save checkpoint every 10 epochs
    )
    
    print("🎯 Custom training completed!")
    print(f"📁 Best model saved at: {results.save_dir}")
    print(f"📊 Results saved in: runs/custom/indoor_night/")
    
    return results

def validate_custom_model():
    """Validate the trained custom model"""
    
    model_path = 'runs/custom/indoor_night/weights/best.pt'
    
    if not os.path.exists(model_path):
        print("❌ Trained model not found. Train the model first!")
        return
    
    print("🔍 Validating custom model...")
    model = YOLO(model_path)
    
    # Run validation
    metrics = model.val()
    print(f"📊 Validation results: {metrics}")

def main():
    """Main training function"""
    
    print("🌙 Custom Indoor/Night Object Detection Training")
    print("=" * 60)
    print("1. Check dataset structure")
    print("2. Train custom model")
    print("3. Validate trained model")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            check_dataset_structure()
            break
        elif choice == '2':
            check_dataset_structure()
            print("\n" + "="*60)
            train_custom_model()
            break
        elif choice == '3':
            validate_custom_model()
            break
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main() 