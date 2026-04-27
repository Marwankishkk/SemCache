import re

import numpy as np


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def normalize_text(text: str) -> str:
    text = text.strip()
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text
