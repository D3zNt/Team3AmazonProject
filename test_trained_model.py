"""
Test Your Trained YOLOv8 Model

This script demonstrates how to use your trained model and compare it with the pre-trained model.
"""

from ultralytics import YOLO
import cv2

def test_pretrained_model():
    """Test the original pre-trained model"""
    
    print("🔄 Testing PRE-TRAINED model...")
    print("=" * 50)
    
    # Load pre-trained model
    model = YOLO('yolov8n.pt')
    
    # Test on bus.jpg
    results = model('bus.jpg')
    
    # Save result image
    for r in results:
        im_array = r.plot()
        cv2.imwrite('bus_pretrained_result.jpg', im_array)
    
    print("✅ Pre-trained model results saved as 'bus_pretrained_result.jpg'")
    
    # Print detected objects
    print("\n📋 Pre-trained model detected:")
    for r in results:
        boxes = r.boxes
        for box in boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])
            print(f"   - {class_name}: {confidence:.3f} confidence")
    
    return results

def test_trained_model():
    """Test your newly trained model"""
    
    print("\n🎯 Testing YOUR TRAINED model...")
    print("=" * 50)
    
    # Load YOUR trained model
    model = YOLO('runs/detect/yolov8_coco8/weights/best.pt')
    
    # Test on the same bus.jpg
    results = model('bus.jpg')
    
    # Save result image
    for r in results:
        im_array = r.plot()
        cv2.imwrite('bus_trained_result.jpg', im_array)
    
    print("✅ Trained model results saved as 'bus_trained_result.jpg'")
    
    # Print detected objects
    print("\n📋 Your trained model detected:")
    for r in results:
        boxes = r.boxes
        for box in boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])
            print(f"   - {class_name}: {confidence:.3f} confidence")
    
    return results

def compare_models():
    """Compare pre-trained vs trained model performance"""
    
    print("\n🔍 COMPARISON SUMMARY:")
    print("=" * 50)
    print("Images saved:")
    print("  📸 bus_pretrained_result.jpg  - Pre-trained model result")
    print("  📸 bus_trained_result.jpg     - Your trained model result")
    print("\n💡 Look at both images to see the differences!")
    print("   - Check detection confidence scores")
    print("   - See if more/fewer objects are detected")
    print("   - Notice any differences in bounding box accuracy")

def test_on_different_image(image_path):
    """Test both models on a different image"""
    
    if not os.path.exists(image_path):
        print(f"❌ Image {image_path} not found")
        return
    
    print(f"\n🖼️  Testing both models on: {image_path}")
    print("=" * 50)
    
    # Pre-trained model
    pretrained_model = YOLO('yolov8n.pt')
    results_pretrained = pretrained_model(image_path)
    
    # Your trained model  
    trained_model = YOLO('runs/custom/indoor_night2/weights/best.pt')
    results_trained = trained_model(image_path)
    
    # Save results
    base_name = image_path.replace('.jpg', '').replace('.png', '')
    
    for r in results_pretrained:
        im_array = r.plot()
        cv2.imwrite(f'{base_name}_pretrained.jpg', im_array)
    
    for r in results_trained:
        im_array = r.plot()
        cv2.imwrite(f'{base_name}_trained.jpg', im_array)
    
    print(f"✅ Results saved as:")
    print(f"   📸 {base_name}_pretrained.jpg")
    print(f"   📸 {base_name}_trained.jpg")

def main():
    """Main function with testing options"""
    
    print("🚀 YOLOv8 Trained Model Testing")
    print("=" * 50)
    print("Choose an option:")
    print("1. Test on bus.jpg (compare pre-trained vs trained)")
    print("2. Test trained model only on bus.jpg")
    print("3. Test on a different image file")
    print("4. Show training results and plots")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            test_pretrained_model()
            test_trained_model()
            compare_models()
            break
        elif choice == '2':
            test_trained_model()
            break
        elif choice == '3':
            image_path = input("Enter path to your image: ").strip()
            test_on_different_image(image_path)
            break
        elif choice == '4':
            print("\n📊 Training results are in:")
            print("   📁 runs/detect/yolov8_coco8/")
            print("   📈 results.png - Training curves")
            print("   🎯 confusion_matrix.png - Model accuracy")
            print("   🖼️  val_batch0_pred.jpg - Validation predictions")
            break
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    import os
    main() 