#!/bin/bash
# install-unsloth.sh — Unsloth Studio as the SkillFishOS on-device AI engine.
#
# Kept for the callers that still know this path (older panels, the docs). The
# work is done by skillfish-unsloth-update, which installs in the HOME OF THE
# USER (an image never ships /root), forces the Vulkan bundle of llama.cpp (the
# only GPU path on gfx1013), removes the desktop icon the installer drops and
# restarts the service so the new version really runs.
set -u
if [ -x /usr/local/bin/skillfish-unsloth-update ]; then
    exec /usr/local/bin/skillfish-unsloth-update "$@"
fi
echo "install-unsloth.sh: skillfish-unsloth-update is missing; install skillfish-ai-panel first." >&2
exit 1
