import pytest
from pathlib import Path

from conjector import properties


@pytest.fixture
def path_class_fixt(request):
    @properties(filename=request.param, root="path")
    class PathClass:
        str_file_path_var: Path
        str_dir_path_var: Path
        missing_path_var: Path

    return PathClass


@pytest.mark.parametrize(
    "path_class_fixt",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
    indirect=True,
)
def test_path_field_ok(path_class_fixt):
    assert path_class_fixt.str_file_path_var == Path("some/path/file.txt")
    assert path_class_fixt.str_dir_path_var == Path("some/file/")
    assert path_class_fixt.missing_path_var == Path()


@pytest.mark.parametrize(
    "filename",
    ("types_cast.yml", "types_cast.json", "types_cast.toml", "types_cast.ini"),
)
def test_invalid_path_field(filename):
    with pytest.raises(ValueError):

        @properties(filename=filename, root="path")
        class InvalidPathClass:
            invalid_path_var: Path
