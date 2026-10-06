import pytest
from fendimo import cli
import contextlib
import io
import sys
'''
tmp_path is a pytest fixture'''  
def test_make(tmp_path):
    '''create a stringio object instead of a real file'''
    output = io.StringIO()
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["fendimo", "make"])
        with contextlib.redirect_stdout(output):
            cli.main()

    fendimo_dir = tmp_path / ".fend"
    objects_dir = fendimo_dir / "objects"
    assert fendimo_dir.is_dir()
    assert objects_dir.is_dir()
    assert list(objects_dir.iterdir()) == []
    assert output.getvalue() == f"Initialized a fendimo directory at {tmp_path}/.fend\n"

def test_codesave(tmp_path):
    output=io.StringIO()
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["fendimo", "codesave", "sample_codes_to_fend/hello_world.py"])
        with contextlib.redirect_stdout(output):
            cli.main()
    
    

def test_show(tmp_path):
    output=io.StringIO()
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["fendimo", "show", "sample_codes_to_fend/hello_world.py"])
        with contextlib.redirect_stdout(output):
            cli.main()

def test_conifer(tmp_path):
    output=io.StringIO()
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr(sys, "argv", ["fendimo", "conifer", "sample_codes_to_fend/hello_world.py"])
        with contextlib.redirect_stdout(output):
            cli.main()
