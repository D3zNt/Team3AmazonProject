import React, { useCallback } from 'react';
import { Upload, Brain, X } from 'lucide-react';

interface ModelUploaderProps {
  onModelUpload: (file: File) => void;
  modelFile: File | null;
}

const ModelUploader: React.FC<ModelUploaderProps> = ({ onModelUpload, modelFile }) => {
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.name.endsWith('.pt') || file.name.endsWith('.onnx') || file.name.endsWith('.engine')) {
        onModelUpload(file);
      }
    }
  }, [onModelUpload]);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onModelUpload(file);
    }
  }, [onModelUpload]);

  const removeFile = () => {
    onModelUpload(null as any);
  };

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h3 className="text-white font-semibold mb-4 flex items-center">
        <Brain className="h-5 w-5 mr-2" />
        YOLOv8 Model
      </h3>
      
      {modelFile ? (
        <div className="bg-gray-700 rounded-lg p-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Brain className="h-6 w-6 text-green-400" />
            <div>
              <p className="text-white font-medium">{modelFile.name}</p>
              <p className="text-gray-400 text-sm">
                {(modelFile.size / 1024 / 1024).toFixed(2)} MB
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
          className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center hover:border-green-500 transition-colors duration-200 cursor-pointer"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => document.getElementById('model-upload')?.click()}
        >
          <Brain className="h-12 w-12 text-gray-500 mx-auto mb-4" />
          <p className="text-gray-400 mb-2">
            Upload YOLOv8 model file
          </p>
          <p className="text-gray-500 text-sm">
            Supported formats: .pt, .onnx, .engine
          </p>
          <input
            id="model-upload"
            type="file"
            accept=".pt,.onnx,.engine"
            onChange={handleFileChange}
            className="hidden"
          />
        </div>
      )}
    </div>
  );
};

export default ModelUploader;