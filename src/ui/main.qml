import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import BTreeApp 1.0

ApplicationWindow {
    id: window
    visible: true
    width: 1600
    height: 1000
    title: "B-Tree Visualizer"
    color: "#0a0a0a"

    property real animationSpeed: 500
    property string currentMessage: ""
    property string messageKind: "info"

    Bridge {
        id: bridge

        onTreeChanged: function(nodes, edges) {
            canvas.updateTree(nodes, edges)
        }

        onMetricsChanged: function(metrics) {
            metricsPanel.updateMetrics(metrics)
        }

        onEventsReady: function(events) {
            canvas.playAnimation(events)
        }

        onMessage: function(text, kind) {
            window.currentMessage = text
            window.messageKind = kind
            messageTimer.restart()
        }
    }

    Timer {
        id: messageTimer
        interval: 3000
        onTriggered: window.currentMessage = ""
    }

    // Modern layout with sidebar
    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Left Sidebar - Controls
        Rectangle {
            id: sidebar
            Layout.preferredWidth: 350
            Layout.fillHeight: true
            color: "#0a0a0a"
            border.color: "#262626"
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 24
                spacing: 32

                // Header
                Column {
                    Layout.fillWidth: true
                    spacing: 8

                    Text {
                        text: "Arvore Multipla"
                        font.pixelSize: 24
                        font.weight: Font.Bold
                        color: "#ffffff"
                    }
                    
                    Text {
                        text: "Explorador Interativo de Árvore Binária"
                        font.pixelSize: 14
                        color: "#71717a"
                    }
                }

                // Controls Section
                Column {
                    Layout.fillWidth: true
                    spacing: 20

                    // Degree Input - Simplified
                    Rectangle {
                        width: parent.width
                        height: 90
                        color: "#18181b"
                        border.color: "#27272a"
                        border.width: 1
                        radius: 8

                        Column {
                            anchors.fill: parent
                            anchors.margins: 16
                            anchors.bottomMargin: 20
                            spacing: 8

                            Text {
                                text: "Grau da Árvore"
                                font.pixelSize: 14
                                font.weight: Font.Medium
                                color: "#f4f4f5"
                            }

                            Row {
                                width: parent.width
                                spacing: 8

                                Rectangle {
                                    width: parent.width - 80
                                    height: 36
                                    color: "#27272a"
                                    border.color: "#3f3f46"
                                    border.width: 1
                                    radius: 6

                                    TextInput {
                                        id: degreeInput
                                        anchors.fill: parent
                                        anchors.margins: 8
                                        text: bridge.degree.toString()
                                        font.pixelSize: 14
                                        color: "#ffffff"
                                        selectByMouse: true
                                        validator: IntValidator { bottom: 2; top: 20 }
                                        verticalAlignment: TextInput.AlignVCenter
                                        
                                        Keys.onReturnPressed: confirmDegree()
                                    }
                                }

                                Rectangle {
                                    width: 72
                                    height: 36
                                    color: "#1e40af"
                                    border.color: "#1e40af"
                                    border.width: 1
                                    radius: 6
                                    
                                    Text {
                                        anchors.centerIn: parent
                                        text: "OK"
                                        font.pixelSize: 12
                                        font.weight: Font.Medium
                                        color: "#ffffff"
                                    }
                                    
                                    MouseArea {
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        cursorShape: Qt.PointingHandCursor
                                        
                                        onEntered: {
                                            parent.color = "#2563eb"
                                            parent.border.color = "#3b82f6"
                                        }
                                        onExited: {
                                            parent.color = "#1e40af"
                                            parent.border.color = "#1e40af"
                                        }
                                        onPressed: {
                                            parent.color = "#1d4ed8"
                                        }
                                        onReleased: {
                                            parent.color = containsMouse ? "#2563eb" : "#1e40af"
                                            parent.border.color = containsMouse ? "#3b82f6" : "#1e40af"
                                        }
                                        onClicked: confirmDegree()
                                    }
                                }
                            }
                        }
                    }

                    // Insert/Remove/Search Section - Consolidated
                    Rectangle {
                        width: parent.width
                        height: 260
                        color: "#18181b"
                        border.color: "#27272a"
                        border.width: 1
                        radius: 8

                        Column {
                            anchors.fill: parent
                            anchors.margins: 16
                            anchors.bottomMargin: 28
                            spacing: 16

                            // Insert Section
                            Column {
                                width: parent.width
                                spacing: 8

                                Text {
                                    text: "Inserir Chaves"
                                    font.pixelSize: 14
                                    font.weight: Font.Medium
                                    color: "#f4f4f5"
                                }

                                Row {
                                    width: parent.width
                                    spacing: 8

                                    Rectangle {
                                        width: parent.width - 80
                                        height: 36
                                        color: "#27272a"
                                        border.color: "#3f3f46"
                                        border.width: 1
                                        radius: 6

                                        TextInput {
                                            id: insertInput
                                            anchors.fill: parent
                                            anchors.margins: 8
                                            font.pixelSize: 14
                                            color: "#ffffff"
                                            selectByMouse: true
                                            verticalAlignment: TextInput.AlignVCenter
                                            
                                            property string placeholderText: "1,2,3 ou número único"
                                            
                                            Text {
                                                anchors.fill: parent
                                                text: parent.placeholderText
                                                font: parent.font
                                                color: "#71717a"
                                                verticalAlignment: Text.AlignVCenter
                                                visible: !parent.activeFocus && parent.text.length === 0
                                            }
                                            
                                            Keys.onReturnPressed: insertKeys()
                                        }
                                    }

                                    Rectangle {
                                        width: 72
                                        height: 36
                                        color: "#059669"
                                        border.color: "#059669"
                                        border.width: 1
                                        radius: 6
                                        
                                        Text {
                                            anchors.centerIn: parent
                                            text: "+"
                                            font.pixelSize: 16
                                            font.weight: Font.Medium
                                            color: "#ffffff"
                                        }
                                        
                                        MouseArea {
                                            anchors.fill: parent
                                            hoverEnabled: true
                                            cursorShape: Qt.PointingHandCursor
                                            
                                            onEntered: {
                                                parent.color = "#047857"
                                                parent.border.color = "#10b981"
                                            }
                                            onExited: {
                                                parent.color = "#059669"
                                                parent.border.color = "#059669"
                                            }
                                            onPressed: {
                                                parent.color = "#065f46"
                                            }
                                            onReleased: {
                                                parent.color = containsMouse ? "#047857" : "#059669"
                                                parent.border.color = containsMouse ? "#10b981" : "#059669"
                                            }
                                            onClicked: insertKeys()
                                        }
                                    }
                                }
                            }

                            // Remove Section
                            Column {
                                width: parent.width
                                spacing: 8

                                Text {
                                    text: "Remover Chaves"
                                    font.pixelSize: 14
                                    font.weight: Font.Medium
                                    color: "#f4f4f5"
                                }

                                Row {
                                    width: parent.width
                                    spacing: 8

                                    Rectangle {
                                        width: parent.width - 80
                                        height: 36
                                        color: "#27272a"
                                        border.color: "#3f3f46"
                                        border.width: 1
                                        radius: 6

                                        TextInput {
                                            id: removeInput
                                            anchors.fill: parent
                                            anchors.margins: 8
                                            font.pixelSize: 14
                                            color: "#ffffff"
                                            selectByMouse: true
                                            verticalAlignment: TextInput.AlignVCenter
                                            
                                            property string placeholderText: "1,2,3 ou número único"
                                            
                                            Text {
                                                anchors.fill: parent
                                                text: parent.placeholderText
                                                font: parent.font
                                                color: "#71717a"
                                                verticalAlignment: Text.AlignVCenter
                                                visible: !parent.activeFocus && parent.text.length === 0
                                            }
                                            
                                            Keys.onReturnPressed: removeKeys()
                                        }
                                    }

                                    Rectangle {
                                        width: 72
                                        height: 36
                                        color: "#dc2626"
                                        border.color: "#dc2626"
                                        border.width: 1
                                        radius: 6
                                        
                                        Text {
                                            anchors.centerIn: parent
                                            text: "−"
                                            font.pixelSize: 16
                                            font.weight: Font.Medium
                                            color: "#ffffff"
                                        }
                                        
                                        MouseArea {
                                            anchors.fill: parent
                                            hoverEnabled: true
                                            cursorShape: Qt.PointingHandCursor
                                            
                                            onEntered: {
                                                parent.color = "#991b1b"
                                                parent.border.color = "#ef4444"
                                            }
                                            onExited: {
                                                parent.color = "#dc2626"
                                                parent.border.color = "#dc2626"
                                            }
                                            onPressed: {
                                                parent.color = "#7f1d1d"
                                            }
                                            onReleased: {
                                                parent.color = containsMouse ? "#991b1b" : "#dc2626"
                                                parent.border.color = containsMouse ? "#ef4444" : "#dc2626"
                                            }
                                            onClicked: removeKeys()
                                        }
                                    }
                                }
                            }

                            // Search Section
                            Column {
                                width: parent.width
                                spacing: 8

                                Text {
                                    text: "Buscar Chave"
                                    font.pixelSize: 14
                                    font.weight: Font.Medium
                                    color: "#f4f4f5"
                                }

                                Row {
                                    width: parent.width
                                    spacing: 8

                                    Rectangle {
                                        width: parent.width - 80
                                        height: 36
                                        color: "#27272a"
                                        border.color: "#3f3f46"
                                        border.width: 1
                                        radius: 6

                                        TextInput {
                                            id: searchInput
                                            anchors.fill: parent
                                            anchors.margins: 8
                                            font.pixelSize: 14
                                            color: "#ffffff"
                                            selectByMouse: true
                                            validator: IntValidator {}
                                            verticalAlignment: TextInput.AlignVCenter
                                            
                                            property string placeholderText: "Digite um número"
                                            
                                            Text {
                                                anchors.fill: parent
                                                text: parent.placeholderText
                                                font: parent.font
                                                color: "#71717a"
                                                verticalAlignment: Text.AlignVCenter
                                                visible: !parent.activeFocus && parent.text.length === 0
                                            }
                                            
                                            Keys.onReturnPressed: searchKey()
                                        }
                                    }

                                    Rectangle {
                                        width: 72
                                        height: 36
                                        color: "#0ea5e9"
                                        border.color: "#0ea5e9"
                                        border.width: 1
                                        radius: 6
                                        
                                        Text {
                                            anchors.centerIn: parent
                                            text: "Buscar"
                                            font.pixelSize: 14
                                            color: "#ffffff"
                                        }
                                        
                                        MouseArea {
                                            anchors.fill: parent
                                            hoverEnabled: true
                                            cursorShape: Qt.PointingHandCursor
                                            
                                            onEntered: {
                                                parent.color = "#0284c7"
                                                parent.border.color = "#38bdf8"
                                            }
                                            onExited: {
                                                parent.color = "#0ea5e9"
                                                parent.border.color = "#0ea5e9"
                                            }
                                            onPressed: {
                                                parent.color = "#0c4a6e"
                                            }
                                            onReleased: {
                                                parent.color = containsMouse ? "#0284c7" : "#0ea5e9"
                                                parent.border.color = containsMouse ? "#38bdf8" : "#0ea5e9"
                                            }
                                            onClicked: searchKey()
                                        }
                                    }
                                }
                            }
                        }
                    }

                    // Actions - Horizontal Row
                    Row {
                        width: parent.width
                        spacing: 8

                        Rectangle {
                            width: (parent.width - 8) / 2
                            height: 44
                            color: "#dc2626"
                            border.color: "#dc2626"
                            border.width: 1
                            radius: 8
                            
                            Text {
                                anchors.centerIn: parent
                                text: "Limpar"
                                font.pixelSize: 14
                                font.weight: Font.Medium
                                color: "#ffffff"
                            }
                            
                            MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                
                                onEntered: {
                                    parent.color = "#991b1b"
                                    parent.border.color = "#ef4444"
                                }
                                onExited: {
                                    parent.color = "#dc2626"
                                    parent.border.color = "#dc2626"
                                }
                                onPressed: {
                                    parent.color = "#7f1d1d"
                                }
                                onReleased: {
                                    parent.color = containsMouse ? "#991b1b" : "#dc2626"
                                    parent.border.color = containsMouse ? "#ef4444" : "#dc2626"
                                }
                                onClicked: bridge.clearAll()
                            }
                        }

                        Rectangle {
                            width: (parent.width - 8) / 2
                            height: 44
                            color: "#2563eb"
                            border.color: "#2563eb"
                            border.width: 1
                            radius: 8
                            
                            Text {
                                anchors.centerIn: parent
                                text: "Exemplo"
                                font.pixelSize: 14
                                font.weight: Font.Medium
                                color: "#ffffff"
                            }
                            
                            MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                
                                onEntered: {
                                    parent.color = "#1d4ed8"
                                    parent.border.color = "#3b82f6"
                                }
                                onExited: {
                                    parent.color = "#2563eb"
                                    parent.border.color = "#2563eb"
                                }
                                onPressed: {
                                    parent.color = "#1e3a8a"
                                }
                                onReleased: {
                                    parent.color = containsMouse ? "#1d4ed8" : "#2563eb"
                                    parent.border.color = containsMouse ? "#3b82f6" : "#2563eb"
                                }
                                onClicked: bridge.loadExample()
                            }
                        }
                    }
                }

                // Metrics Panel
                MetricsPanel {
                    id: metricsPanel
                    Layout.fillWidth: true
                }

                // Spacer
                Item {
                    Layout.fillHeight: true
                }

                // Status Message
                Rectangle {
                    Layout.fillWidth: true
                    height: messageText.contentHeight + 16
                    color: window.messageKind === "error" ? "#7f1d1d" : 
                           window.messageKind === "success" ? "#14532d" : "#1e3a8a"
                    border.color: window.messageKind === "error" ? "#dc2626" : 
                                  window.messageKind === "success" ? "#16a34a" : "#3b82f6"
                    border.width: 1
                    radius: 8
                    visible: window.currentMessage !== ""
                    
                    Text {
                        id: messageText
                        anchors.centerIn: parent
                        text: window.currentMessage
                        font.pixelSize: 12
                        color: "#ffffff"
                        wrapMode: Text.WordWrap
                        width: parent.width - 16
                        horizontalAlignment: Text.AlignHCenter
                    }
                }
            }
        }

        // Main Canvas Area
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#0a0a0a"

            TreeCanvas {
                id: canvas
                anchors.fill: parent
                anchors.margins: 20

                onNodeClicked: function(nodeId) {
                    console.log("Node clicked:", nodeId)
                }

                onNodeDoubleClicked: function(nodeId) {
                    console.log("Node double-clicked:", nodeId)
                }
            }
        }
    }

    // Helper functions for actions
    function confirmDegree() {
        let value = parseInt(degreeInput.text)
        if (value >= 2 && value <= 20) {
            bridge.degree = value
        } else {
            degreeInput.text = bridge.degree.toString()
        }
    }

    function insertKeys() {
        if (insertInput.text.trim()) {
            bridge.insertKeys(insertInput.text)
            insertInput.text = ""
        }
    }

    function removeKeys() {
        if (removeInput.text.trim()) {
            bridge.deleteKeys(removeInput.text)
            removeInput.text = ""
        }
    }

    function searchKey() {
        if (searchInput.text.trim()) {
            bridge.searchKey(parseInt(searchInput.text))
            searchInput.text = ""
        }
    }
}
