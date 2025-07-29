# src/download_coco.py
from ultralytics import YOLO
import yaml
from pathlib import Path

def setup_coco_dataset():
    """Setup COCO dataset for indoor robot detection"""
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    print("Initializing YOLOv8 model...")
    # Initialize YOLOv8 model (pre-trained on COCO)
    model = YOLO('yolov8n.pt')  # nano version, lightweight for testing
    
    print("Creating COCO dataset configuration file...")
    
    # COCO classes relevant for indoor robot scenarios
    indoor_classes = {
        0: 'person',
        39: 'bottle', 
        40: 'wine glass',
        41: 'cup',
        42: 'fork',
        43: 'knife', 
        44: 'spoon',
        45: 'bowl',
        56: 'chair',
        57: 'couch', 
        58: 'potted plant',
        59: 'bed',
        60: 'dining table',
        61: 'toilet',
        62: 'tv',
        63: 'laptop',
        64: 'mouse',
        65: 'remote',
        66: 'keyboard',
        67: 'cell phone',
        68: 'microwave',
        69: 'oven',
        70: 'toaster',
        71: 'sink',
        72: 'refrigerator',
        73: 'book',
        74: 'clock',
        75: 'vase',
        76: 'scissors',
        77: 'teddy bear',
        78: 'hair drier',
        79: 'toothbrush'
    }
    
    # COCO configuration file
    coco_config = {
        'path': str(data_dir / 'coco'),
        'train': 'train2017',
        'val': 'val2017', 
        'test': 'test2017',
        'names': indoor_classes
    }
    
    # Save configuration file
    config_path = data_dir / 'coco_indoor.yaml'
    with open(config_path, 'w') as f:
        yaml.dump(coco_config, f, default_flow_style=False)
    
    print(f"Configuration file saved: {config_path}")
    print(f"Number of indoor-related classes: {len(indoor_classes)}")
    
    # Train YOLOv8 with COCO dataset for automatic download
    print("Starting COCO dataset download...")
    try:
        # Small epoch number for trial (main purpose is data download)
        model.train(data='coco.yaml', epochs=1, imgsz=640, batch=1, verbose=True)
        print("COCO dataset download completed!")
    except Exception as e:
        print(f"Error during download: {e}")
        print("Manual download might be required")
    
    return config_path

if __name__ == "__main__":
    config_path = setup_coco_dataset()
    print(f"\n🎉 Setup completed!")
    print(f"Configuration file: {config_path}")
    print("Next step: Fine-tuning with indoor-specific data")