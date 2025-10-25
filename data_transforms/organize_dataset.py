import json
import os
import random
import shutil

TRAIN_RATIO = 0.9
VAL_RATIO = 0.0
TEST_RATIO = 0.1

VIDEO_DIR = ".bin/videos"
EVENTS_DIR = ".bin/events"
DATASET_DIR = "dataset"


def create_dataset(train_ratio=TRAIN_RATIO, val_ratio=VAL_RATIO, test_ratio=TEST_RATIO):
    """
    Create dataset following HuggingFace conventions:

    HuggingFace datasets typically use:
    - JSONL format (JSON Lines): One JSON object per line for each sample
    - Separate splits: train.jsonl, validation.jsonl, test.jsonl
    - Organized file structure: Raw data in subdirectories (videos/, annotations/)
    - Relative paths: Split files reference data using relative paths
    - Metadata included: Each sample contains all relevant metadata inline

    This allows easy loading with:
        from datasets import load_dataset
        dataset = load_dataset('json', data_files={'train': 'train.jsonl', 'test': 'test.jsonl'})

    Or manual loading:
        with open('train.jsonl') as f:
            for line in f:
                sample = json.loads(line)
                video_path = sample['video']  # e.g., "videos/abc123.mp4"
    """

    if os.path.exists(DATASET_DIR):
        shutil.rmtree(DATASET_DIR)

    videos_out = os.path.join(DATASET_DIR, "videos")
    annotations_out = os.path.join(DATASET_DIR, "annotations")
    os.makedirs(videos_out, exist_ok=True)
    os.makedirs(annotations_out, exist_ok=True)

    video_files = {f.replace(".mp4", ""): f for f in os.listdir(VIDEO_DIR) if f.endswith(".mp4")}
    annotation_files = {
        f.replace(".json", ""): f for f in os.listdir(EVENTS_DIR) if f.endswith(".json")
    }
    matched_ids = list(set(video_files.keys()) & set(annotation_files.keys()))

    for video_id in matched_ids:
        shutil.copy2(
            os.path.join(VIDEO_DIR, video_files[video_id]),
            os.path.join(videos_out, video_files[video_id]),
        )
        shutil.copy2(
            os.path.join(EVENTS_DIR, annotation_files[video_id]),
            os.path.join(annotations_out, annotation_files[video_id]),
        )

    random.shuffle(matched_ids)
    train_end = int(len(matched_ids) * train_ratio)
    val_end = train_end + int(len(matched_ids) * val_ratio)

    splits = {
        "train": matched_ids[:train_end],
        "validation": matched_ids[train_end:val_end],
        "test": matched_ids[val_end:],
    }

    for split_name, split_ids in splits.items():
        if not split_ids:
            continue

        split_data = []
        for video_id in split_ids:
            split_data.append(
                {
                    "video_id": video_id,
                    "video": f"videos/{video_files[video_id]}",
                    "annotation": f"annotations/{annotation_files[video_id]}",
                }
            )

        with open(os.path.join(DATASET_DIR, f"{split_name}.jsonl"), "w") as f:
            for sample in split_data:
                f.write(json.dumps(sample) + "\n")

    print(f"Dataset: {DATASET_DIR}")
    print(
        f"Train: {len(splits['train'])} | Val: {len(splits['validation'])} | Test: {len(splits['test'])}"
    )
    print(f"Total: {len(matched_ids)} matched pairs")


if __name__ == "__main__":
    create_dataset()
