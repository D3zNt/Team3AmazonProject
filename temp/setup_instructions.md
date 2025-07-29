# YOLOv8 Object Detection Training Setup

This project provides a complete setup for training YOLOv8 object detection models on custom datasets.

## Environment Setup

### 1. Install Required Dependencies

```bash
pip install ultralytics
```

Or install from the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 2. Dataset Structure

The dataset is organized in the following structure:

```
dataset/
├── train/
│   ├── images/     # Training images (.jpg, .png, etc.)
│   └── labels/     # Training labels (.txt files in YOLO format)
└── val/
    ├── images/     # Validation images
    └── labels/     # Validation labels
```

### 3. Label Format

Labels should be in YOLO format (.txt files) with one line per object:
```
class_id center_x center_y width height
```

Where coordinates are normalized (0-1) relative to image dimensions.

Example label file content:
```
0 0.5 0.5 0.3 0.4  # person at center
1 0.2 0.3 0.1 0.2  # car in upper left
```

## Configuration

### data.yaml
The `data.yaml` file defines the dataset configuration:
- **path**: Root directory of the dataset
- **train**: Path to training images (relative to path)
- **val**: Path to validation images (relative to path)
- **nc**: Number of classes (2 in this example)
- **names**: List of class names

## Training

### Run Training Script

Execute the training script:

```bash
python train_yolov8.py
```

### Training Parameters

The script uses the following default parameters:
- **Model**: yolov8n.pt (nano version for faster training)
- **Epochs**: 100
- **Image Size**: 640x640
- **Batch Size**: 16 (adjust based on GPU memory)
- **Device**: Auto-detect (GPU if available, else CPU)

### Model Variants

You can modify the script to use different YOLOv8 model sizes:
- `yolov8n.pt` - Nano (fastest, smallest)
- `yolov8s.pt` - Small
- `yolov8m.pt` - Medium
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra Large (most accurate, slowest)

## Output

Training results will be saved in:
```
runs/detect/yolov8_custom/
├── weights/
│   ├── best.pt      # Best model weights
│   └── last.pt      # Last epoch weights
├── plots/           # Training plots and metrics
└── results.csv      # Training metrics
```

## Usage After Training

```python
from ultralytics import YOLO

# Load your trained model
model = YOLO('runs/detect/yolov8_custom/weights/best.pt')

# Make predictions
results = model('path/to/image.jpg')
results.show()  # Display results
```

## Notes

- Ensure you have sufficient training data (recommended: 100+ images per class)
- For GPU training, ensure CUDA is properly installed
- Adjust batch size based on your available GPU memory
- The training script includes validation after training completes 