"""
Analyze existing video files in the dataset
"""

import cv2
import os
from pathlib import Path
import json
from config import DATASET_DIR

def analyze_video(video_path):
    """Analyze a single video file and return metadata."""

    try:
        cap = cv2.VideoCapture(str(video_path))

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0

        # Get file size
        file_size = video_path.stat().st_size

        # Sample a few frames to check content
        sample_frames = []
        for i in range(0, min(frame_count, 5)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i * (frame_count // 5) if frame_count > 5 else i)
            ret, frame = cap.read()
            if ret:
                sample_frames.append({
                    "frame_number": i * (frame_count // 5) if frame_count > 5 else i,
                    "timestamp": (i * (frame_count // 5) / fps) if fps > 0 else 0
                })

        cap.release()

        return {
            "filename": video_path.name,
            "path": str(video_path),
            "resolution": f"{width}x{height}",
            "fps": fps,
            "frame_count": frame_count,
            "duration_seconds": duration,
            "file_size_mb": file_size / (1024 * 1024),
            "sample_frames": sample_frames,
            "analysis_status": "success"
        }

    except Exception as e:
        return {
            "filename": video_path.name,
            "path": str(video_path),
            "error": str(e),
            "analysis_status": "failed"
        }

def analyze_dataset():
    """Analyze all videos in the dataset directory."""

    print("Video Dataset Analysis")
    print("=" * 50)

    video_files = list(DATASET_DIR.glob("*.mp4"))

    if not video_files:
        print("No MP4 files found in dataset directory")
        return

    analysis_results = []

    for video_file in video_files:
        print(f"\nAnalyzing: {video_file.name}")
        result = analyze_video(video_file)
        analysis_results.append(result)

        if result["analysis_status"] == "success":
            print(f"  Resolution: {result['resolution']}")
            print(f"  Duration: {result['duration_seconds']:.2f} seconds")
            print(f"  FPS: {result['fps']:.2f}")
            print(f"  Frame count: {result['frame_count']}")
            print(f"  File size: {result['file_size_mb']:.2f} MB")
        else:
            print(f"  Error: {result['error']}")

    # Save analysis results
    output_file = Path("outputs") / "video_analysis.json"
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(analysis_results, f, indent=2)

    print(f"\nAnalysis results saved to: {output_file}")

    # Summary
    successful_analyses = [r for r in analysis_results if r["analysis_status"] == "success"]
    print(f"\nSummary:")
    print(f"Total videos: {len(analysis_results)}")
    print(f"Successfully analyzed: {len(successful_analyses)}")

    if successful_analyses:
        total_duration = sum(r["duration_seconds"] for r in successful_analyses)
        avg_duration = total_duration / len(successful_analyses)
        total_size = sum(r["file_size_mb"] for r in successful_analyses)

        print(f"Total duration: {total_duration:.2f} seconds")
        print(f"Average duration: {avg_duration:.2f} seconds")
        print(f"Total size: {total_size:.2f} MB")

        # Check if videos are suitable for OmniVinci
        print(f"\nOmniVinci Compatibility:")
        for result in successful_analyses:
            max_frames_at_4fps = result["duration_seconds"] * 4
            print(f"  {result['filename']}: {max_frames_at_4fps:.0f} frames at 4 FPS (limit: 128)")
            if max_frames_at_4fps > 128:
                print(f"    Warning: Video too long, will need trimming or frame sampling")

if __name__ == "__main__":
    analyze_dataset()