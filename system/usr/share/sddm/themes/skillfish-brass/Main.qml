import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: root
    width: 1920; height: 1080
    color: "#160f06"

    property color brass: "#d8a849"
    property color brassHi: "#f6e2a0"
    property color copper: "#b9722f"
    property color cream: "#f1e3c6"
    property color dark: "#0d0903"
    property color surf: "#20180b"

    // background image (brass wallpaper) with dark overlay
    Image {
        id: bg
        anchors.fill: parent
        source: "background.png"
        fillMode: Image.PreserveAspectCrop
        asynchronous: true
        clip: true
    }
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#cc160f06" }
            GradientStop { position: 1.0; color: "#e6080502" }
        }
    }

    // SkillFishOS mechanical fish (cut-out, transparent bg), above the clock
    Image {
        id: fish
        source: "fish.png"
        fillMode: Image.PreserveAspectFit
        height: root.height * 0.26
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: root.height * 0.06
        smooth: true
    }

    // clock (below the fish)
    Text {
        id: clock
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: fish.bottom
        anchors.topMargin: 6
        color: brassHi
        font.pixelSize: 56
        font.bold: true
        function upd() { text = Qt.formatTime(new Date(), "HH:mm") }
        Component.onCompleted: upd()
    }
    Timer { interval: 1000; running: true; repeat: true; onTriggered: clock.upd() }

    // login panel
    Rectangle {
        id: panel
        width: 460; height: 280
        radius: 18
        anchors.centerIn: parent
        anchors.verticalCenterOffset: root.height * 0.12
        color: "#e620180b"
        border.color: brass
        border.width: 2

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 28
            spacing: 16

            Text {
                text: "SkillFishOS"
                color: cream
                font.pixelSize: 22; font.bold: true
                Layout.alignment: Qt.AlignHCenter
            }

            // user
            ComboBox {
                id: userBox
                Layout.fillWidth: true
                model: userModel
                textRole: "name"
                height: 44
                Component.onCompleted: currentIndex = userModel.lastIndex
            }

            // password
            TextField {
                id: pw
                Layout.fillWidth: true
                echoMode: TextInput.Password
                placeholderText: "Password"
                focus: true
                color: cream
                background: Rectangle {
                    color: "#0d0903"; radius: 8
                    border.color: brass; border.width: 1
                }
                onAccepted: sddm.login(userBox.currentText, pw.text, sessionBox.currentIndex)
            }

            // login button
            Button {
                Layout.fillWidth: true
                height: 46
                text: "Accedi"
                contentItem: Text {
                    text: parent.text; color: dark
                    font.bold: true; font.pixelSize: 16
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    radius: 8
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: brassHi }
                        GradientStop { position: 1.0; color: brass }
                    }
                }
                onClicked: sddm.login(userBox.currentText, pw.text, sessionBox.currentIndex)
            }
        }
    }

    // session selector (bottom-left) + power (bottom-right)
    ComboBox {
        id: sessionBox
        width: 240
        anchors.left: parent.left; anchors.bottom: parent.bottom
        anchors.margins: 24
        model: sessionModel
        textRole: "name"
        Component.onCompleted: currentIndex = sessionModel.lastIndex
    }

    Row {
        anchors.right: parent.right; anchors.bottom: parent.bottom
        anchors.margins: 24
        spacing: 16
        Button {
            text: "⏻"
            onClicked: sddm.powerOff()
            contentItem: Text { text: parent.text; color: copper; font.pixelSize: 24 }
            background: Rectangle { color: "transparent" }
        }
        Button {
            text: "⟳"
            onClicked: sddm.reboot()
            contentItem: Text { text: parent.text; color: brass; font.pixelSize: 24 }
            background: Rectangle { color: "transparent" }
        }
    }

    Connections {
        target: sddm
        function onLoginFailed() {
            pw.text = ""
            pw.placeholderText = "Password errata, riprova"
        }
    }
}
