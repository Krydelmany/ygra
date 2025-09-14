import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ColumnLayout {
    id: metricsPanel
    spacing: 16
    Layout.preferredHeight: 260

    property int treeHeight: 0
    property int totalNodes: 0
    property int totalKeys: 0

    function updateMetrics(metrics) {
        treeHeight = metrics.height || 0
        totalNodes = metrics.totalNodes || 0
        totalKeys = metrics.totalKeys || 0
    }

    // Metrics Header
    Text {
        text: "Métricas da Árvore"
        font.pixelSize: 14
        font.weight: Font.Medium
        color: "#f4f4f5"
    }

    // Metrics Container
    Rectangle {
        Layout.fillWidth: true
        Layout.preferredHeight: 220
        color: "#18181b"
        border.color: "#27272a"
        border.width: 1
        radius: 8
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 16
            anchors.bottomMargin: 24
            spacing: 14

            // Height Metric
            Row {
                Layout.fillWidth: true
                Layout.preferredHeight: 24
                spacing: 8

                Rectangle {
                    width: 8
                    height: 8
                    color: "#3b82f6"
                    radius: 4
                    anchors.verticalCenter: parent.verticalCenter
                }

                Text {
                    text: "Altura:"
                    font.pixelSize: 12
                    color: "#a1a1aa"
                    anchors.verticalCenter: parent.verticalCenter
                }

                Item { Layout.fillWidth: true }

                Text {
                    text: metricsPanel.treeHeight.toString()
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: "#ffffff"
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            // Nodes Metric
            Row {
                Layout.fillWidth: true
                Layout.preferredHeight: 24
                spacing: 8

                Rectangle {
                    width: 8
                    height: 8
                    color: "#10b981"
                    radius: 4
                    anchors.verticalCenter: parent.verticalCenter
                }

                Text {
                    text: "Nós:"
                    font.pixelSize: 12
                    color: "#a1a1aa"
                    anchors.verticalCenter: parent.verticalCenter
                }

                Item { Layout.fillWidth: true }

                Text {
                    text: metricsPanel.totalNodes.toString()
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: "#ffffff"
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            // Keys Metric
            Row {
                Layout.fillWidth: true
                Layout.preferredHeight: 24
                spacing: 8

                Rectangle {
                    width: 8
                    height: 8
                    color: "#f59e0b"
                    radius: 4
                    anchors.verticalCenter: parent.verticalCenter
                }

                Text {
                    text: "Chaves:"
                    font.pixelSize: 12
                    color: "#a1a1aa"
                    anchors.verticalCenter: parent.verticalCenter
                }

                Item { Layout.fillWidth: true }

                Text {
                    text: metricsPanel.totalKeys.toString()
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: "#ffffff"
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            // Tree Config Info
            Rectangle {
                Layout.fillWidth: true
                height: 1
                color: "#27272a"
                Layout.topMargin: 8
                Layout.bottomMargin: 6
            }

            Column {
                Layout.fillWidth: true
                spacing: 6
                Layout.bottomMargin: 4

                Text {
                    text: "B-Tree (grau " + (bridge ? bridge.degree : 2) + ")"
                    font.pixelSize: 11
                    color: "#71717a"
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Text {
                    text: "Máx. chaves por nó: " + (bridge ? (bridge.degree - 1) : 1)
                    font.pixelSize: 10
                    color: "#52525b"
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }
        }
    }
}
