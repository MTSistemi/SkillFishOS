# SkillFishOS Control Center - one window for every SkillFishOS tool.
#
# The package lives in /usr/share/skillfish/control-center/sfcc and is started
# by /usr/local/bin/skillfish-control-center. Pages are modules under pagine/;
# each one is built the first time it is shown, so opening the window costs the
# same whatever the number of sections.
#
# ⚠️ The version was written here by hand, and 26.09.3 shipped with a window
# still saying 26.09.1: a number kept in two places is a number that will
# disagree. It is asked to dpkg now, which is the only one that knows what is
# installed; the string below is the fallback for a tree run from git.
import subprocess

RIPIEGO = "26.09.3"


def _installata():
    try:
        r = subprocess.run(["dpkg-query", "-W", "-f=${Version}", "skillfish-control-center"],
                           capture_output=True, text=True, timeout=10)
        v = (r.stdout or "").strip()
        return v if r.returncode == 0 and v else RIPIEGO
    except Exception:
        return RIPIEGO


VERSIONE = _installata()
