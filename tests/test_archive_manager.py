import os
import io
import hashlib
import pytest
import shutil
from etl_scripts import archive_manager as am


@pytest.fixture
def setup_dirs(tmp_path):
    """Create temporary directories for raw, processed, and archive."""
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    archive_dir = tmp_path / "archive"

    raw_dir.mkdir()
    processed_dir.mkdir()
    archive_dir.mkdir()
    return raw_dir, processed_dir, archive_dir


def _create_file(path, content="sample"):
    """Helper to create a file with given content."""
    with open(path, "w") as f:
        f.write(content)
    return path


def test_is_already_processed_by_name(setup_dirs):
    raw_dir, processed_dir, _ = setup_dirs
    test_file = _create_file(raw_dir / "data.csv")
    _create_file(processed_dir / "data.csv")

    assert am.is_already_processed_by_name(str(test_file), str(processed_dir)) is True

'''
def test_is_already_processed_by_checksum(setup_dirs):
    raw_dir, processed_dir, _ = setup_dirs
    f1 = _create_file(raw_dir / "f1.csv", "abc123")
    f2 = _create_file(processed_dir / "f2.csv", "abc123")

    result = am.is_already_processed_by_checksum(str(f1), str(processed_dir))
    assert result is True


def test_is_not_processed_by_checksum(setup_dirs):
    raw_dir, processed_dir, _ = setup_dirs
    f1 = _create_file(raw_dir / "f1.csv", "abc123")
    f2 = _create_file(processed_dir / "f2.csv", "xyz999")

    result = am.is_already_processed_by_checksum(str(f1), str(processed_dir))
    assert result is False
'''

def test_move_to_archive_creates_timestamp_folder(setup_dirs):
    raw_dir, _, archive_dir = setup_dirs
    test_file = _create_file(raw_dir / "x.csv")
    moved_path = am.move_to_archive(str(test_file), str(archive_dir))

    # Folder and file should now exist
    assert os.path.exists(moved_path)
    assert "x.csv" in moved_path
    assert os.path.exists(os.path.dirname(moved_path))


def test_handle_file_new(setup_dirs):
    raw_dir, processed_dir, archive_dir = setup_dirs
    test_file = _create_file(raw_dir / "fresh.csv")

    result = am.handle_file(str(test_file), str(processed_dir), str(archive_dir))
    assert result == "new"


def test_handle_file_already_processed(setup_dirs):
    raw_dir, processed_dir, archive_dir = setup_dirs
    test_file = _create_file(raw_dir / "old.csv", "samecontent")
    _create_file(processed_dir / "old.csv", "samecontent")

    result = am.handle_file(str(test_file), str(processed_dir), str(archive_dir))
    assert result == "archived"
    # file should have moved from raw to archive
    assert not os.path.exists(test_file)
    assert len(os.listdir(archive_dir)) > 0


def test_handle_file_missing(setup_dirs):
    _, processed_dir, archive_dir = setup_dirs
    fake_file = "non_existent.csv"

    result = am.handle_file(fake_file, str(processed_dir), str(archive_dir))
    assert result == "missing"
