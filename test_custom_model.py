"""
Custom Model Testing Script

Test your trained indoor/night object detection model on new images.
"""

from ultralytics import YOLO
import cv2
import os

def test_custom_model_single(image_path):
    """Test custom model on a single image"""
    
    model_path = 'runs/custom/indoor_night2/weights/best.pt'
    
    if not os.path.exists(model_path):
        print("❌ Custom model not found!")
        print("   Train your model first using: python train_custom.py")
        return
    
    if not os.path.exists(image_path):
        print(f"❌ Image {image_path} not found!")
        return
    
    print(f"🌙 Testing custom model on: {image_path}")
    print("=" * 50)
    
    # Load your custom trained model
    model = YOLO(model_path)
    
    # Run detection
    results = model(image_path)
    
    # Save result image
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_path = f'{base_name}_custom_detection.jpg'
    
    for r in results:
        im_array = r.plot()
        cv2.imwrite(output_path, im_array)
    
    print(f"✅ Result saved as: {output_path}")
    
    # Print detected objects
    print("\n📋 Custom model detected:")
    total_detections = 0
    for r in results:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])
                print(f"   - {class_name}: {confidence:.3f} confidence")
                total_detections += 1
    
    if total_detections == 0:
        print("   - No objects detected")
    
    return results

def test_custom_model_folder(folder_path):
    """Test custom model on all images in a folder"""
    
    if not os.path.exists(folder_path):
        print(f"❌ Folder {folder_path} not found!")
        return
    
    # Find all image files
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    image_files = [f for f in os.listdir(folder_path) 
                   if f.lower().endswith(image_extensions)]
    
    if not image_files:
        print(f"❌ No image files found in {folder_path}")
        return
    
    print(f"🌙 Testing custom model on {len(image_files)} images in: {folder_path}")
    print("=" * 60)
    
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f"\n🖼️  Processing: {image_file}")
        test_custom_model_single(image_path)

def compare_models(image_path):
    """Compare custom model vs pre-trained model"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image {image_path} not found!")
        return
    
    print(f"🔍 Comparing models on: {image_path}")
    print("=" * 50)
    
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    
    # Test pre-trained model
    print("🔄 Testing PRE-TRAINED model...")
    pretrained_model = YOLO('yolov8n.pt')
    results_pretrained = pretrained_model(image_path)
    
    for r in results_pretrained:
        im_array = r.plot()
        cv2.imwrite(f'{base_name}_pretrained.jpg', im_array)
    
    print("📋 Pre-trained model detected:")
    for r in results_pretrained:
        boxes = r.boxes
        if boxes is not None:
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = pretrained_model.names[class_id]
                confidence = float(box.conf[0])
                print(f"   - {class_name}: {confidence:.3f}")
    
    # Test custom model
    print("\n🌙 Testing CUSTOM model...")
    test_custom_model_single(image_path)
    
    print(f"\n🎯 Comparison complete!")
    print(f"   📸 {base_name}_pretrained.jpg - Pre-trained results")
    print(f"   📸 {base_name}_custom_detection.jpg - Custom results")

def main():
    """Main testing function"""
    
    print("🌙 Custom Indoor/Night Object Detection Testing")
    print("=" * 60)
    print("1. Test on single image")
    print("2. Test on folder of images")
    print("3. Compare custom vs pre-trained model")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            image_path = input("Enter path to image: ").strip()
            test_custom_model_single(image_path)
            break
        elif choice == '2':
            folder_path = input("Enter path to folder: ").strip()
            test_custom_model_folder(folder_path)
            break
        elif choice == '3':
            image_path = input("Enter path to image: ").strip()
            compare_models(image_path)
            break
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main() 