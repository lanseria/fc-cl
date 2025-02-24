import face_recognition
from PIL import Image
import numpy as np

def load_image(image_path: str) -> np.ndarray:
    """加载并验证图像文件"""
    try:
        image = face_recognition.load_image_file(image_path)
        return image
    except FileNotFoundError:
        raise ValueError(f"Image not found: {image_path}")
    except Exception as e:
        raise RuntimeError(f"Error loading image: {str(e)}")

def get_face_encoding(image: np.ndarray) -> np.ndarray:
    """提取单张人脸编码"""
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        raise ValueError("No face detected in image")
    return encodings[0]

def calculate_similarity(encoding1: np.ndarray, encoding2: np.ndarray) -> float:
    """计算相似度评分（0-1）"""
    distance = face_recognition.face_distance([encoding1], encoding2)[0]
    return float(1 - distance)  # 转换为相似度百分比