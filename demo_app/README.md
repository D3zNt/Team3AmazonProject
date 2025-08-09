# How to run the backend
```shell
uv run uvicorn backend.yolov8_infer_api:app --reload
```

To check
```shell
curl -X POST "http://127.0.0.1:8000/api/yolov8/infer" \
  -F "video=@/Users/Kota/Downloads/sample_mov.mov" \
  -F "model=@/Users/Kota/blended/Team3AmazonProject/notebooks/furniture_project_3/furniture_yolov8n_20250805_223347/weights/best.pt"
```

# How to run demp app
First, set up environment. This is only first time.
```shell
npm install
```

Then, run the app.
```shell
npm run dev
```
