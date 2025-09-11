import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15
import QtQuick.Shapes 1.15
import QtQuick.Effects 
import Qt.labs.settings 1.1

ApplicationWindow {
    id: root
    visible: true
    width: 1200
    height: 800
    title: typeof(APP_TITLE) === "string" ? APP_TITLE : "ygra"

    // ---- TEMA MINIMALISTA ----
    Settings { id: themeSettings; property bool darkTheme: true }
    Material.theme: themeSettings.darkTheme ? Material.Dark : Material.Light
    Material.primary: Material.Blue
    Material.accent: Material.Cyan
    
    property color primaryColor: themeSettings.darkTheme ? "#3b82f6" : "#2563eb"
    property color surfaceColor: themeSettings.darkTheme ? "#1f1f1f" : "#ffffff"
    property color cardColor: themeSettings.darkTheme ? "#2a2a2a" : "#f8f9fa"
    property color textColor: themeSettings.darkTheme ? "#ffffff" : "#1f2937"
    property color borderColor: themeSettings.darkTheme ? "#404040" : "#e5e7eb"

    // ---- HEADER MINIMALISTA ----
    header: Rectangle {
        height: 48
        color: surfaceColor
        border.width: 1
        border.color: borderColor
        
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 16
            anchors.rightMargin: 16
            spacing: 16
            
            // Logo simples
            Text {
                text: "ygra"
                font.bold: true
                font.pointSize: 14
                color: primaryColor
            }
            
            Rectangle { width: 1; height: 24; color: borderColor }
            
            // Botões simples sem ícones
            Button {
                text: "Novo"
                flat: true
                hoverEnabled: true
                
                background: Rectangle {
                    color: parent.hovered ? (themeSettings.darkTheme ? "#404040" : "#f3f4f6") : "transparent"
                    radius: 0
                }
            }
            
            Button {
                text: "Abrir"
                flat: true
                hoverEnabled: true
                
                background: Rectangle {
                    color: parent.hovered ? (themeSettings.darkTheme ? "#404040" : "#f3f4f6") : "transparent"
                    radius: 0
                }
            }
            
            Button {
                text: "Salvar"
                flat: true
                hoverEnabled: true
                
                background: Rectangle {
                    color: parent.hovered ? (themeSettings.darkTheme ? "#404040" : "#f3f4f6") : "transparent"
                    radius: 0
                }
            }
            
            Rectangle { width: 1; height: 24; color: borderColor }
            
            // Campo de busca simples, menor verticalmente
            TextField {
                id: searchBox
                Layout.fillWidth: true
                Layout.maximumWidth: 250
                Layout.preferredWidth: 200
                placeholderText: "Buscar nós..."
                selectByMouse: true
                height: 28
                font.pointSize: 10
                padding: 4
                background: Rectangle {
                    radius: 4
                    color: "transparent"
                    border.color: borderColor
                    border.width: 1
                }
            }
            Item { Layout.fillWidth: true }
            
            // Toggle de tema simples
            Button {
                text: themeSettings.darkTheme ? "Claro" : "Escuro"
                flat: true
                hoverEnabled: true
                onClicked: themeSettings.darkTheme = !themeSettings.darkTheme
                
                background: Rectangle {
                    color: parent.hovered ? (themeSettings.darkTheme ? "#404040" : "#f3f4f6") : "transparent"
                    radius: 0
                }
            }
            
            Text {
                text: typeof(APP_VERSION) === "string" ? "v" + APP_VERSION : "v0.1.0"
                color: textColor
                opacity: 0.6
                font.pointSize: 9
            }
        }
    }

    // ---- FOOTER SIMPLES ----
    footer: Rectangle {
        height: 32
        color: surfaceColor
        border.width: 1
        border.color: borderColor
        
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 16
            anchors.rightMargin: 16
            spacing: 16
            
            Text {
                text: "Zoom: " + Math.round(canvasView.zoom * 100) + "%"
                color: textColor
                font.pointSize: 10
            }
            
            Rectangle { width: 1; height: 16; color: borderColor }
            
            Text {
                text: "Pos: (" + Math.round(canvasView.offsetX) + ", " + Math.round(canvasView.offsetY) + ")"
                color: textColor
                font.pointSize: 10
            }
            
            Item { Layout.fillWidth: true }
            
            Text {
                text: "Scroll para zoom • Arraste para mover"
                color: textColor
                opacity: 0.6
                font.pointSize: 10
            }
        }
    }

    // ---- PAINEL LATERAL MINIMALISTA ----
    Rectangle {
        id: sidePanel
        width: 280
        anchors {
            left: parent.left
            top: parent.top
            bottom: parent.bottom
        }
        
        color: surfaceColor
        border.width: 1
        border.color: borderColor

        ScrollView {
            anchors.fill: parent
            anchors.margins: 16
            contentWidth: parent.width - 32
            
            ColumnLayout {
                width: parent.width
                spacing: 24

                // Título
                Text {
                    text: "Controles"
                    font.bold: true
                    font.pointSize: 14
                    color: textColor
                    Layout.topMargin: 8
                }

                // Propriedades
                GroupBox {
                    title: "Propriedades"
                    Layout.fillWidth: true
                    
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 8
                        
                        TextField {
                            Layout.fillWidth: true
                            placeholderText: "Nome do nó..."
                        }
                        
                        TextArea {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 80
                            placeholderText: "Descrição..."
                            wrapMode: TextArea.Wrap
                        }
                    }
                }

                // Ações
                GroupBox {
                    title: "Ações"
                    Layout.fillWidth: true
                    
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 8
                        
                        Button {
                            text: "Adicionar Filho"
                            Layout.fillWidth: true
                        }
                        
                        Button {
                            text: "Remover Nó"
                            Layout.fillWidth: true
                        }
                        
                        // RowLayout {
                        //     Layout.fillWidth: true
                        //     spacing: 8
                            
                        //     Button {
                        //         text: "BFS"
                        //         Layout.fillWidth: true
                        //     }
                            
                        //     Button {
                        //         text: "DFS"
                        //         Layout.fillWidth: true
                        //     }
                        // }
                    }
                }

                // Métricas
                GroupBox {
                    title: "Métricas"
                    Layout.fillWidth: true
                    
                    GridLayout {
                        anchors.fill: parent
                        columns: 2
                        columnSpacing: 12
                        rowSpacing: 6
                        
                        Text { text: "Altura:"; color: textColor }
                        Text { text: "3"; color: primaryColor; font.bold: true }
                        
                        Text { text: "Nós:"; color: textColor }
                        Text { text: "4"; color: primaryColor; font.bold: true }
                        
                        Text { text: "Folhas:"; color: textColor }
                        Text { text: "3"; color: primaryColor; font.bold: true }
                    }
                }

                // Configurações
                // GroupBox {
                //     title: "Configurações"
                //     Layout.fillWidth: true
                    
                //     ColumnLayout {
                //         anchors.fill: parent
                //         spacing: 8
                        
                //         Text {
                //             text: "Velocidade das animações"
                //             color: textColor
                //         }
                        
                //         Slider {
                //             id: speedSlider
                //             Layout.fillWidth: true
                //             from: 0.2
                //             to: 1.0
                //             value: 1.0
                //             stepSize: 0.1
                //             onValueChanged: canvasView.animationSpeed = value
                //         }
                        
                //         Text {
                //             text: animationSpeedText(speedSlider.value)
                //             color: textColor
                //             opacity: 0.7
                //             font.pointSize: 9
                //         }
                //     }
                // }
            }
        }
    }

    // Canvas central ocupa o restante
    CanvasView {
        id: canvasView
        anchors {
            left: sidePanel.right
            right: parent.right
            top: parent.top
            bottom: parent.bottom
        }
    }

    function animationSpeedText(v) {
        if (v < 0.6) return "Lento"
        if (v < 1.2) return "Normal"
        if (v < 1.6) return "Rápido"
        return "Muito rápido"
    }

    // ================= COMPONENTES INLINE =================

    // Área de desenho com gradiente, grid, zoom/pan e nós/arestas mock
    component CanvasView: Item {
        property real zoom: 1.0
        property real offsetX: 0.0
        property real offsetY: 0.0
        property real animationSpeed: 1.0
        focus: true
        clip: true

        // Background com gradiente radial sutil
        Rectangle {
            anchors.fill: parent
            gradient: Gradient {
                GradientStop { 
                    position: 0.0
                    color: themeSettings.darkTheme ? "#0f172a" : "#f8fafc"
                }
                GradientStop { 
                    position: 0.5
                    color: themeSettings.darkTheme ? "#1e293b" : "#e2e8f0"
                }
                GradientStop { 
                    position: 1.0
                    color: themeSettings.darkTheme ? "#111827" : "#f1f5f9"
                }
            }
        }

        // Grid dinâmico mais elegante
        Repeater {
            model: 100
            Rectangle {
                width: parent.width
                height: 1
                y: (index * 25 * zoom) + offsetY % 25
                color: themeSettings.darkTheme ? "#1f2937" : "#e2e8f0"
                opacity: 0.3
            }
        }
        
        Repeater {
            model: 120
            Rectangle {
                width: 1
                height: parent.height
                x: (index * 25 * zoom) + offsetX % 25
                color: themeSettings.darkTheme ? "#1f2937" : "#e2e8f0"
                opacity: 0.3
            }
        }

        // Área para os nós com transformação
        Item {
            id: scene
            x: parent.width/2 + offsetX
            y: parent.height/2 + offsetY
            transform: Scale { xScale: zoom; yScale: zoom; origin.x: 0; origin.y: 0 }

            // Conexões simples
            SimpleConnection { fromX: 0; fromY: -30; toX: -160; toY: 30 }
            SimpleConnection { fromX: 0; fromY: -30; toX: 0; toY: 30 }
            SimpleConnection { fromX: 0; fromY: -30; toX: 160; toY: 30 }

            // Nós como círculos
            CircleNode { 
                x: -15; y: -45
                nodeText: "Raiz"
                textColor: "#000000"
                nodeColor: "#ffffff"
                isRoot: true
            }
            
            CircleNode { 
                x: -175; y: 15
                nodeText: "A"
                nodeColor: "#ffffff"
            }
            
            CircleNode { 
                x: -15; y: 15
                nodeText: "B"
                nodeColor: "#ffffff"
            }
            
            CircleNode { 
                x: 145; y: 15
                nodeText: "C"
                nodeColor: "#ffffff"
            }
        }

        WheelHandler {
            acceptedDevices: PointerDevice.Mouse | PointerDevice.TouchPad
            onWheel: (event) => {
                const delta = event.angleDelta.y > 0 ? 0.1 : -0.1
                const newZoom = Math.min(2.0, Math.max(0.3, zoom + delta))
                zoom = newZoom
                event.accepted = true
            }
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            drag.target: null
            property real lastX: 0
            property real lastY: 0
            onPressed: (mouse) => { lastX = mouse.x; lastY = mouse.y }
            onPositionChanged: (mouse) => {
                if (mouse.buttons & Qt.LeftButton) {
                    offsetX += mouse.x - lastX
                    offsetY += mouse.y - lastY
                    lastX = mouse.x
                    lastY = mouse.y
                }
            }
        }

        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_Plus)  { zoom = Math.min(2.0, zoom + 0.1) }
            if (event.key === Qt.Key_Minus) { zoom = Math.max(0.3, zoom - 0.1) }
            if (event.key === Qt.Key_0)     { zoom = 1.0; offsetX = 0; offsetY = 0 }
        }
    }

    // Nó com sombra e hover suave
    component NodeBubble: Item {
        property alias label: nodeText.text
        width: 120; height: 68

        Item {
            anchors.fill: parent

            Rectangle {
                id: bg
                anchors.fill: parent
                radius: 18
                color: Material.theme === Material.Dark ? "#253042" : "#ffffff"
                border.color: Material.theme === Material.Dark ? "#3b4b61" : "#dfe3ea"
            }

            MultiEffect {
                anchors.fill: bg
                source: bg
                shadowEnabled: true
                shadowBlur: 0.55
                shadowHorizontalOffset: 0
                shadowVerticalOffset: 2
                shadowColor: Material.theme === Material.Dark ? "#90000000" : "#30000000"
            }

            Text {
                id: nodeText
                anchors.centerIn: bg
                text: "Nó"
                font.bold: true
                font.pointSize: 10
                renderType: Text.NativeRendering
            }

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                onEntered: bg.scale = 1.04
                onExited:  bg.scale = 1.0
            }
        }
    }

    // Aresta curva
    component EdgeCurve: Shape {
        property real fromX: 0
        property real fromY: 0
        property real toX: 100
        property real toY: 100
        ShapePath {
            strokeWidth: 2
            strokeColor: Material.theme === Material.Dark ? "#6aa2ff" : "#1565c0"
            fillColor: "transparent"
            startX: fromX; startY: fromY
            PathCubic {
                x: toX; y: toY
                control1X: fromX; control1Y: (fromY + toY)/2
                control2X: toX;   control2Y: (fromY + toY)/2
            }
        }
    }

    // ================= COMPONENTES MINIMALISTAS =================
    
    component CircleNode: Item {
        id: node
        width: 30
        height: 30
        
        property alias nodeText: label.text
        property color nodeColor: primaryColor
        property color textColor: root.textColor
        property bool isRoot: false
        property bool hovered: mouseArea.containsMouse
        
        signal clicked()
        
        // Círculo principal
        Rectangle {
            id: circle
            anchors.centerIn: parent
            width: isRoot ? 30 : 24
            height: width
            radius: width / 2
            color: nodeColor
            border.width: isRoot ? 3 : 2
            border.color: Qt.lighter(nodeColor, 1.3)
        }
        
        // Texto do nó (aparece no hover)
        Rectangle {
            id: labelBackground
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.bottom
            anchors.topMargin: 8
            width: label.width + 12
            height: label.height + 6
            radius: 4
            color: surfaceColor
            border.width: 1
            border.color: borderColor
            visible: hovered
            opacity: hovered ? 1 : 0
            
            Text {
                id: label
                anchors.centerIn: parent
                text: "Nó"
                font.pointSize: 9
                color: textColor
            }
        }
        
        // Área de interação
        MouseArea {
            id: mouseArea
            anchors.fill: parent
            anchors.margins: -10
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            
            onClicked: node.clicked()
            onEntered: circle.scale = 1.2
            onExited: circle.scale = 1.0
        }
    }
    
    component SimpleConnection: Shape {
        property real fromX: 0
        property real fromY: 0
        property real toX: 100
        property real toY: 100
        
        ShapePath {
            strokeWidth: 2
            strokeColor: borderColor
            fillColor: "transparent"
            
            startX: fromX
            startY: fromY
            
            PathLine {
                x: toX
                y: toY
            }
        }
    }
}
