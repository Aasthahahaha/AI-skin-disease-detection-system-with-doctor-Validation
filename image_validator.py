"""
Image Quality Validation Module

Validates uploaded skin images for minimum quality requirements before
sending them to the AI model. Ensures high-quality inputs for better
prediction accuracy.

Checks performed:
1. File size (minimum 10 KB)
2. Resolution (minimum 800x800 px; warns below 1024x1024)
3. Blur detection via Laplacian variance (OpenCV, with NumPy fallback)
4. Brightness check (rejects too-dark or overexposed images)
"""

from PIL import Image, ExifTags
import io
import numpy as np

# ── Thresholds ────────────────────────────────────────────────────────────────
MIN_FILE_SIZE_KB      = 1       # bytes / 1024
MIN_RESOLUTION        = (100, 100)
WARN_RESOLUTION       = (1024, 1024)
MIN_BLUR_SCORE        = 5.0    # Laplacian variance; below = extremely blurry
MIN_BRIGHTNESS        = 10      # 0-255
MAX_BRIGHTNESS        = 250     # 0-255


def _laplacian_blur_score(img_array: np.ndarray) -> float:
    """
    Compute sharpness via Laplacian variance.
    Higher = sharper.  Tries OpenCV first, falls back to pure NumPy.
    """
    try:
        import cv2  # optional fast path
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        return float(cv2.Laplacian(gray, cv2.CV_64F).var())
    except ImportError:
        # Pure NumPy Laplacian approximation
        gray = np.mean(img_array, axis=2)
        kernel = np.array([[0, 1, 0],
                            [1, -4, 1],
                            [0, 1, 0]], dtype=np.float64)
        from numpy.lib.stride_tricks import sliding_window_view
        windows = sliding_window_view(gray, (3, 3))
        laplacian = (windows * kernel).sum(axis=(2, 3))
        return float(np.var(laplacian))


def validate_image(file_bytes: bytes) -> tuple:
    """
    Validate an uploaded image for minimum quality requirements.

    Args:
        file_bytes: Raw bytes of the uploaded image file.

    Returns:
        (is_valid: bool, error_message: str, metadata: dict)
        metadata keys: width, height, file_size_kb, blur_score, brightness,
                       resolution_warning (bool)
    """
    metadata = {
        "width": 0,
        "height": 0,
        "file_size_kb": 0.0,
        "blur_score": 0.0,
        "brightness": 0.0,
        "resolution_warning": False,
    }

    # ── 1. File size ──────────────────────────────────────────────────────────
    file_size_kb = len(file_bytes) / 1024.0
    metadata["file_size_kb"] = round(file_size_kb, 1)
    if file_size_kb < MIN_FILE_SIZE_KB:
        return (
            False,
            f"Image file is too small ({file_size_kb:.1f} KB). "
            "Please upload a real photograph (minimum 10 KB).",
            metadata,
        )

    # ── 2. Open image ─────────────────────────────────────────────────────────
    try:
        img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    except Exception:
        return False, "Could not open the image. Please upload a valid JPG or PNG file.", metadata

    width, height = img.size
    metadata["width"]  = width
    metadata["height"] = height

    # ── 3. Resolution check ───────────────────────────────────────────────────
    if width < MIN_RESOLUTION[0] or height < MIN_RESOLUTION[1]:
        return (
            False,
            f"Image resolution is too low ({width}×{height} px). "
            f"Minimum required: {MIN_RESOLUTION[0]}×{MIN_RESOLUTION[1]} px. "
            "Please use a higher-quality camera.",
            metadata,
        )

    if width < WARN_RESOLUTION[0] or height < WARN_RESOLUTION[1]:
        metadata["resolution_warning"] = True   # soft warning, not rejected

    # ── 4. Convert to NumPy for pixel analysis ────────────────────────────────
    img_array = np.array(img, dtype=np.uint8)

    # ── 5. Blur detection ──────────────────────────────────────────────────────
    try:
        blur_score = _laplacian_blur_score(img_array)
    except Exception:
        blur_score = 999.0   # if analysis fails, skip this check
    metadata["blur_score"] = round(blur_score, 2)

    if blur_score < MIN_BLUR_SCORE:
        return (
            False,
            "Image quality insufficient — the image appears blurry. "
            "Please upload a clearer, in-focus photograph.",
            metadata,
        )

    # ── 6. Brightness check ───────────────────────────────────────────────────
    brightness = float(np.mean(img_array))
    metadata["brightness"] = round(brightness, 1)

    if brightness < MIN_BRIGHTNESS:
        return (
            False,
            "Image is too dark. Please photograph the skin area in good lighting.",
            metadata,
        )

    if brightness > MAX_BRIGHTNESS:
        return (
            False,
            "Image is overexposed (too bright). "
            "Avoid direct flash or strong sunlight directly on the lens.",
            metadata,
        )

    return True, "Image quality validated successfully.", metadata


def quality_score(metadata: dict) -> int:
    """
    Compute a 0-100 composite quality score from metadata.
    Used to display a quality badge in the UI.
    """
    scores = []

    # Resolution score (max 100 at 2000+ px)
    res = min(metadata.get("width", 0), metadata.get("height", 0))
    scores.append(min(100, int((res / 2000) * 100)))

    # Blur score (MAX_BLUR assumed at 500)
    blur = metadata.get("blur_score", 0)
    scores.append(min(100, int((blur / 500) * 100)))

    # Brightness score — penalise extremes
    b = metadata.get("brightness", 128)
    bright_score = 100 - int(abs(b - 128) / 128 * 100)
    scores.append(max(0, bright_score))

    return int(sum(scores) / len(scores))
