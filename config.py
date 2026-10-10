"""Shared application configuration and filesystem/database helpers."""

from __future__ import annotations

import os
from pathlib import Path

import mysql.connector


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ASSET_DIR = BASE_DIR / "college_images"
MODEL_PATH = BASE_DIR / "classifier.xml"
CASCADE_PATH = BASE_DIR / "haarcascade_frontalface_default.xml"
ATTENDANCE_PATH = BASE_DIR / "vishnu.csv"
MODEL_DIR = BASE_DIR / "models"
YUNET_PATH = MODEL_DIR / "face_detection_yunet_2023mar.onnx"
SFACE_PATH = MODEL_DIR / "face_recognition_sface_2021dec.onnx"
EMBEDDINGS_PATH = BASE_DIR / "face_embeddings.npz"

DB_CONFIG = {
    "host": os.getenv("FACE_DB_HOST", "localhost"),
    "user": os.getenv("FACE_DB_USER", "root"),
    "password": os.getenv("FACE_DB_PASSWORD", "root@123"),
    "database": os.getenv("FACE_DB_NAME", "face_recognition"),
}


def asset_path(filename: str) -> str:
    """Return an absolute path for an image or other bundled asset."""
    return str(ASSET_DIR / filename)


def connect_db():
    """Open a database connection using environment-configurable settings."""
    return mysql.connector.connect(**DB_CONFIG)


def ensure_data_dir() -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return DATA_DIR
