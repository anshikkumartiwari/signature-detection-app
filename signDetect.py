import cv2
from ultralytics import YOLO
import time

def detectandMark(input_path, output_path, model_path=r"best.pt", conf_threshold=0.75):
    """
    Detect and mark all signatures in the image.
    """
    
    model = YOLO(model_path)
    
    image = cv2.imread(input_path)
    
    results = model.predict(source=input_path, conf=conf_threshold)
    
    print(f"Number of detections: {len(results)}")
    
    start_time = time.time()

    for result in results:
        if result.boxes is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            for box in boxes:
                x1, y1, x2, y2 = map(int, box)
                # Draw a red box around the detected signature
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red color in BGR, thickness 2

    # Save the processed image
    cv2.imwrite(output_path, image)

    # End timing
    end_time = time.time()
    processing_time = end_time - start_time

    # Generate processing information
    processing_info = (
        f"{len(boxes)} signatures, {processing_time * 1000:.1f}ms\n"
        #f"Speed: {processing_time * 1000:.1f}ms total\n"
        #f"Number of detections: {len(results)}\n"
        #f"Number of boxes detected: {len(boxes)}"
    )

    return processing_info
