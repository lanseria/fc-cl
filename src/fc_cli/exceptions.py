"""Custom exceptions for face comparison"""


class FaceCompareError(Exception):
    """Base exception for face comparison errors"""

    ERROR_CODES = {
        1000: "General Error",
        1001: "Face Detection Failed",
        1002: "Image Loading Error",
        1003: "Model Initialization Failed",
        1004: "Invalid Configuration"
        }

    def __init__(self, code: int, message: str = None):
        self.code = code
        self.message = message or self.ERROR_CODES.get(code, "Unknown Error")
        super().__init__(f"[Error {code}] {self.message}")
