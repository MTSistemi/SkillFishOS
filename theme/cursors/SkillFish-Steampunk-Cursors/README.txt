SkillFish Steampunk — cursor (Xcursor) theme
============================================
25 cursor shapes + full alias set (X11 + freedesktop names), sizes 24/32/48/64.
'wait' and 'left_ptr_watch/progress' are ANIMATED (spinning brass gear).

INSTALL (user-local):
  unzip SkillFish-Steampunk-Cursors.zip -d ~/.local/share/icons/

SET IT:
  GTK / GNOME:
    gsettings set org.gnome.desktop.interface cursor-theme 'SkillFish Steampunk'
    gsettings set org.gnome.desktop.interface cursor-size 32
  nwg-look / lxappearance also work and are handy on Wayfire.

WAYFIRE (wlroots) — make it apply everywhere, add to ~/.config/wayfire.ini:
    [input]
    cursor_theme = SkillFish Steampunk
    cursor_size = 32
  or export before launching the session:
    export XCURSOR_THEME="SkillFish Steampunk"
    export XCURSOR_SIZE=32

Inherits Adwaita, so any shape not provided falls back cleanly.
