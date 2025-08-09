import React, { useState, useRef, useCallback } from 'react';
import { Upload, Play, Pause, RotateCcw, Download, Settings } from 'lucide-react';
import VideoUploader from './VideoUploader';
import VideoPlayer from './VideoPlayer';
import ModelUploader from './ModelUploader';
import DetectionResults from './DetectionResults';
import { DetectionResult } from '../types/detection';

const VideoDetectionApp: React.FC = () => {
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [modelFile, setModelFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [detectionResults, setDetectionResults] = useState<DetectionResult[]>([]);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  
  const videoRef = useRef<HTMLVideoElement>(null);

  const handleVideoUpload = useCallback((file: File) => {
    setVideoFile(file);
    setDetectionResults([]);
    setCurrentFrame(0);
  }, []);

  const handleModelUpload = useCallback((file: File) => {
    setModelFile(file);
  }, []);

  const processVideo = async () => {
    if (!videoFile || !modelFile) {
      alert('Please upload both video file and model file');
      return;
    }

    setIsProcessing(true);
    
    // Mock detection results (can be replaced with actual YOLOv8 processing)
    const mockResults: DetectionResult[] = [
      {
        frameNumber: 0,
        timestamp: 0,
        detections: [
          {
            bbox: { x: 100, y: 50, width: 150, height: 200 },
            confidence: 0.85,
            className: 'person',
            classId: 0
          },
          {
            bbox: { x: 300, y: 100, width: 120, height: 80 },
            confidence: 0.92,
            className: 'car',
            classId: 2
          }
        ]
      },
      {
        frameNumber: 30,
        timestamp: 1.0,
        detections: [
          {
            bbox: { x: 110, y: 55, width: 150, height: 200 },
            confidence: 0.87,
            className: 'person',
            classId: 0
          },
          {
            bbox: { x: 320, y: 105, width: 120, height: 80 },
            confidence: 0.89,
            className: 'car',
            classId: 2
          }
        ]
      }
    ];

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setDetectionResults(mockResults);
    setIsProcessing(false);
  };

  const togglePlayPause = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const resetVideo = () => {
    if (videoRef.current) {
      videoRef.current.currentTime = 0;
      setCurrentFrame(0);
      setIsPlaying(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">
          YOLOv8 Video Object Detection
        </h1>
        <p className="text-gray-400">
          Upload videos and run real-time detection with YOLOv8 models
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Upload Section */}
        <div className="lg:col-span-1 space-y-6">
          <VideoUploader onVideoUpload={handleVideoUpload} videoFile={videoFile} />
          <ModelUploader onModelUpload={handleModelUpload} modelFile={modelFile} />
          
          <button
            onClick={processVideo}
            disabled={!videoFile || !modelFile || isProcessing}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:from-blue-700 hover:to-purple-700 transition-all duration-200 flex items-center justify-center space-x-2"
          >
            {isProcessing ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Settings className="h-5 w-5" />
                <span>Start Detection</span>
              </>
            )}
          </button>
        </div>

        {/* Video Player Section */}
        <div className="lg:col-span-2">
          {videoFile ? (
            <div className="space-y-4">
              <VideoPlayer
                videoFile={videoFile}
                detectionResults={detectionResults}
                currentFrame={currentFrame}
                onFrameChange={setCurrentFrame}
                ref={videoRef}
              />
              
              {/* Controls */}
              <div className="flex justify-center space-x-4">
                <button
                  onClick={togglePlayPause}
                  className="bg-green-600 hover:bg-green-700 text-white p-3 rounded-full transition-colors duration-200"
                >
                  {isPlaying ? <Pause className="h-6 w-6" /> : <Play className="h-6 w-6" />}
                </button>
                <button
                  onClick={resetVideo}
                  className="bg-yellow-600 hover:bg-yellow-700 text-white p-3 rounded-full transition-colors duration-200"
                >
                  <RotateCcw className="h-6 w-6" />
                </button>
                <button
                  className="bg-purple-600 hover:bg-purple-700 text-white p-3 rounded-full transition-colors duration-200"
                  disabled={detectionResults.length === 0}
                >
                  <Download className="h-6 w-6" />
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-gray-800 rounded-lg p-12 text-center">
              <Upload className="h-16 w-16 text-gray-500 mx-auto mb-4" />
              <p className="text-gray-400 text-lg">
                Upload a video to start detection
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Detection Results */}
      {detectionResults.length > 0 && (
        <div className="mt-8">
          <DetectionResults results={detectionResults} currentFrame={currentFrame} />
        </div>
      )}
    </div>
  );
};

export default VideoDetectionApp;