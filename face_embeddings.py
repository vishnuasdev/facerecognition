"""OpenCV YuNet/SFace face detection and embedding utilities."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import cv2
import numpy as np

from config import EMBEDDINGS_PATH, SFACE_PATH, YUNET_PATH

YUNET_URL = (
    "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/"
    "face_detection_yunet_2023mar.onnx"
)
SFACE_URL = (
    "https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/"
    "face_recognition_sface_2021dec.onnx"
)
MIN_FACE_SIZE = 90
MIN_BLUR_SCORE = 45.0
MIN_BRIGHTNESS = 35.0
MAX_BRIGHTNESS = 225.0
MATCH_THRESHOLD = 0.42


def model_error() -> str:
    return (
        "Embedding models are missing. Download these files into the models folder:\n"
        f"{YUNET_URL}\n{SFACE_URL}"
    )


def create_detector():
    if not YUNET_PATH.exists():
        raise FileNotFoundError(model_error())
    return cv2.FaceDetectorYN.create(
        str(YUNET_PATH), "", (320, 320), 0.85, 0.3, 5000
    )


def create_recognizer():
    if not SFACE_PATH.exists():
        raise FileNotFoundError(model_error())
    return cv2.FaceRecognizerSF.create(str(SFACE_PATH), "")


def quality_reason(face: np.ndarray) -> str | None:
    if face.size == 0:
        return "No face image"
    height, width = face.shape[:2]
    if min(height, width) < MIN_FACE_SIZE:
        return "Move closer"
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    brightness = float(gray.mean())
    if blur_score < MIN_BLUR_SCORE:
        return "Hold still"
    if brightness < MIN_BRIGHTNESS or brightness > MAX_BRIGHTNESS:
        return "Improve lighting"
    return None


def detect_faces(detector, frame: np.ndarray) -> np.ndarray:
    detector.setInputSize((frame.shape[1], frame.shape[0]))
    _, faces = detector.detect(frame)
    return faces if faces is not None else np.empty((0, 15), dtype=np.float32)


def embedding(recognizer, frame: np.ndarray, face: np.ndarray) -> np.ndarray:
    aligned = recognizer.alignCrop(frame, face)
    feature = recognizer.feature(aligned)
    return cv2.normalize(feature, None).flatten().astype(np.float32)


def enroll_dataset(data_dir: Path) -> tuple[dict[str, np.ndarray], int]:
    detector = create_detector()
    recognizer = create_recognizer()
    grouped: dict[str, list[np.ndarray]] = defaultdict(list)
    skipped = 0
    for image_path in sorted(data_dir.glob("user.*.*.*")):
        if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        try:
            student_id = image_path.name.split(".")[1]
            frame = cv2.imread(str(image_path))
            if frame is None:
                skipped += 1
                continue
            faces = detect_faces(detector, frame)
            if len(faces) != 1:
                skipped += 1
                continue
            x, y, width, height = faces[0, :4].astype(int)
            face_crop = frame[max(y, 0):y + height, max(x, 0):x + width]
            if quality_reason(face_crop):
                skipped += 1
                continue
            grouped[student_id].append(embedding(recognizer, frame, faces[0]))
        except (OSError, ValueError, IndexError, cv2.error):
            skipped += 1
    if not grouped:
        raise ValueError("No usable face images found. Capture clear face samples first.")
    profiles = {
        student_id: cv2.normalize(np.mean(features, axis=0).reshape(1, -1), None).flatten()
        for student_id, features in grouped.items()
    }
    np.savez_compressed(
        EMBEDDINGS_PATH,
        ids=np.array(list(profiles.keys())),
        embeddings=np.array(list(profiles.values()), dtype=np.float32),
    )
    return profiles, skipped


def load_profiles() -> dict[str, np.ndarray]:
    if not EMBEDDINGS_PATH.exists():
        raise FileNotFoundError(
            "face_embeddings.npz is missing. Open Train Photos and train embeddings first."
        )
    stored = np.load(EMBEDDINGS_PATH, allow_pickle=False)
    return {
        str(student_id): vector
        for student_id, vector in zip(stored["ids"], stored["embeddings"])
    }


def match_embedding(feature: np.ndarray, profiles: dict[str, np.ndarray]):
    if not profiles:
        return None, 0.0
    scores = {
        student_id: float(
            recognizer_score(feature, profile)
        )
        for student_id, profile in profiles.items()
    }
    student_id, score = max(scores.items(), key=lambda item: item[1])
    return (student_id, score) if score >= MATCH_THRESHOLD else (None, score)


def recognizer_score(first: np.ndarray, second: np.ndarray) -> float:
    return float(cv2.norm(first, second, cv2.NORM_COSINE))
