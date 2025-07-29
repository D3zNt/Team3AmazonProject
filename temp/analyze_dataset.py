"""
Dataset Analysis Script
This script analyzes your label files to discover what classes are actually present.
"""

import os
import glob
from collections import Counter

def analyze_labels():
    """Analyze all label files to find unique classes and their frequencies"""
    
    # Find all label files in the dataset
    label_patterns = [
        'datasets/custom/labels/train/*.txt',
        'datasets/custom/labels/val/*.txt',
    ]
    
    all_classes = []
    file_count = 0
    
    print("🔍 Scanning for label files...")
    
    for pattern in label_patterns:
        label_files = glob.glob(pattern, recursive=True)
        if label_files:
            print(f"Found {len(label_files)} label files in pattern: {pattern}")
            
            for label_file in label_files:
                try:
                    with open(label_file, 'r') as f:
                        lines = f.readlines()
                        
                    for line in lines:
                        line = line.strip()
                        if line:  # Skip empty lines
                            parts = line.split()
                            if len(parts) >= 5:  # Valid YOLO format: class x y w h
                                try:
                                    class_id = int(parts[0])
                                    all_classes.append(class_id)
                                except ValueError:
                                    print(f"⚠️  Invalid class ID in {label_file}: {parts[0]}")
                    
                    file_count += 1
                        
                except Exception as e:
                    print(f"❌ Error reading {label_file}: {e}")
    
    if not all_classes:
        print("❌ No valid label files found!")
        print("\n🔍 Let me search for any .txt files in your project:")
        all_txt_files = glob.glob('**/*.txt', recursive=True)
        for txt_file in all_txt_files[:10]:  # Show first 10
            print(f"  📄 {txt_file}")
        if len(all_txt_files) > 10:
            print(f"  ... and {len(all_txt_files) - 10} more files")
        return
    
    # Analyze the classes
    class_counts = Counter(all_classes)
    unique_classes = sorted(class_counts.keys())
    
    print(f"\n📊 Dataset Analysis Results:")
    print(f"=" * 50)
    print(f"📁 Total label files processed: {file_count}")
    print(f"🏷️  Total annotations: {len(all_classes)}")
    print(f"🎯 Unique classes found: {len(unique_classes)}")
    print(f"📈 Class range: {min(unique_classes)} to {max(unique_classes)}")
    
    print(f"\n📋 Class Distribution:")
    print(f"Class ID | Count | Percentage")
    print(f"-" * 30)
    
    for class_id in unique_classes:
        count = class_counts[class_id]
        percentage = (count / len(all_classes)) * 100
        print(f"{class_id:8d} | {count:5d} | {percentage:7.1f}%")
    
    # Generate updated data.yaml content
    print(f"\n✅ Suggested data.yaml update:")
    print(f"=" * 50)
    print(f"nc: {len(unique_classes)}")
    print(f"names:")
    
    # Generic class names based on indices
    for i, class_id in enumerate(unique_classes):
        print(f"  {class_id}: class_{class_id}")
    
    print(f"\n💡 Next steps:")
    print(f"1. Update your data.yaml with nc: {len(unique_classes)}")
    print(f"2. Replace the generic 'class_X' names with meaningful names")
    print(f"3. Make sure all class IDs are consecutive (0, 1, 2, 3...)")
    
    # Check for non-consecutive class IDs
    expected_classes = list(range(len(unique_classes)))
    if unique_classes != expected_classes:
        print(f"\n⚠️  WARNING: Your class IDs are not consecutive!")
        print(f"   Found: {unique_classes}")
        print(f"   Expected: {expected_classes}")
        print(f"   You may need to remap your class IDs.")

if __name__ == "__main__":
    analyze_labels() 