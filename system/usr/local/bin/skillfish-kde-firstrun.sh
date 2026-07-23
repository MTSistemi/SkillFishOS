#!/bin/bash
sleep 5
plasma-apply-wallpaperimage /usr/share/skillfish/wallpaper_brass.png
plasma-apply-cursortheme SkillFish-Steampunk-Cursors 2>/dev/null
rm -f "$HOME/.config/autostart/skillfish-kde-firstrun.desktop"
