"""Control Center, Games page: which folder a GE-Proton release is installed in.

From GE-Proton11-12 the tarball unpacks into GE-Proton11-12-x86_64, not
GE-Proton11-12. The page compared names only, showed the release as not
installed and downloaded it again. giochi.py needs PyQt and the Control
Center package to import, so only cartella_di() is taken out of it.
"""
import ast
import pathlib

GIOCHI = (pathlib.Path(__file__).resolve().parents[1]
          / "apps" / "control-center" / "sfcc" / "pagine" / "giochi.py")


def _cartella_di():
    tree = ast.parse(GIOCHI.read_text(encoding="utf-8"))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "cartella_di")
    ns = {}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(GIOCHI), "exec"), ns)
    return ns["cartella_di"]


def test_old_releases_unpack_into_their_own_name():
    f = _cartella_di()
    assert f("GE-Proton11-6", ["GE-Proton10-34", "GE-Proton11-6"]) == "GE-Proton11-6"


def test_new_releases_unpack_into_name_x86_64():
    f = _cartella_di()
    assert f("GE-Proton11-12", ["GE-Proton11-12-x86_64", "GE-Proton11-6"]) == "GE-Proton11-12-x86_64"


def test_not_installed_is_none():
    f = _cartella_di()
    assert f("GE-Proton11-12", ["GE-Proton11-6"]) is None


def test_a_prefix_of_another_release_does_not_match():
    f = _cartella_di()
    assert f("GE-Proton11-1", ["GE-Proton11-12-x86_64", "GE-Proton11-12"]) is None
