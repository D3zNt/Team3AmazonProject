import React, { useEffect, useRef, forwardRef, useImperativeHandle } from 'react';
import { DetectionResult } from '../types/detection';

interface VideoPlayerProps {
  videoFile: File;
  detectionResults: DetectionResult[];
  currentFrame: number;
  onFrameChange: (frame: number) => void;
}

const VideoPlayer = forwardRef<HTMLVideoElement, VideoPlayerProps>(
  ({ videoFile, detectionResults, currentFrame, onFrameChange }, ref) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useImperativeHandle(ref, () => videoRef.current!, []);

    useEffect(() => {
      if (videoRef.current) {
        const videoUrl = URL.createObjectURL(videoFile);
        videoRef.current.src = videoUrl;

        return () => {
          URL.revokeObjectURL(videoUrl);
        };
      }
    }, [videoFile]);

    useEffect(() => {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      
      if (!video || !canvas) return;

      const ctx = canvas.getContext('2d');
      if (!ctx) return;

      const drawDetections = () => {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Get detection results for current frame
        const currentDetection = detectionResults.find(
          result => Math.abs(result.frameNumber - currentFrame) < 15
        );

        if (currentDetection && currentDetection.detections.length > 0) {
          currentDetection.detections.forEach((detection, index) => {
            const { bbox, confidence, className } = detection;
            
            // Set bounding box colors
            const colors = ['#ef4444', '#10b981', '#3b82f6', '#f59e0b', '#8b5cf6'];
            const color = colors[index % colors.length];
            
            // Draw bounding box
            ctx.strokeStyle = color;
            ctx.lineWidth = 3;
            ctx.strokeRect(bbox.x, bbox.y, bbox.width, bbox.height);
            
            // Draw label background
            const label = `${className} ${(confidence * 100).toFixed(1)}%`;
            ctx.fillStyle = color;
            ctx.font = '14px Arial';
            const textMetrics = ctx.measureText(label);
            ctx.fillRect(
              bbox.x,
              bbox.y - 25,
              textMetrics.width + 10,
              20
            );
            
            // Draw label text
            ctx.fillStyle = 'white';
            ctx.fillText(label, bbox.x + 5, bbox.y - 10);
          });
        }
      };

      const handleTimeUpdate = () => {
        const frame = Math.floor(video.currentTime * 30); // Assuming 30fps
        onFrameChange(frame);
        drawDetections();
      };

      const handleLoadedMetadata = () => {
        // Adjust canvas size to video size
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
      };

      video.addEventListener('timeupdate', handleTimeUpdate);
      video.addEventListener('loadedmetadata', handleLoadedMetadata);

      // detectionResultsが増えたら再描画
      drawDetections();

      return () => {
        video.removeEventListener('timeupdate', handleTimeUpdate);
        video.removeEventListener('loadedmetadata', handleLoadedMetadata);
      };
    }, [detectionResults.length, currentFrame, onFrameChange]);

    return (
      <div className="relative bg-black rounded-lg overflow-hidden">
        <video
          ref={videoRef}
          className="w-full h-auto"
          controls
          preload="metadata"
        />
        <canvas
          ref={canvasRef}
          className="absolute top-0 left-0 w-full h-full pointer-events-none"
          style={{ mixBlendMode: 'normal' }}
        />
      </div>
    );
  }
);

VideoPlayer.displayName = 'VideoPlayer';

export default VideoPlayer;