from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from fastapi.responses import StreamingResponse
import tempfile
import shutil
import cv2
import json
import asyncio

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/yolov8/infer")
async def infer(
    video: UploadFile = File(...),
    model: UploadFile = File(...),
):
    with (
        tempfile.NamedTemporaryFile(delete=False, suffix=".pt") as model_tmp,
        tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as video_tmp,
    ):
        shutil.copyfileobj(model.file, model_tmp)
        shutil.copyfileobj(video.file, video_tmp)
        model_path = model_tmp.name
        video_path = video_tmp.name

    yolo = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)

    frame_num = 0
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    frame_stride = 2
    conf_th = 0.5
    iou_th = 0.6
    max_area_ratio = 0.6

    async def result_generator():
        nonlocal frame_num
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_num % frame_stride != 0:
                frame_num += 1
                continue

            preds = yolo(frame, conf=conf_th, iou=iou_th, imgsz=640)
            h, w = frame.shape[:2]
            dets = []

            for box in preds[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                bw, bh = float(x2 - x1), float(y2 - y1)
                if (bw * bh) / (w * h) > max_area_ratio:
                    continue

                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                dets.append(
                    {
                        "bbox": {
                            "x": int(x1),
                            "y": int(y1),
                            "width": int(bw),
                            "height": int(bh),
                        },
                        "confidence": conf,
                        "className": yolo.names[cls_id],
                        "classId": cls_id,
                    }
                )

            result = {
                "frameNumber": frame_num,
                "timestamp": frame_num / fps,
                "detections": dets,
            }
            yield (json.dumps(result) + "\n")
            frame_num += 1
            await asyncio.sleep(0)  # イベントループを譲る

        cap.release()
        try:
            import os

            os.remove(model_path)
            os.remove(video_path)
        except Exception:
            pass

    return StreamingResponse(result_generator(), media_type="application/x-ndjson")


@app.post("/api/yolov8/infer_image")
async def infer_image(
    image: UploadFile = File(...),
    model: UploadFile = File(...),
):
    import numpy as np
    import os

    with (
        tempfile.NamedTemporaryFile(delete=False, suffix=".pt") as model_tmp,
        tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as image_tmp,
    ):
        shutil.copyfileobj(model.file, model_tmp)
        shutil.copyfileobj(image.file, image_tmp)
        model_path = model_tmp.name
        image_path = image_tmp.name

    yolo = YOLO(model_path)
    img = cv2.imread(image_path)
    conf_th = 0.5
    iou_th = 0.6
    max_area_ratio = 0.6

    preds = yolo(img, conf=conf_th, iou=iou_th, imgsz=640)
    h, w = img.shape[:2]
    dets = []

    for box in preds[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        bw, bh = float(x2 - x1), float(y2 - y1)
        if (bw * bh) / (w * h) > max_area_ratio:
            continue

        conf = float(box.conf[0])
        cls_id = int(box.cls[0])
        dets.append(
            {
                "bbox": {
                    "x": int(x1),
                    "y": int(y1),
                    "width": int(bw),
                    "height": int(bh),
                },
                "confidence": conf,
                "className": yolo.names[cls_id],
                "classId": cls_id,
            }
        )

    try:
        os.remove(model_path)
        os.remove(image_path)
    except Exception:
        pass

    return {"detections": dets}
