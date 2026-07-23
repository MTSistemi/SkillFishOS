#!/bin/sh
# Make the SkillFishOS os-release survive base-files upgrades via dpkg-divert.
set -e
# divert base-files' /usr/lib/os-release so apt can never overwrite our branding
if ! dpkg-divert --list /usr/lib/os-release | grep -q os-release; then
  dpkg-divert --divert /usr/lib/os-release.debian --rename --add /usr/lib/os-release
fi
cat > /usr/lib/os-release <<'EOF'
PRETTY_NAME="SkillFishOS 26.06 (Aetherium)"
NAME="SkillFishOS"
VERSION="26.06 (Aetherium)"
VERSION_ID="26.06"
VERSION_CODENAME=aetherium
ID=skillfishos
ID_LIKE=debian
HOME_URL="https://skillfishos.com"
SUPPORT_URL="https://github.com/MTSistemi/SkillFishOS"
BUG_REPORT_URL="https://github.com/MTSistemi/SkillFishOS/issues"
PRIVACY_POLICY_URL="https://skillfishos.com"
LOGO=skillfishos
ANSI_COLOR="0;33"
EOF
# canonical symlink (standard Debian layout)
ln -sf ../usr/lib/os-release /etc/os-release
echo "=== result ==="
cat /etc/os-release | grep -E '^NAME|^PRETTY|^LOGO|^HOME'
echo "--- divert ---"; dpkg-divert --list /usr/lib/os-release
