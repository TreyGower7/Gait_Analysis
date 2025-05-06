import logging
from pathlib import Path
from zenml import step

@step
def ingest_images(image_dir: str) -> list:
    """
    ZenML step to ingest image file paths from a directory.

    Args:
        image_dir (str): Directory containing image files.

    Returns:
        list: List of image file paths as strings.
    """
    try:
        image_paths = list(Path(image_dir).glob("*.[jJpP]*[gGnN]"))
        if not image_paths:
            raise FileNotFoundError(f"No images found in {image_dir}")
        logging.info(f"✅ Found {len(image_paths)} image(s) in {image_dir}")
        return [str(p.resolve()) for p in image_paths]
    except Exception as e:
        logging.error(f"Failed to read image files from {image_dir}: {e}")
        raise
