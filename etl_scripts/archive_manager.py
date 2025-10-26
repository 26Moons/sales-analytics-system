# etl_scripts/archive_manager.py
import os
import shutil
from datetime import datetime
import hashlib
from typing import Optional

from etl_scripts.utils import get_logger

logger = get_logger("archive_manager")


def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def compute_md5(path: str, chunk_size: int = 8192) -> str:
    """Compute MD5 checksum for a file (used optionally to detect duplicates)."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def is_already_processed_by_name(file_path: str, processed_dir: str) -> bool:
    """Check if a file with the same name exists in processed_dir."""
    file_name = os.path.basename(file_path)
    processed_path = os.path.join(processed_dir, file_name)
    exists = os.path.exists(processed_path)
    logger.debug("is_already_processed_by_name: %s -> %s", file_name, exists)
    return exists


def is_already_processed_by_checksum(file_path: str, processed_dir: str) -> bool:
    """
    (Optional) Check if the file checksum matches any file in processed_dir.
    Useful if filenames can repeat but content may differ.
    """
    try:
        target_md5 = compute_md5(file_path)
    except Exception as e:
        logger.warning("Failed to compute checksum for %s: %s", file_path, e)
        return False

    for fname in os.listdir(processed_dir):
        processed_file = os.path.join(processed_dir, fname)
        if not os.path.isfile(processed_file):
            continue
        try:
            if compute_md5(processed_file) == target_md5:
                logger.debug("Checksum match found: %s == %s", file_path, processed_file)
                return True
        except Exception:
            continue
    return False


def move_to_archive(file_path: str, archive_root: str, prefix: Optional[str] = None) -> str:
    """
    Move file to archive/{YYYY-MM-DD}/[prefix_]filename and return new path.
    Uses shutil.move (atomic on same filesystem).
    """
    _ensure_dir(archive_root)
    date_folder = datetime.now().strftime("%Y-%m-%d")
    dest_folder = os.path.join(archive_root, date_folder)
    _ensure_dir(dest_folder)

    file_name = os.path.basename(file_path)
    if prefix:
        dest_name = f"{prefix}_{file_name}"
    else:
        dest_name = file_name

    dest_path = os.path.join(dest_folder, dest_name)

    # If destination exists, avoid overwriting: append timestamp
    if os.path.exists(dest_path):
        suffix = datetime.now().strftime("%H%M%S")
        dest_name = f"{os.path.splitext(dest_name)[0]}_{suffix}{os.path.splitext(dest_name)[1]}"
        dest_path = os.path.join(dest_folder, dest_name)

    logger.info("Moving file %s -> %s", file_path, dest_path)
    shutil.move(file_path, dest_path)
    return dest_path


def handle_file(file_path: str, processed_dir: str, archive_root: str, use_checksum: bool = False) -> str:
    """
    Central entry:
    - If file already processed -> move to archive and return 'archived'
    - If not processed -> return 'new' (caller should process it)
    """
    # Normalize paths
    file_path = os.path.normpath(file_path)
    processed_dir = os.path.normpath(processed_dir)
    archive_root = os.path.normpath(archive_root)

    if not os.path.exists(file_path):
        logger.error("File does not exist: %s", file_path)
        return "missing"

    # Check by name first (fast)
    if is_already_processed_by_name(file_path, processed_dir):
        archived = move_to_archive(file_path, archive_root, prefix="already_processed")
        logger.info("File archived (already processed by name): %s", archived)
        return "archived"

    # Optional checksum check if filenames might repeat
    if use_checksum and is_already_processed_by_checksum(file_path, processed_dir):
        archived = move_to_archive(file_path, archive_root, prefix="duplicate_content")
        logger.info("File archived (duplicate by checksum): %s", archived)
        return "archived"

    # File is new
    logger.info("File is new and ready for processing: %s", file_path)
    return "new"
