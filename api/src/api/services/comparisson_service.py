import cv2
import numpy as np

def compare_images(before_path: str, after_path: str, diff_path: str):
    before, after = load_images(before_path, after_path)

    after = is_same_seize(before, after)

    diff = cv2.absdiff(before, after)

    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

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

def count_changed_pixels(thresh):
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
