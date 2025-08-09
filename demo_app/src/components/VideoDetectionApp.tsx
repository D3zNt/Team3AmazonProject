import React, { useState, useRef, useCallback } from 'react';
import { Upload, Play, Pause, RotateCcw, Download, Settings } from 'lucide-react';
import VideoUploader from './VideoUploader';
import VideoPlayer from './VideoPlayer';
import ModelUploader from './ModelUploader';
import DetectionResults from './DetectionResults';
import { DetectionResult } from '../types/detection';

const FPS = 10;

const VideoDetectionApp: React.FC = () => {
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [modelFile, setModelFile] = useState<File | null>(null);
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [canPlay, setCanPlay] = useState(true);

  const videoRef = useRef<HTMLVideoElement>(null);

  const handleVideoUpload = useCallback((file: File) => {
    setVideoFile(file);
    setResults([]);
    setCurrentFrame(0);
    setCanPlay(true);
  }, []);

  const handleModelUpload = useCallback((file: File) => {
    setModelFile(file);
  }, []);

  // 10fpsごとにフレーム画像を抽出
  const extractFrames = (videoFile: File, fps: number): Promise<{frameId: number, image: Blob}[]> => {
    return new Promise((resolve) => {
      const video = document.createElement('video');
      video.src = URL.createObjectURL(videoFile);
      video.preload = 'auto';
      video.muted = true;
      video.crossOrigin = 'anonymous';

      const frames: {frameId: number, image: Blob}[] = [];
      video.addEventListener('loadedmetadata', async () => {
        const duration = video.duration;
        const totalFrames = Math.floor(duration * fps);
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d')!;
        let frameId = 0;

        const captureFrame = (frame: number) => {
          return new Promise<Blob>((resolveFrame) => {
            video.currentTime = frame / fps;
            video.onseeked = () => {
              ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
              canvas.toBlob((blob) => {
                if (blob) resolveFrame(blob);
              }, 'image/jpeg');
            };
          });
        };

        for (let frame = 0; frame < totalFrames; frame++) {
          // eslint-disable-next-line no-await-in-loop
          const blob = await captureFrame(frame);
          frames.push({ frameId: frame, image: blob });
        }
        resolve(frames);
      });
    });
  };

  // 1フレーム画像ごとにバックエンドへ推論リクエスト
  const detectFrame = async (image: Blob, modelFile: File, frameId: number) => {
    const formData = new FormData();
    formData.append('image', image, `frame${frameId}.jpg`);
    formData.append('model', modelFile);
    const response = await fetch('http://127.0.0.1:8000/api/yolov8/infer_image', {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error('Detection failed');
    const result = await response.json();
    return { ...result, frameId };
  };

  const processVideo = async () => {
    if (!videoFile || !modelFile) {
      alert('Please upload both video file and model file');
      return;
    }

    setLoading(true);
    setResults([]);
    setCanPlay(false);

    // 10fpsでフレーム抽出
    const frames = await extractFrames(videoFile, FPS);

    const detectionResults: any[] = [];
    for (const { frameId, image } of frames) {
      try {
        // eslint-disable-next-line no-await-in-loop
        const result = await detectFrame(image, modelFile, frameId);
        detectionResults.push(result);
        setResults([...detectionResults]); // 進捗表示
      } catch (e) {
        detectionResults.push({ frameId, detections: [] });
      }
    }

    setResults(detectionResults);
    setLoading(false);
    setCanPlay(true);
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
            disabled={!videoFile || !modelFile || loading}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed hover:from-blue-700 hover:to-purple-700 transition-all duration-200 flex items-center justify-center space-x-2"
          >
            {loading ? (
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
                detectionResults={results}
                currentFrame={currentFrame}
                onFrameChange={setCurrentFrame}
                ref={videoRef}
                disabled={!canPlay}
                fps={FPS}
              />
              
              {/* Controls */}
              <div className="flex justify-center space-x-4">
                <button
                  onClick={togglePlayPause}
                  className="bg-green-600 hover:bg-green-700 text-white p-3 rounded-full transition-colors duration-200"
                  disabled={!canPlay}
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
                  disabled={results.length === 0}
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
      {results.length > 0 && (
        <div className="mt-8">
          <DetectionResults results={results} currentFrame={currentFrame} />
        </div>
      )}
    </div>
  );
};

export default VideoDetectionApp;

// Whammy型宣言
declare global {
  interface Window {
    Whammy: any;
  }
}