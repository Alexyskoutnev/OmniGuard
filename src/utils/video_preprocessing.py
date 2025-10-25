"""
Video preprocessing pipeline for construction safety analysis with OmniVinci
"""

import cv2
import numpy as np
import librosa
from moviepy import VideoFileClip
from pathlib import Path
import json
from typing import List, Dict, Tuple, Optional
from config import VIDEO_CONFIG, AUDIO_CONFIG, DATASET_DIR, OUTPUT_DIR

class VideoPreprocessor:
    """Handles video preprocessing for OmniVinci model."""

    def __init__(self):
        self.max_frames = VIDEO_CONFIG["max_frames"]
        self.target_fps = VIDEO_CONFIG["fps"]
        self.target_resolution = VIDEO_CONFIG["resolution"]
        self.max_duration = VIDEO_CONFIG["max_duration"]
        self.audio_sample_rate = AUDIO_CONFIG["sample_rate"]
        self.load_audio = AUDIO_CONFIG["load_audio"]

    def extract_frames(self, video_path: Path, target_fps: int = None) -> List[np.ndarray]:
        """Extract frames from video at specified FPS."""

        if target_fps is None:
            target_fps = self.target_fps

        cap = cv2.VideoCapture(str(video_path))
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Calculate frame sampling interval
        frame_interval = max(1, int(original_fps / target_fps))

        frames = []
        frame_idx = 0

        while len(frames) < self.max_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()

            if not ret:
                break

            # Resize frame if needed
            if self.target_resolution:
                frame = cv2.resize(frame, self.target_resolution)

            frames.append(frame)
            frame_idx += frame_interval

        cap.release()
        return frames

    def extract_audio(self, video_path: Path) -> Optional[np.ndarray]:
        """Extract audio from video file."""

        if not self.load_audio:
            return None

        try:
            # Load video with moviepy
            video = VideoFileClip(str(video_path))

            if video.audio is None:
                return None

            # Extract audio
            audio_path = str(video_path).replace('.mp4', '_temp_audio.wav')
            video.audio.write_audiofile(audio_path, verbose=False, logger=None)

            # Load with librosa
            audio, sr = librosa.load(audio_path, sr=self.audio_sample_rate)

            # Clean up temporary file
            Path(audio_path).unlink(missing_ok=True)
            video.close()

            return audio

        except Exception as e:
            print(f"Error extracting audio from {video_path}: {e}")
            return None

    def analyze_video_content(self, frames: List[np.ndarray]) -> Dict:
        """Analyze video content for construction safety elements."""

        analysis = {
            "frame_count": len(frames),
            "brightness_stats": [],
            "motion_detected": False,
            "color_distribution": {},
            "potential_safety_elements": []
        }

        if not frames:
            return analysis

        # Analyze brightness across frames
        for i, frame in enumerate(frames):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)
            analysis["brightness_stats"].append({
                "frame": i,
                "brightness": float(brightness)
            })

        # Simple motion detection (frame difference)
        if len(frames) > 1:
            for i in range(1, len(frames)):
                diff = cv2.absdiff(frames[i-1], frames[i])
                motion_score = np.mean(diff)
                if motion_score > 30:  # Threshold for motion
                    analysis["motion_detected"] = True
                    break

        # Color analysis (detect high-vis safety colors)
        sample_frame = frames[len(frames)//2]  # Use middle frame
        hsv = cv2.cvtColor(sample_frame, cv2.COLOR_BGR2HSV)

        # Detect safety colors (orange, yellow, green ranges in HSV)
        safety_colors = {
            "orange": {"lower": (5, 50, 50), "upper": (15, 255, 255)},
            "yellow": {"lower": (15, 50, 50), "upper": (35, 255, 255)},
            "green": {"lower": (35, 50, 50), "upper": (85, 255, 255)}
        }

        for color_name, color_range in safety_colors.items():
            mask = cv2.inRange(hsv, color_range["lower"], color_range["upper"])
            percentage = (np.sum(mask > 0) / mask.size) * 100
            analysis["color_distribution"][color_name] = float(percentage)

            if percentage > 5:  # If more than 5% of frame is safety color
                analysis["potential_safety_elements"].append(f"{color_name}_safety_gear")

        return analysis

    def preprocess_video(self, video_path: Path) -> Dict:
        """Complete preprocessing pipeline for a single video."""

        print(f"Preprocessing: {video_path.name}")

        result = {
            "source_path": str(video_path),
            "filename": video_path.name,
            "preprocessing_status": "failed",
            "frames": None,
            "audio": None,
            "content_analysis": {},
            "metadata": {}
        }

        try:
            # Extract frames
            frames = self.extract_frames(video_path)
            if not frames:
                result["error"] = "No frames extracted"
                return result

            result["frames"] = frames
            result["metadata"]["extracted_frames"] = len(frames)

            # Extract audio if enabled
            if self.load_audio:
                audio = self.extract_audio(video_path)
                result["audio"] = audio
                result["metadata"]["audio_extracted"] = audio is not None

            # Analyze content
            content_analysis = self.analyze_video_content(frames)
            result["content_analysis"] = content_analysis

            result["preprocessing_status"] = "success"
            print(f"  Extracted {len(frames)} frames")
            print(f"  Audio: {'Yes' if result['audio'] is not None else 'No'}")
            print(f"  Safety colors detected: {list(content_analysis['color_distribution'].keys())}")

        except Exception as e:
            result["error"] = str(e)
            print(f"  Error: {e}")

        return result

    def preprocess_dataset(self) -> List[Dict]:
        """Preprocess all videos in the dataset."""

        print("Video Preprocessing Pipeline")
        print("=" * 50)

        video_files = list(DATASET_DIR.glob("*.mp4"))
        if not video_files:
            print("No video files found in dataset")
            return []

        results = []
        for video_file in video_files:
            result = self.preprocess_video(video_file)
            results.append(result)

        # Save preprocessing results
        output_file = OUTPUT_DIR / "preprocessing_results.json"

        # Convert numpy arrays to lists for JSON serialization
        json_results = []
        for result in results:
            json_result = result.copy()
            if result["frames"] is not None:
                json_result["frames"] = f"<{len(result['frames'])} frames extracted>"
            if result["audio"] is not None:
                json_result["audio"] = f"<audio array of length {len(result['audio'])}>"
            json_results.append(json_result)

        with open(output_file, 'w') as f:
            json.dump(json_results, f, indent=2)

        print(f"\nPreprocessing results saved to: {output_file}")

        # Summary
        successful = [r for r in results if r["preprocessing_status"] == "success"]
        print(f"\nSummary:")
        print(f"Total videos processed: {len(results)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(results) - len(successful)}")

        return results

def main():
    """Main preprocessing function."""

    preprocessor = VideoPreprocessor()
    results = preprocessor.preprocess_dataset()

    print("\nPreprocessing complete!")
    print("Ready for annotation and fine-tuning setup.")

if __name__ == "__main__":
    main()