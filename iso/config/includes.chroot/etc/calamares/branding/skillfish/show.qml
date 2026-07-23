import QtQuick 2.0
import calamares.slideshow 1.0
Presentation {
    id: presentation
    Timer { interval: 6000; running: true; repeat: true; onTriggered: presentation.goToNextSlide() }
    Slide { Rectangle { anchors.fill: parent; color: "#101418" }
        Text { anchors.centerIn: parent; color: "#1fb6ff"; font.pixelSize: 42; text: "SkillFishOS" } }
    Slide { Rectangle { anchors.fill: parent; color: "#101418" }
        Text { anchors.centerIn: parent; color: "white"; font.pixelSize: 22; text: "Kernel 7.0.10-tkg - Mesa - Hyprland - btrfs snapshots" } }
}
