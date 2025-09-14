import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: node

    property string nodeId: ""
    property var keys: []
    property bool isLeaf: true
    property bool selected: false
    property real animationScale: 1.0

    signal clicked()
    signal doubleClicked()

    width: Math.max(120, keys.length * 40 + 32)
    height: 56

    color: selected ? "#1e3a8a" : "#18181b"
    border.color: selected ? "#3b82f6" : "#27272a"
    border.width: 2
    radius: 12

    // Modern gradient background
    Rectangle {
        anchors.fill: parent
        radius: parent.radius
        gradient: Gradient {
            GradientStop { position: 0.0; color: selected ? "#1e40af" : "#1f1f23" }
            GradientStop { position: 1.0; color: selected ? "#1e3a8a" : "#18181b" }
        }
    }

    // Subtle glow effect
    Rectangle {
        anchors.fill: parent
        anchors.margins: -2
        color: "transparent"
        border.color: selected ? "#3b82f680" : "#27272a40"
        border.width: 1
        radius: parent.radius + 2
        z: -1
        opacity: nodeMouseArea.containsMouse ? 0.8 : 0.3
        
        Behavior on opacity {
            PropertyAnimation { duration: 200 }
        }
    }

    // Keys display container
    Rectangle {
        anchors.fill: parent
        anchors.margins: 8
        color: "transparent"
        radius: 8

        Row {
            anchors.centerIn: parent
            spacing: 4

            Repeater {
                model: node.keys

                Rectangle {
                    width: 32
                    height: 32
                    color: "#27272a"
                    border.color: "#3f3f46"
                    border.width: 1
                    radius: 6

                    Text {
                        anchors.centerIn: parent
                        text: modelData
                        font.pixelSize: 13
                        font.weight: Font.Medium
                        color: "#ffffff"
                    }

                    // Modern key separator
                    Rectangle {
                        anchors.right: parent.right
                        anchors.rightMargin: -2
                        anchors.verticalCenter: parent.verticalCenter
                        width: 2
                        height: parent.height * 0.4
                        color: "#52525b"
                        radius: 1
                        visible: index < node.keys.length - 1
                    }
                }
            }
        }
    }

    // Modern node type indicator
    Rectangle {
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 6
        width: 10
        height: 10
        radius: 5
        color: isLeaf ? "#10b981" : "#f59e0b"
        border.color: isLeaf ? "#065f46" : "#92400e"
        border.width: 1

        ToolTip.visible: nodeMouseArea.containsMouse
        ToolTip.text: isLeaf ? "Leaf Node" : "Internal Node"
    }

    // Interactive mouse area
    MouseArea {
        id: nodeMouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onClicked: node.clicked()
        onDoubleClicked: node.doubleClicked()

        onEntered: {
            node.scale = 1.05
        }

        onExited: {
            node.scale = 1.0
        }
    }

    // Enhanced highlight animation
    function highlight() {
        highlightAnimation.start()
    }

    SequentialAnimation {
        id: highlightAnimation

        ParallelAnimation {
            PropertyAnimation {
                target: node
                property: "scale"
                to: 1.2
                duration: 200
                easing.type: Easing.OutBack
            }

            ColorAnimation {
                target: node
                property: "border.color"
                to: "#ef4444"
                duration: 200
            }
        }

        PauseAnimation { duration: 100 }

        ParallelAnimation {
            PropertyAnimation {
                target: node
                property: "scale"
                to: 1.0
                duration: 250
                easing.type: Easing.OutCubic
            }

            ColorAnimation {
                target: node
                property: "border.color"
                to: selected ? "#3b82f6" : "#27272a"
                duration: 250
            }
        }
    }

    // Smooth behaviors
    Behavior on scale {
        PropertyAnimation {
            duration: 200
            easing.type: Easing.OutCubic
        }
    }

    Behavior on color {
        ColorAnimation { duration: 300 }
    }

    Behavior on border.color {
        ColorAnimation { duration: 300 }
    }
}
