import React from 'react';
import { Eye, Target, Clock } from 'lucide-react';
import { DetectionResult } from '../types/detection';

interface DetectionResultsProps {
  results: DetectionResult[];
  currentFrame: number;
}

const DetectionResults: React.FC<DetectionResultsProps> = ({ results, currentFrame }) => {
  const currentResult = results.find(
    result => Math.abs(result.frameNumber - currentFrame) < 15
  );

  const totalDetections = results.reduce(
    (total, result) => total + result.detections.length,
    0
  );

  const classStats = results.reduce((stats, result) => {
    result.detections.forEach(detection => {
      stats[detection.className] = (stats[detection.className] || 0) + 1;
    });
    return stats;
  }, {} as Record<string, number>);

  return (
    <div className="bg-gray-800 rounded-lg p-6">
      <h3 className="text-white font-semibold mb-6 flex items-center">
        <Target className="h-5 w-5 mr-2" />
        Detection Results
      </h3>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Detections</p>
              <p className="text-2xl font-bold text-white">{totalDetections}</p>
            </div>
            <Eye className="h-8 w-8 text-blue-400" />
          </div>
        </div>

        <div className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Processed Frames</p>
              <p className="text-2xl font-bold text-white">{results.length}</p>
            </div>
            <Clock className="h-8 w-8 text-green-400" />
          </div>
        </div>

        <div className="bg-gray-700 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Current Frame</p>
              <p className="text-2xl font-bold text-white">{currentFrame}</p>
            </div>
            <Target className="h-8 w-8 text-purple-400" />
          </div>
        </div>
      </div>

      {/* Class Statistics */}
      <div className="mb-6">
        <h4 className="text-white font-medium mb-3">Detection Class Statistics</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
          {Object.entries(classStats).map(([className, count]) => (
            <div key={className} className="bg-gray-700 rounded px-3 py-2">
              <p className="text-white font-medium capitalize">{className}</p>
              <p className="text-gray-400 text-sm">{count} detections</p>
            </div>
          ))}
        </div>
      </div>

      {/* Current Frame Detection Results */}
      {currentResult && (
        <div>
          <h4 className="text-white font-medium mb-3">
            Current Frame Detections (Frame {currentResult.frameNumber})
          </h4>
          <div className="space-y-2">
            {currentResult.detections.map((detection, index) => (
              <div key={index} className="bg-gray-700 rounded-lg p-3">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-white font-medium capitalize">
                      {detection.className}
                    </p>
                    <p className="text-gray-400 text-sm">
                      Confidence: {(detection.confidence * 100).toFixed(1)}%
                    </p>
                  </div>
                  <div className="text-right">
                    <p className="text-gray-400 text-sm">
                      Position: ({detection.bbox.x}, {detection.bbox.y})
                    </p>
                    <p className="text-gray-400 text-sm">
                      Size: {detection.bbox.width} × {detection.bbox.height}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DetectionResults;