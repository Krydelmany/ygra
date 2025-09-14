import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: canvas

    property real animationDuration: 600
    property real zoomLevel: 1.0
    property real panX: 0
    property real panY: 0
    property bool spacePressed: false
    property var nodes: []
    property var edges: []
    property var selectedNodeId: null

    signal nodeClicked(string nodeId)
    signal nodeDoubleClicked(string nodeId)

    function updateTree(newNodes, newEdges) {
        nodes = newNodes
        edges = newEdges

        // Update repeaters
        nodeRepeater.model = nodes
        edgeRepeater.model = edges

        // Auto-fit if first time
        if (nodes.length > 0 && zoomLevel === 1.0 && panX === 0 && panY === 0) {
            fitToView()
        }
    }

    function playAnimation(events) {
        // Smart animation that highlights the correct node
        if (events.length === 0) return
        
        // Find the most relevant node to highlight
        var targetNodeId = findTargetNodeForHighlight(events)
        
        if (targetNodeId) {
            // Single highlight with slight delay
            animationTimer.interval = 300
            animationTimer.nodeToHighlight = targetNodeId
            animationTimer.restart()
        }
    }
    
    function findTargetNodeForHighlight(events) {
        // Logic to find the correct node to highlight based on event types
        
        // Case 1: Single event - use that node
        if (events.length === 1) {
            return events[0].nodeId || ""
        }
        
        // Case 2: Multiple events - find the most relevant one
        for (var i = events.length - 1; i >= 0; i--) {
            var event = events[i]
            
            // Priority 1: If there's a split, highlight the NEW node (where the key actually went)
            if (event.type === "split" && event.newNodeId) {
                // For splits, we need to determine which node contains the inserted key
                // Check if this is an insertion sequence ending with split
                var hasInsertLeaf = false
                var insertedKey = -1
                
                for (var j = 0; j < events.length; j++) {
                    if (events[j].type === "insert_leaf" || events[j].type === "insert_root") {
                        hasInsertLeaf = true
                        insertedKey = events[j].key
                        break
                    }
                }
                
                if (hasInsertLeaf && insertedKey !== -1) {
                    // Determine which node contains the inserted key after split
                    // The promoted key is the middle key
                    var promotedKey = event.promoted || 0
                    
                    if (insertedKey > promotedKey) {
                        // Key went to the new (right) node
                        return event.newNodeId
                    } else {
                        // Key stayed in the original (left) node  
                        return event.nodeId
                    }
                }
                
                // Default: highlight the new node for splits
                return event.newNodeId
            }
            
            // Priority 2: Insert events
            if (event.type === "insert_leaf" || event.type === "insert_root") {
                return event.nodeId
            }
        }
        
        // Fallback: highlight the last node with an ID
        for (var k = events.length - 1; k >= 0; k--) {
            if (events[k].nodeId) {
                return events[k].nodeId
            }
        }
        
        return ""
    }

    Timer {
        id: animationTimer
        property string nodeToHighlight: ""
        onTriggered: highlightNode(nodeToHighlight)
    }

    function highlightNode(nodeId) {
        for (var i = 0; i < nodeRepeater.count; i++) {
            var nodeItem = nodeRepeater.itemAt(i)
            if (nodeItem && nodeItem.nodeId === nodeId) {
                nodeItem.highlight()
                break
            }
        }
    }

    function fitToView() {
        if (nodes.length === 0) return

        var minX = nodes[0].x, maxX = nodes[0].x
        var minY = nodes[0].y, maxY = nodes[0].y

        for (var i = 0; i < nodes.length; i++) {
            minX = Math.min(minX, nodes[i].x)
            maxX = Math.max(maxX, nodes[i].x)
            minY = Math.min(minY, nodes[i].y)
            maxY = Math.max(maxY, nodes[i].y)
        }

        var treeWidth = maxX - minX + 300
        var treeHeight = maxY - minY + 200

        var scaleX = width / treeWidth
        var scaleY = height / treeHeight
        var scale = Math.min(scaleX, scaleY, 1.5)

        zoomLevel = scale
        panX = -((minX + maxX) / 2) * scale + width / 2
        panY = -((minY + maxY) / 2) * scale + height / 2
    }

    function centerOnNode(nodeId) {
        for (var i = 0; i < nodes.length; i++) {
            if (nodes[i].id === nodeId) {
                panX = -nodes[i].x * zoomLevel + width / 2
                panY = -nodes[i].y * zoomLevel + height / 2
                break
            }
        }
    }

    // Modern dark canvas background
    Rectangle {
        anchors.fill: parent
        color: "#0a0a0a"

        // Simple grid pattern using Repeater instead of Canvas
        Repeater {
            model: Math.ceil(parent.width / 40)
            Rectangle {
                x: index * 40
                y: 0
                width: 1
                height: parent.height
                color: "#27272a"
                opacity: 0.1
            }
        }

        Repeater {
            model: Math.ceil(parent.height / 40)
            Rectangle {
                x: 0
                y: index * 40
                width: parent.width
                height: 1
                color: "#27272a"
                opacity: 0.1
            }
        }

        // Content container with transform
        Item {
            id: content
            width: parent.width
            height: parent.height

            transform: [
                Scale { 
                    xScale: canvas.zoomLevel
                    yScale: canvas.zoomLevel
                    origin.x: 0
                    origin.y: 0
                },
                Translate {
                    x: canvas.panX
                    y: canvas.panY
                }
            ]

            // Edges layer
            Repeater {
                id: edgeRepeater
                model: canvas.edges

                delegate: Line {
                    property var fromNode: findNode(modelData.fromId)
                    property var toNode: findNode(modelData.toId)

                    x1: fromNode ? fromNode.x : 0
                    y1: fromNode ? fromNode.y + 35 : 0
                    x2: toNode ? toNode.x : 0
                    y2: toNode ? toNode.y - 15 : 0
                    lineColor: "#52525b"

                    function findNode(id) {
                        for (var i = 0; i < canvas.nodes.length; i++) {
                            if (canvas.nodes[i].id === id) {
                                return canvas.nodes[i]
                            }
                        }
                        return null
                    }
                }
            }

            // Nodes layer
            Repeater {
                id: nodeRepeater
                model: canvas.nodes

                delegate: Node {
                    nodeId: modelData.id
                    keys: modelData.keys
                    isLeaf: modelData.isLeaf
                    x: modelData.x - width/2
                    y: modelData.y - height/2
                    selected: canvas.selectedNodeId === modelData.id

                    onClicked: {
                        canvas.selectedNodeId = nodeId
                        canvas.nodeClicked(nodeId)
                    }

                    onDoubleClicked: {
                        canvas.centerOnNode(nodeId)
                        canvas.nodeDoubleClicked(nodeId)
                    }

                    Behavior on x {
                        NumberAnimation { 
                            duration: canvas.animationDuration
                            easing.type: Easing.OutCubic
                        }
                    }

                    Behavior on y {
                        NumberAnimation { 
                            duration: canvas.animationDuration
                            easing.type: Easing.OutCubic
                        }
                    }
                }
            }

            // Smooth transform animations
            Behavior on transform {
                PropertyAnimation { 
                    duration: 400
                    easing.type: Easing.OutCubic
                }
            }
        }
    }

    // Enhanced mouse interaction
    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        hoverEnabled: true

        property real lastX: 0
        property real lastY: 0
        property bool panning: false

        onPressed: function(mouse) {
            if (canvas.spacePressed || mouse.button === Qt.RightButton) {
                panning = true
                lastX = mouse.x
                lastY = mouse.y
                cursorShape = Qt.ClosedHandCursor
            }
        }

        onPositionChanged: function(mouse) {
            if (panning) {
                canvas.panX += mouse.x - lastX
                canvas.panY += mouse.y - lastY
                lastX = mouse.x
                lastY = mouse.y
            }
        }

        onReleased: {
            panning = false
            cursorShape = canvas.spacePressed ? Qt.OpenHandCursor : Qt.ArrowCursor
        }

        onWheel: {
            var zoomFactor = wheel.angleDelta.y > 0 ? 1.15 : 0.85
            var newZoom = canvas.zoomLevel * zoomFactor

            // Clamp zoom with better limits
            newZoom = Math.max(0.2, Math.min(2.5, newZoom))

            // Zoom towards mouse position
            var mouseXWorld = (wheel.x - canvas.panX) / canvas.zoomLevel
            var mouseYWorld = (wheel.y - canvas.panY) / canvas.zoomLevel

            canvas.zoomLevel = newZoom
            canvas.panX = wheel.x - mouseXWorld * newZoom
            canvas.panY = wheel.y - mouseYWorld * newZoom
        }
    }

    // Enhanced keyboard interaction
    focus: true
    Keys.onPressed: {
        if (event.key === Qt.Key_Space) {
            canvas.spacePressed = true
            event.accepted = true
        } else if (event.key === Qt.Key_0 || event.key === Qt.Key_Home) {
            fitToView()
            event.accepted = true
        } else if (event.key === Qt.Key_Plus || event.key === Qt.Key_Equal) {
            canvas.zoomLevel = Math.min(2.5, canvas.zoomLevel * 1.2)
            event.accepted = true
        } else if (event.key === Qt.Key_Minus || event.key === Qt.Key_Underscore) {
            canvas.zoomLevel = Math.max(0.2, canvas.zoomLevel * 0.8)
            event.accepted = true
        } else if (event.key === Qt.Key_R) {
            // Reset view
            canvas.zoomLevel = 1.0
            canvas.panX = 0
            canvas.panY = 0
            event.accepted = true
        }
    }

    Keys.onReleased: {
        if (event.key === Qt.Key_Space) {
            canvas.spacePressed = false
            event.accepted = true
        }
    }

    Component.onCompleted: {
        forceActiveFocus()
    }

    // Modern zoom controls overlay
    Rectangle {
        anchors.bottom: parent.bottom
        anchors.right: parent.right
        anchors.margins: 20
        width: 120
        height: 40
        color: "#18181b"
        border.color: "#27272a"
        border.width: 1
        radius: 8
        opacity: 0.9

        Row {
            anchors.centerIn: parent
            spacing: 8

            Rectangle {
                width: 32
                height: 32
                color: "#27272a"
                border.color: "#52525b"
                border.width: 1
                radius: 6
                
                Text {
                    anchors.centerIn: parent
                    text: "−"
                    font.pixelSize: 16
                    color: "#ffffff"
                }
                
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    
                    onEntered: {
                        parent.color = "#3f3f46"
                        parent.border.color = "#71717a"
                    }
                    onExited: {
                        parent.color = "#27272a"
                        parent.border.color = "#52525b"
                    }
                    onPressed: {
                        parent.color = "#18181b"
                    }
                    onReleased: {
                        parent.color = containsMouse ? "#3f3f46" : "#27272a"
                        parent.border.color = containsMouse ? "#71717a" : "#52525b"
                    }
                    onClicked: canvas.zoomLevel = Math.max(0.2, canvas.zoomLevel * 0.8)
                }
            }

            Rectangle {
                width: 40
                height: 32
                color: "#27272a"
                border.color: "#52525b"
                border.width: 1
                radius: 6
                
                Text {
                    anchors.centerIn: parent
                    text: "⌂"
                    font.pixelSize: 14
                    color: "#ffffff"
                }
                
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    
                    onEntered: {
                        parent.color = "#3f3f46"
                        parent.border.color = "#71717a"
                    }
                    onExited: {
                        parent.color = "#27272a"
                        parent.border.color = "#52525b"
                    }
                    onPressed: {
                        parent.color = "#18181b"
                    }
                    onReleased: {
                        parent.color = containsMouse ? "#3f3f46" : "#27272a"
                        parent.border.color = containsMouse ? "#71717a" : "#52525b"
                    }
                    onClicked: fitToView()
                }
            }

            Rectangle {
                width: 32
                height: 32
                color: "#27272a"
                border.color: "#52525b"
                border.width: 1
                radius: 6
                
                Text {
                    anchors.centerIn: parent
                    text: "+"
                    font.pixelSize: 16
                    color: "#ffffff"
                }
                
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    
                    onEntered: {
                        parent.color = "#3f3f46"
                        parent.border.color = "#71717a"
                    }
                    onExited: {
                        parent.color = "#27272a"
                        parent.border.color = "#52525b"
                    }
                    onPressed: {
                        parent.color = "#18181b"
                    }
                    onReleased: {
                        parent.color = containsMouse ? "#3f3f46" : "#27272a"
                        parent.border.color = containsMouse ? "#71717a" : "#52525b"
                    }
                    onClicked: canvas.zoomLevel = Math.min(2.5, canvas.zoomLevel * 1.2)
                }
            }
        }
    }
}
