"""Utility functions for face comparison"""

from pathlib import Path
from typing import Dict, Any, Optional
import json

import cv2
import numpy as np
from rich.table import Table
from rich.console import Console


def load_image(path: Path) -> np.ndarray:
    """Load image with validation and format conversion"""
    try:
        # Read with OpenCV
        img = cv2.imread(str(path))
        if img is None:
            raise ValueError("Invalid image file")

        # Convert BGR to RGB
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    except Exception as e:
        raise ValueError(f"Failed to load image: {str(e)}") from e


def handle_output(result: Dict[str, Any], threshold: float, output: Optional[Path], format: str) -> None:
    """Handle output formatting and display"""
    console = Console()
    verified = result["similarity"] >= threshold

    output_data = {
        "verified": verified,
        "similarity": round(result["similarity"], 4),
        "threshold": threshold,
        "detection_time": round(result["detection_time"], 3),
        "model": result["model"],
        "images": {
            "image1": result["image1"],
            "image2": result["image2"]
            },
        "faces_detected": result["faces_detected"]
        }

    if format == "json":
        output_str = json.dumps(output_data, indent=2)
    elif format == "table":
        output_str = _format_table(output_data)
    else:  # text format
        output_str = _format_text(output_data)

    if output:
        _write_output(output_str, output, format)
    else:
        console.print(output_str)


def _format_text(data: Dict) -> str:
    """Format results as plain text"""
    return (
        f"Comparison Result:\n"
        f"  Images: {data['images']['image1']} vs {data['images']['image2']}\n"
        f"  Verified: {'✅' if data['verified'] else '❌'}\n"
        f"  Similarity: {data['similarity']:.2%}\n"
        f"  Threshold: {data['threshold']:.2%}\n"
        f"  Model: {data['model']}\n"
        f"  Detection Time: {data['detection_time']:.2f}s\n"
        f"  Faces Detected: Image1={data['faces_detected']['image1']}, "
        f"Image2={data['faces_detected']['image2']}"
        )


def _format_table(data: Dict) -> str:
    """Format results as rich table"""
    table = Table(title="Face Comparison Results", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Verification Status", "✅ Verified" if data['verified'] else "❌ Not Verified")
    table.add_row("Similarity Score", f"{data['similarity']:.2%}")
    table.add_row("Threshold", f"{data['threshold']:.2%}")
    table.add_row("Detection Time", f"{data['detection_time']:.3f} seconds")
    table.add_row("Model Used", data['model'])
    table.add_row("Image 1 Path", data['images']['image1'])
    table.add_row("Image 2 Path", data['images']['image2'])
    table.add_row("Faces Detected",
                  f"Image 1: {data['faces_detected']['image1']}, Image 2: {data['faces_detected']['image2']}")

    console = Console()
    with console.capture() as capture:
        console.print(table)
    return capture.get()


def _write_output(content: str, path: Path, format: str) -> None:
    """Write output to file with format validation"""
    suffix = path.suffix.lower()

    if format == "json" and suffix != ".json":
        path = path.with_suffix(".json")
    elif format == "table" and suffix not in (".txt", ".md"):
        path = path.with_suffix(".txt")

    path.write_text(content, encoding="utf-8")


def load_config(config_path: Path) -> Dict[str, Any]:
    """Load configuration from TOML file"""
    try:
        import tomli
        with open(config_path, "rb") as f:
            return tomli.load(f)
    except ImportError:
        raise RuntimeError("TOML parser required: pip install tomli")
    except Exception as e:
        raise RuntimeError(f"Failed to load config: {str(e)}")
