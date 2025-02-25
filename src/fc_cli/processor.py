"""Core face processing logic"""

from pathlib import Path
from typing import Dict, Any
import time

import cv2
import numpy as np
from insightface.app import FaceAnalysis

from .utils import load_image
from .exceptions import FaceCompareError


class FaceProcessor:
    """Face comparison processor with InsightFace backend"""

    def __init__(self, model_name: str = "buffalo_l", providers: list = None, config: dict = None):
        self.model_name = model_name
        self.providers = providers or ["CPUExecutionProvider"]
        self.config = config or {}
        self._app = None

        # Initialize with lazy loading
        self._initialized = False

    def _initialize(self):
        """Lazy initialization of face analysis model"""
        if self._initialized:
            return

        try:
            self._app = FaceAnalysis(
                name=self.model_name,
                providers=self.providers,
                allowed_modules=['detection', 'recognition']
                )

            # Apply configuration
            self._app.prepare(
                ctx_id=0,
                det_size=self.config.get("det_size", (640, 640)),
                det_thresh=self.config.get("det_thresh", 0.5)
                )

            self._initialized = True

        except Exception as e:
            raise FaceCompareError(1003, f"Model initialization failed: {str(e)}")

    @property
    def app(self):
        """Get initialized face analysis application"""
        if not self._initialized:
            self._initialize()
        return self._app

    def compare(self, image1: Path, image2: Path) -> Dict[str, Any]:
        """Compare two face images and return detailed results"""
        start_time = time.time()

        # Load and process images
        img1 = load_image(image1)
        img2 = load_image(image2)

        # Detect faces
        faces1 = self._detect_faces(img1)
        faces2 = self._detect_faces(img2)

        # Extract embeddings
        embedding1 = self._get_embedding(faces1)
        embedding2 = self._get_embedding(faces2)

        # Calculate similarity
        similarity = self._cosine_similarity(embedding1, embedding2)

        return {
            "similarity": float(similarity),
            "detection_time": time.time() - start_time,
            "image1": str(image1.resolve()),
            "image2": str(image2.resolve()),
            "model": self.model_name,
            "faces_detected": {
                "image1": len(faces1),
                "image2": len(faces2)
                }
            }

    def _detect_faces(self, image: np.ndarray) -> list:
        """Detect faces in an image with error handling"""
        try:
            return self.app.get(image)
        except Exception as e:
            raise FaceCompareError(1001, f"Face detection failed: {str(e)}")

    def _get_embedding(self, faces: list) -> np.ndarray:
        """Validate and extract face embedding"""
        if len(faces) == 0:
            raise FaceCompareError(1001, "No faces detected")
        if len(faces) > 1:
            raise FaceCompareError(1001, "Multiple faces detected")
        return faces[0].normed_embedding

    @staticmethod
    def _cosine_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Calculate cosine similarity between embeddings"""
        return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
