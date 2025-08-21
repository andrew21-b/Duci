import cv2
import numpy as np
from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException
from src.api.models.comparison import Comparison

STORAGE = Path("comparisons")
STORAGE.mkdir(exist_ok=True)

def compare_images(before_path: str, after_path: str, diff_path: str, threshold: int) -> float:
    before, after = load_images(before_path, after_path)

    after = is_same_seize(before, after)

    diff = cv2.absdiff(before, after)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    diff_percent = count_changed_pixels(thresh)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    highlight = after.copy()
    for c in contours:
        if cv2.contourArea(c) < 50:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(highlight, (x, y), (x+w, y+h), (0, 0, 255), 2)

    cv2.imwrite(diff_path, highlight)

    return diff_percent

def count_changed_pixels(thresh) -> float:
    diff_pixels = np.count_nonzero(thresh)
    total_pixels = thresh.size
    return (diff_pixels / total_pixels) * 100

def load_images(before_path, after_path):
    before = cv2.imread(before_path)
    after = cv2.imread(after_path)

    if before is None or after is None:
        raise ValueError("One or both images could not be loaded.")
    return before,after

def is_same_seize(before, after):
    if before.shape != after.shape:
        after = cv2.resize(after, (before.shape[1], before.shape[0]))
    return after


def initialize_comparison_resources():
    comp_id = str(uuid4())
    comp_dir = STORAGE / comp_id
    try:
        comp_dir.mkdir()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create comparison resources: {e}")
    return comp_id, comp_dir

def generate_image_paths(comp_dir):
    before_path = (comp_dir / "before.png").resolve()
    after_path = (comp_dir / "after.png").resolve()
    diff_path = (comp_dir / "diff.png").resolve()
    return str(before_path), str(after_path), str(diff_path)

def get_comparison_by_id(comp_id, db):
    comparison = db.query(Comparison).filter(Comparison.id == comp_id).first()
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")
    return comparison