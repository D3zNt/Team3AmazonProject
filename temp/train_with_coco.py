"""
YOLOv8 Training with COCO Dataset Options

This script shows different ways to train YOLOv8 using COCO dataset configurations.
"""

from ultralytics import YOLO

def train_full_coco():
    """Train on full COCO dataset (80 classes, ~20GB download)"""
    
    print("Training with full COCO dataset...")
    model = YOLO('yolov8n.pt')
    
    # This will automatically download COCO dataset if not present
    results = model.train(
        data='coco.yaml',           # Use built-in COCO configuration
        epochs=100,
        imgsz=640,
        batch=16,
        device='cpu',
        project='runs/detect',
        name='yolov8_full_coco',
    )
    
    print("Full COCO training completed!")
    return results

def train_coco_subset():
    """Train on COCO8 (small subset for testing, 8 images)"""
    
    print("Training with COCO8 subset...")
    model = YOLO('yolov8n.pt')
    
    # Small subset for quick testing
    results = model.train(
        data='coco8.yaml',          # Use COCO8 subset
        epochs=10,                  # Fewer epochs for testing
        imgsz=640,
        batch=16,
        device='cpu',
        project='runs/detect',
        name='yolov8_coco8',
    )
    
    print("COCO8 training completed!")
    return results

def train_coco128():
    """Train on COCO128 (medium subset for testing, 128 images)"""
    
    print("Training with COCO128 subset...")
    model = YOLO('yolov8n.pt')
    
    # Medium subset for testing
    results = model.train(
        data='coco128.yaml',        # Use COCO128 subset
        epochs=50,
        imgsz=640,
        batch=16,
        device='cpu',
        project='runs/detect',
        name='yolov8_coco128',
    )
    
    print("COCO128 training completed!")
    return results

def show_coco_classes():
    """Display all 80 COCO classes"""
    
    model = YOLO('yolov8n.pt')
    
    print("COCO Dataset Classes (80 total):")
    print("=" * 50)
    
    # COCO class names (same as pre-trained model)
    for i, class_name in model.names.items():
        print(f"{i:2d}: {class_name}")

def main():
    """Main function with options"""
    
    print("YOLOv8 COCO Dataset Training Options")
    print("=" * 50)
    print("1. Train on full COCO dataset (80 classes, ~20GB)")
    print("2. Train on COCO8 subset (8 images, quick test)")
    print("3. Train on COCO128 subset (128 images, medium test)")
    print("4. Show all COCO classes")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            train_full_coco()
            break
        elif choice == '2':
            train_coco_subset()
            break
        elif choice == '3':
            train_coco128()
            break
        elif choice == '4':
            show_coco_classes()
            break
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main() 