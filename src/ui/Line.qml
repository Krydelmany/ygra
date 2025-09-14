import QtQuick 2.15
import QtQuick.Shapes 1.15

Shape {
    id: line

    property real x1: 0
    property real y1: 0
    property real x2: 0
    property real y2: 0
    property color lineColor: "#52525b"
    property real lineWidth: 2.5

    width: Math.abs(x2 - x1) + lineWidth * 2
    height: Math.abs(y2 - y1) + lineWidth * 2
    x: Math.min(x1, x2) - lineWidth
    y: Math.min(y1, y2) - lineWidth

    ShapePath {
        strokeColor: line.lineColor
        strokeWidth: line.lineWidth
        fillColor: "transparent"
        capStyle: ShapePath.RoundCap
        joinStyle: ShapePath.RoundJoin

        startX: line.x1 - line.x
        startY: line.y1 - line.y

        PathLine {
            x: line.x2 - line.x
            y: line.y2 - line.y
        }
    }

    // Smooth animations
    Behavior on x1 {
        PropertyAnimation {
            duration: 600
            easing.type: Easing.OutCubic
        }
    }

    Behavior on y1 {
        PropertyAnimation {
            duration: 600
            easing.type: Easing.OutCubic
        }
    }

    Behavior on x2 {
        PropertyAnimation {
            duration: 600
            easing.type: Easing.OutCubic
        }
    }

    Behavior on y2 {
        PropertyAnimation {
            duration: 600
            easing.type: Easing.OutCubic
        }
    }

    Behavior on lineColor {
        ColorAnimation { duration: 400 }
    }
}
