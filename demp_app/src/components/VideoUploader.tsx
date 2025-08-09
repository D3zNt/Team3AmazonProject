import React, { useCallback } from 'react';
import { Upload, Video, X } from 'lucide-react';

interface VideoUploaderProps {
  onVideoUpload: (file: File) => void;
  videoFile: File | null;
}

const VideoUploader: React.FC<VideoUploaderProps> = ({ onVideoUpload, videoFile }) => {
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('video/')) {
        onVideoUpload(file);
      }
    }
  }, [onVideoUpload]);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onVideoUpload(file);
    }
  }, [onVideoUpload]);

  const removeFile = () => {
    onVideoUpload(null as any);
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h3 className="text-white font-semibold mb-4 flex items-center">
        <Video className="h-5 w-5 mr-2" />
        Video Upload
      </h3>
      
      {videoFile ? (
        <div className="bg-gray-700 rounded-lg p-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Video className="h-6 w-6 text-blue-400" />
            <div>
              <p className="text-white font-medium">{videoFile.name}</p>
              <p className="text-gray-400 text-sm">
                {(videoFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>
          <button
            onClick={removeFile}
            className="text-red-400 hover:text-red-300 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
      ) : (
        <div
          className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center hover:border-blue-500 transition-colors duration-200 cursor-pointer"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => document.getElementById('video-upload')?.click()}
        >
          <Upload className="h-12 w-12 text-gray-500 mx-auto mb-4" />
          <p className="text-gray-400 mb-2">
            Drag & drop video file or click to upload
          </p>
          <p className="text-gray-500 text-sm">
            Supported formats: MP4, AVI, MOV, WebM
          </p>
          <input
            id="video-upload"
            type="file"
            accept="video/*"
            onChange={handleFileChange}
            className="hidden"
          />
        </div>
      )}
    </div>
  );
};

export default VideoUploader;