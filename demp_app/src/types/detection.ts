export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface Detection {
  bbox: BoundingBox;
  confidence: number;
  className: string;
  classId: number;
}

export interface DetectionResult {
  frameNumber: number;
  timestamp: number;
  detections: Detection[];
}