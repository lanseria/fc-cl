"""Command-line interface entry point"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .processor import FaceProcessor
from .utils import handle_output, load_config
from .exceptions import FaceCompareError

app = typer.Typer(help="Face Comparison CLI Tool", add_completion=False)
console = Console()


@app.command()
def compare(
        image1: Path = typer.Argument(..., help="First image path", exists=True),
        image2: Path = typer.Argument(..., help="Second image path", exists=True),
        model: str = typer.Option("buffalo_l", "--model", "-m", help="Model name (buffalo_l, buffalo_sc, antelopev2)"),
        threshold: float = typer.Option(
            0.6, "--threshold", "-t", min=0.0, max=1.0, help="Similarity threshold"),
        output: Optional[Path] = typer.Option(
            None, "--output", "-o", help="Output file path"),
        format: str = typer.Option(
            "text", "--format", "-f", help="Output format (text, json, table)"),
        gpu: bool = typer.Option(False, "--gpu", help="Enable GPU acceleration"),
        config: Path = typer.Option(
            Path("configs/default.toml"), "--config", "-c", help="Configuration file path")
        ):
    """Compare two face images and output similarity results"""
    try:
        # Load configuration
        cfg = load_config(config)

        # Initialize processor
        processor = FaceProcessor(
            model_name=model,
            providers=["CUDAExecutionProvider"] if gpu else [
                "CPUExecutionProvider"],
            config=cfg
            )

        # Process comparison
        result = processor.compare(image1, image2)

        # Handle output
        handle_output(result, threshold, output, format)

    except FaceCompareError as e:
        console.print(f"[bold red]Error {e.code}:[/] {e.message}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/] {str(e)}")
        sys.exit(2)


if __name__ == "__main__":
    compare()
