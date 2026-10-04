"""
Unit tests for Virtual Filesystem (VFS).
"""

import pytest
from phantasm_os.core.models import FileType
from phantasm_os.core.vfs import VirtualFileSystem


@pytest.fixture
def vfs():
    return VirtualFileSystem(seed_defaults=True)


def test_path_normalization():
    norm = VirtualFileSystem.normalize_path
    assert norm("") == "C:\\"
    assert norm("C:") == "C:\\"
    assert norm("c:/windows/system") == "C:\\WINDOWS\\SYSTEM"
    assert norm("/mydocs/test.txt") == "C:\\MYDOCS\\TEST.TXT"
    assert norm("C:\\WINDOWS\\..\\MYDOCS") == "C:\\MYDOCS"
    assert norm("C:\\MYDOCS\\.\\NOTE.TXT") == "C:\\MYDOCS\\NOTE.TXT"


def test_seed_files_present(vfs):
    assert vfs.exists("C:\\AUTOEXEC.BAT")
    assert vfs.exists("C:\\CONFIG.SYS")
    assert vfs.exists("C:\\README.TXT")
    assert vfs.exists("C:\\WINDOWS\\SYSTEM.INI")
    assert vfs.exists("C:\\SYSTEM\\LOGS\\KERNEL_BOOT.LOG")
    assert vfs.exists("C:\\RESTRICTED\\CHIMERA.EXE")


def test_get_node_content(vfs):
    node = vfs.get_node("C:\\README.TXT")
    assert node is not None
    assert not node.is_dir
    assert "WELCOME TO PHANTASM-OS" in node.content
    assert node.file_type == FileType.TEXT


def test_get_nonexistent_node(vfs):
    node = vfs.get_node("C:\\DOES_NOT_EXIST.TXT")
    assert node is None


def test_list_directory_folders_first(vfs):
    nodes = vfs.list_dir("C:\\")
    assert len(nodes) > 0
    # Directory nodes must precede file nodes
    found_file = False
    for n in nodes:
        if not n.is_dir:
            found_file = True
        elif found_file:
            pytest.fail("Found directory after file in sorted list.")


def test_write_and_read_file(vfs):
    path = "C:\\MYDOCS\\NOTES.TXT"
    content = "Testing 1995 dial-up speed and retro cyber aesthetics."
    created = vfs.write_file(path, content)
    assert created.name == "NOTES.TXT"
    assert created.size == len(content.encode("utf-8"))

    read_back = vfs.get_node(path)
    assert read_back is not None
    assert read_back.content == content


def test_create_directory(vfs):
    new_dir = vfs.create_dir("C:\\GAMES\\DOOM")
    assert new_dir.is_dir
    assert vfs.exists("C:\\GAMES")
    assert vfs.exists("C:\\GAMES\\DOOM")


def test_delete_file(vfs):
    path = "C:\\TEMP_FILE.TXT"
    vfs.write_file(path, "temporary")
    assert vfs.exists(path)

    deleted = vfs.delete_node(path)
    assert deleted is True
    assert not vfs.exists(path)


def test_delete_root_rejected(vfs):
    deleted = vfs.delete_node("C:\\")
    assert deleted is False


def test_glitch_file(vfs):
    path = "C:\\TEST_GLITCH.TXT"
    original = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    vfs.write_file(path, original)

    glitched = vfs.glitch_file(path, intensity=0.5)
    assert glitched.corrupted is True
    assert glitched.file_type == FileType.CORRUPT
    assert glitched.content != original


def test_hallucinate_file(vfs):
    path = "C:\\MYDOCS\\SECRET_TRANSMISSION.TXT"
    node = vfs.hallucinate_file(path, theme="conspiracy")
    assert node is not None
    assert node.content is not None
    assert "[THEME: CONSPIRACY]" in node.content


def test_search_nodes(vfs):
    results = vfs.search("autoexec")
    assert len(results) >= 1
    assert any("AUTOEXEC.BAT" in r.name for r in results)

    content_results = vfs.search("Sound Blaster")
    assert len(content_results) >= 1
    assert any("KERNEL_BOOT.LOG" in r.name for r in content_results)


def test_serialization_persistence(vfs):
    vfs.write_file("C:\\CUSTOM.TXT", "Saved in persistent snapshot")
    data = vfs.to_dict()

    new_vfs = VirtualFileSystem(seed_defaults=False)
    new_vfs.from_dict(data)

    assert new_vfs.exists("C:\\CUSTOM.TXT")
    assert new_vfs.get_node("C:\\CUSTOM.TXT").content == "Saved in persistent snapshot"
