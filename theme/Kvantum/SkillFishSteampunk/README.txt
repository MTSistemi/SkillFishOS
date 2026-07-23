SkillFish Steampunk — tema Kvantum (app Qt/KDE)
===============================================
Base: KvDarkRed di Tsu Jan (Kvantum), ricolorata in ottone/rame.

INSTALL:
  mkdir -p ~/.config/Kvantum
  cp -r SkillFishSteampunk ~/.config/Kvantum/
  kvantummanager --set SkillFishSteampunk      # oppure scegli il tema in Kvantum Manager

FAR USARE KVANTUM ALLE APP QT (importante su Wayland/Wayfire):
  - installa il motore: pacchetto "kvantum" (es. kvantum-qt5 / kvantum-qt6)
  - imposta la variabile (in ~/.config/wayfire.ini [env] o nel profilo di sessione):
        QT_QPA_PLATFORMTHEME=kvantum
    in alternativa usa qt5ct/qt6ct e lì seleziona lo stile "kvantum".

Richiede Kvantum installato. Tutti gli id dei widget sono originali: solo i colori
sono stati cambiati, quindi resta pienamente compatibile.
