# Explicação Completa da Implementação da Árvore B

Este documento explica em detalhes como toda a aplicação de visualização da árvore B foi implementada, analisando cada arquivo e componente do sistema.

## Visão Geral da Arquitetura

A aplicação está dividida em camadas bem definidas:

```
┌─────────────────────┐
│   Interface QML     │ ← Tela que o usuário vê
├─────────────────────┤
│   Bridge (Python)   │ ← Ponte entre Python e QML  
├─────────────────────┤
│   Core Logic        │ ← Lógica da árvore B
│   (BTree + Layout)  │
└─────────────────────┘
```

## 1. Ponto de Entrada - `main.py`

### O que faz este arquivo?
É o arquivo que você executa para iniciar o programa. Ele faz 3 coisas principais:

1. **Configura a aplicação Qt/QML**
2. **Carrega a interface gráfica**
3. **Conecta tudo**

### Como funciona?

```python
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("B-Tree Visualizer")
    
    # Registra os tipos QML personalizados
    register_bridge()
    
    # Cria o motor QML
    engine = QQmlApplicationEngine()
    
    # Carrega o arquivo principal da interface
    qml_file = Path(__file__).parent / "src" / "ui" / "main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    
    return app.exec()
```

**Explicação linha por linha:**
- `QApplication`: Cria a aplicação Qt
- `register_bridge()`: Registra nossa classe Bridge para usar no QML
- `QQmlApplicationEngine`: Motor que interpreta arquivos QML
- `engine.load()`: Carrega a interface gráfica
- `app.exec()`: Roda o loop principal da aplicação

### Funcionalidades extras:
- **Tema escuro**: Código comentado para configurar cores escuras
- **Barra de título escura**: Suporte específico para Windows

---

## 2. Lógica Central - `src/core/btree.py`

Este é o **coração** do programa. Contém toda a lógica da árvore B.

### Classe `BNode` - Representa um Nó

```python
class BNode:
    def __init__(self, leaf: bool = True):
        self.keys: List[int] = []        # Números armazenados
        self.children: List['BNode'] = [] # Filhos (se não for folha)
        self.leaf: bool = leaf           # Se é folha ou não
        self.id: str = str(uuid.uuid4()) # ID único para animações
```

**O que cada nó contém:**
- **keys**: Lista dos números armazenados (ex: [1, 5, 9])
- **children**: Lista dos nós filhos (só existe se não for folha)
- **leaf**: True se for folha (sem filhos), False se for nó interno
- **id**: Identificador único para animações

### Classe `BTree` - A Árvore Completa

#### Inicialização
```python
def __init__(self, t: int = 2, max_keys: Optional[int] = None):
    if max_keys is not None:
        t = max(2, (max_keys + 1) // 2)
        self._max_keys = max_keys
    else:
        self._max_keys = 2 * t - 1
```

**Como funciona:**
- Se você especificar `max_keys=2`, a árvore terá no máximo 2 números por nó
- Se você especificar `t=3`, a árvore terá no máximo `2*3-1 = 5` números por nó
- O programa usa `max_keys` porque é mais intuitivo

#### Busca (`search`)
```python
def search(self, key: int) -> Tuple[bool, List[Dict[str, Any]], List[BNode]]:
    events = []
    path = []
    current = self.root
    
    while current:
        path.append(current)
        events.append({"type": "visit", "nodeId": current.id})
        
        # Encontra posição da chave no nó atual
        i = current.find_key_index(key)
        
        # Se encontrou a chave
        if i < len(current.keys) and current.keys[i] == key:
            events.append({"type": "found", "nodeId": current.id, "keyIndex": i})
            return True, events, path
            
        # Se é folha, não encontrou
        if current.leaf:
            break
            
        # Vai para o filho
        current = current.children[i]
    
    return False, events, path
```

**Como a busca funciona:**
1. Começa na raiz
2. Para cada nó visitado, gera um evento "visit"
3. Procura a posição onde a chave deveria estar
4. Se encontrou, gera evento "found" e retorna True
5. Se é folha e não encontrou, retorna False
6. Senão, desce para o filho apropriado

#### Inserção (`insert`)
A inserção é mais complexa porque pode precisar dividir nós:

```python
def insert(self, key: int) -> List[Dict[str, Any]]:
    # Verifica duplicatas
    found, _, _ = self.search(key)
    if found:
        return [{"type": "error", "message": f"Chave {key} já existe"}]
    
    # Cria raiz se árvore vazia
    if not self.root:
        self.root = BNode(leaf=True)
        self.root.keys.append(key)
        return [{"type": "insert_root", "nodeId": self.root.id, "key": key}]
    
    # Insere usando algoritmo padrão
    self._insert_non_full(self.root, key, events)
    
    # Se raiz ficou muito cheia, divide
    if len(self.root.keys) > self._max_keys:
        new_root = BNode(leaf=False)
        new_root.children.append(self.root)
        self._split_child(new_root, 0, events)
        self.root = new_root
```

**Algoritmo de inserção:**
1. Verifica se a chave já existe
2. Se árvore vazia, cria raiz com a chave
3. Usa algoritmo padrão de inserção
4. Se raiz ficou muito cheia, cria nova raiz e divide

#### Divisão de Nós (`_split_child`)
Quando um nó fica com muitas chaves, ele precisa ser dividido:

```python
def _split_child(self, parent: BNode, index: int, events: List[Dict[str, Any]]):
    full_child = parent.children[index]
    new_child = BNode(leaf=full_child.leaf)
    
    mid_index = len(full_child.keys) // 2
    mid_key = full_child.keys[mid_index]
    
    # Divide as chaves
    new_child.keys = full_child.keys[mid_index + 1:]
    full_child.keys = full_child.keys[:mid_index]
    
    # Divide os filhos (se não for folha)
    if not full_child.leaf:
        new_child.children = full_child.children[mid_index + 1:]
        full_child.children = full_child.children[:mid_index + 1]
    
    # Sobe a chave do meio para o pai
    parent.keys.insert(index, mid_key)
    parent.children.insert(index + 1, new_child)
```

**Como funciona a divisão:**
1. Pega o nó cheio
2. Encontra a chave do meio
3. Cria novo nó com as chaves da direita
4. Deixa as chaves da esquerda no nó original
5. Sobe a chave do meio para o pai

---

## 3. Cálculo de Layout - `src/core/layout.py`

Este arquivo calcula onde cada nó deve aparecer na tela.

### Função Principal (`layout`)
```python
def layout(tree: BTree) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    if not tree.root:
        return [], []
    
    nodes = []
    edges = []
    
    # Calcula posições usando travessia por níveis
    levels = _build_level_data(tree.root)
    _assign_positions(levels, nodes, edges)
    
    return nodes, edges
```

**O que retorna:**
- **nodes**: Lista com posição (x, y) de cada nó
- **edges**: Lista com as conexões entre nós

### Construção de Níveis (`_build_level_data`)
```python
def _build_level_data(root: BNode) -> List[List[BNode]]:
    levels = []
    queue = [root]
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        for _ in range(level_size):
            node = queue.pop(0)
            current_level.append(node)
            
            # Adiciona filhos à fila
            for child in node.children:
                queue.append(child)
        
        levels.append(current_level)
    
    return levels
```

**Como funciona:**
1. Usa algoritmo BFS (busca em largura)
2. Agrupa nós por nível (altura na árvore)
3. Retorna lista de listas: `[[raiz], [nível1], [nível2], ...]`

### Atribuição de Posições (`_assign_positions`)
```python
def _assign_positions(levels, nodes, edges):
    LEVEL_HEIGHT = 120    # Espaçamento vertical
    MIN_NODE_SPACING = 150  # Espaçamento horizontal
    
    for level_idx, level in enumerate(levels):
        y = level_idx * LEVEL_HEIGHT + 50
        
        # Calcula largura total necessária
        total_width = 0
        for node in level:
            width = max(subtree_widths[node.id] * MIN_NODE_SPACING, MIN_NODE_SPACING)
            total_width += width
        
        # Centraliza o nível
        start_x = -total_width / 2
        current_x = start_x
        
        for node in level:
            node_width = max(subtree_widths[node.id] * MIN_NODE_SPACING, MIN_NODE_SPACING)
            x = current_x + node_width / 2
            
            nodes.append({
                "id": node.id,
                "keys": node.keys.copy(),
                "x": x,
                "y": y,
                "isLeaf": node.leaf
            })
```

**Estratégia de posicionamento:**
1. Cada nível tem altura fixa (120 pixels de diferença)
2. Calcula quantos "filhos" cada nó tem na árvore
3. Dá mais espaço horizontal para nós com mais descendentes
4. Centraliza tudo na tela

---

## 4. Ponte Python-QML - `src/app/bridge.py`

Esta é a **ponte** entre a lógica Python e a interface QML.

### Classe Bridge
```python
class Bridge(QObject):
    # Sinais (enviam dados para QML)
    treeChanged = Signal(list, list)  # nodes, edges
    metricsChanged = Signal('QVariant')  # metrics dict
    eventsReady = Signal(list)  # animation events
    message = Signal(str, str)  # text, kind
    degreeChanged = Signal()  # signal for degree property
```

**Sinais explicados:**
- **treeChanged**: Quando árvore muda, envia novos nós e conexões
- **metricsChanged**: Envia estatísticas (altura, número de nós, etc.)
- **eventsReady**: Envia eventos para animações
- **message**: Envia mensagens para mostrar ao usuário

### Propriedade Grau
```python
@Property(int, notify=degreeChanged)
def degree(self):
    return self._degree

@degree.setter
def degree(self, value):
    if value != self._degree and value >= 2:
        self._degree = value
        max_keys = value - 1  # grau 3 = máx 2 chaves
        self._tree = BTree(max_keys=max_keys)
        self._emit_tree_update()
        self.degreeChanged.emit()
```

**Como funciona:**
- QML pode ler e modificar a propriedade `degree`
- Quando muda, recria a árvore com novo limite de chaves
- Emite sinal para QML se atualizar

### Slot de Inserção
```python
@Slot(str)
def insertKeys(self, text: str):
    try:
        # Processa texto: "1,2,3" → [1, 2, 3]
        keys_str = text.replace(" ", "").split(",")
        keys = [int(key_str.strip()) for key_str in keys_str if key_str.strip()]
        
        all_events = []
        inserted_count = 0
        
        for key in keys:
            events = self._tree.insert(key)
            
            if events and events[0].get("type") != "error":
                all_events.extend(events)
                inserted_count += 1
            else:
                error_msg = events[0].get("message", f"Erro ao inserir {key}")
                self.message.emit(error_msg, "error")
        
        if inserted_count > 0:
            self._emit_tree_update()
            if all_events:
                self.eventsReady.emit(all_events)
            self.message.emit(f"{inserted_count} chave(s) inserida(s)", "success")
    
    except ValueError:
        self.message.emit("Formato inválido. Use números separados por vírgula", "error")
```

**Processo de inserção:**
1. Recebe texto do QML (ex: "1,2,3,4")
2. Converte para lista de números
3. Insere cada número na árvore
4. Coleta eventos de animação
5. Atualiza interface e envia animações

---

## 5. Interface Principal - `src/ui/main.qml`

Este arquivo define toda a interface gráfica usando QML.

### Estrutura da Janela
```qml
ApplicationWindow {
    id: window
    visible: true
    width: 1600
    height: 1000
    title: "B-Tree Visualizer"
    color: "#0a0a0a"  // Fundo preto
    
    Bridge {
        id: bridge
        
        onTreeChanged: function(nodes, edges) {
            canvas.updateTree(nodes, edges)
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
}
```

**Componentes principais:**
- **Bridge**: Instância da ponte Python-QML
- **Conectores de eventos**: Quando Python emite sinais, QML reage

### Layout da Interface
```qml
RowLayout {
    anchors.fill: parent
    
    // Barra lateral esquerda - Controles
    Rectangle {
        Layout.preferredWidth: 350
        Layout.fillHeight: true
        color: "#0a0a0a"
        
        ColumnLayout {
            // Cabeçalho
            Column { /* título e descrição */ }
            
            // Controle de grau
            Rectangle { /* input para definir grau */ }
            
            // Controles de operação
            Column { /* inserir, buscar, remover */ }
            
            // Botões de exemplo
            Column { /* carregar exemplos */ }
            
            // Painel de métricas
            MetricsPanel { /* estatísticas da árvore */ }
        }
    }
    
    // Área principal - Canvas da árvore
    TreeCanvas {
        Layout.fillWidth: true
        Layout.fillHeight: true
    }
}
```

### Controles de Entrada
```qml
// Controle de grau
SpinBox {
    id: degreeSpinBox
    from: 2
    to: 10
    value: bridge.degree
    
    onValueChanged: {
        if (value !== bridge.degree) {
            bridge.degree = value
        }
    }
}

// Campo de inserção
TextField {
    id: insertField
    placeholderText: "Ex: 1,2,3,4,5"
    
    Keys.onReturnPressed: {
        bridge.insertKeys(text)
        text = ""
    }
}

Button {
    text: "Inserir"
    onClicked: {
        bridge.insertKeys(insertField.text)
        insertField.text = ""
    }
}
```

**Como funciona:**
- SpinBox está ligado à propriedade `bridge.degree`
- TextField coleta texto do usuário
- Button chama `bridge.insertKeys()` com o texto

---

## 6. Canvas da Árvore - `src/ui/TreeCanvas.qml`

Este componente desenha e anima a árvore.

### Estrutura Principal
```qml
Item {
    id: canvas
    
    property var nodes: []
    property var edges: []
    property real zoomLevel: 1.0
    property real panX: 0
    property real panY: 0
    
    function updateTree(newNodes, newEdges) {
        nodes = newNodes
        edges = newEdges
        
        nodeRepeater.model = nodes
        edgeRepeater.model = edges
        
        if (nodes.length > 0 && zoomLevel === 1.0) {
            fitToView()
        }
    }
}
```

### Sistema de Animação
```qml
function playAnimation(events) {
    if (events.length === 0) return
    
    var targetNodeId = findTargetNodeForHighlight(events)
    
    if (targetNodeId) {
        animationTimer.interval = 300
        animationTimer.nodeToHighlight = targetNodeId
        animationTimer.restart()
    }
}

function findTargetNodeForHighlight(events) {
    // Lógica inteligente para destacar o nó correto
    
    // Caso 1: Evento único
    if (events.length === 1) {
        return events[0].nodeId || ""
    }
    
    // Caso 2: Múltiplos eventos - procura o mais relevante
    for (var i = events.length - 1; i >= 0; i--) {
        var event = events[i]
        
        // Prioridade 1: Split (divisão)
        if (event.type === "split" && event.newNodeId) {
            // Determina qual nó contém a chave inserida
            var insertedKey = getInsertedKeyFromEvents(events)
            var promotedKey = event.promoted || 0
            
            if (insertedKey > promotedKey) {
                return event.newNodeId  // Nó da direita
            } else {
                return event.nodeId     // Nó da esquerda
            }
        }
        
        // Prioridade 2: Inserção
        if (event.type === "insert_leaf" || event.type === "insert_root") {
            return event.nodeId
        }
    }
}
```

**Lógica de animação:**
1. Analisa lista de eventos da operação
2. Determina qual nó é mais importante destacar
3. Para divisões, destaca o nó onde a chave foi parar
4. Para inserções simples, destaca o nó modificado

### Navegação (Zoom e Pan)
```qml
MouseArea {
    anchors.fill: parent
    
    onWheel: function(wheel) {
        var delta = wheel.angleDelta.y > 0 ? 1.1 : 0.9
        var newZoom = Math.max(0.1, Math.min(3.0, zoomLevel * delta))
        
        if (newZoom !== zoomLevel) {
            zoomLevel = newZoom
        }
    }
    
    property bool dragging: false
    property real startX: 0
    property real startY: 0
    
    onPressed: function(mouse) {
        if (spacePressed) {
            dragging = true
            startX = mouse.x
            startY = mouse.y
        }
    }
    
    onPositionChanged: function(mouse) {
        if (dragging && spacePressed) {
            panX += (mouse.x - startX) / zoomLevel
            panY += (mouse.y - startY) / zoomLevel
            startX = mouse.x
            startY = mouse.y
        }
    }
}
```

**Controles de navegação:**
- **Roda do mouse**: Zoom in/out
- **Espaço + arrastar**: Move a visualização
- **Duplo clique**: Centraliza em um nó

---

## 7. Componentes Visuais

### Nó da Árvore - `src/ui/Node.qml`
```qml
Rectangle {
    id: nodeRect
    width: Math.max(120, keysText.contentWidth + 24)
    height: 60
    color: isHighlighted ? "#3b82f6" : "#18181b"
    border.color: isSelected ? "#f59e0b" : "#374151"
    border.width: 2
    radius: 8
    
    Text {
        id: keysText
        anchors.centerIn: parent
        text: nodeKeys.join(", ")
        color: "#ffffff"
        font.pixelSize: 16
        font.weight: Font.Medium
    }
    
    // Animação de destaque
    PropertyAnimation {
        id: highlightAnimation
        target: nodeRect
        property: "color"
        to: "#10b981"
        duration: 200
        
        onFinished: {
            // Volta à cor normal após 1 segundo
            Qt.callLater(function() {
                nodeRect.color = "#18181b"
            })
        }
    }
}
```

### Linha de Conexão - `src/ui/Line.qml`
```qml
Rectangle {
    id: line
    color: "#6b7280"
    
    transform: [
        Translate { x: line.width / 2; y: line.height / 2 },
        Rotation { angle: line.angle },
        Translate { x: -line.width / 2; y: -line.height / 2 }
    ]
    
    property real angle: Math.atan2(toY - fromY, toX - fromX) * 180 / Math.PI
    property real distance: Math.sqrt(Math.pow(toX - fromX, 2) + Math.pow(toY - fromY, 2))
    
    width: distance
    height: 2
    x: fromX
    y: fromY
}
```

---

## 8. Fluxo Completo de uma Operação

Vamos acompanhar o que acontece quando você insere "1,2,3":

### 1. Interface (QML)
```qml
// Usuário digita "1,2,3" e clica "Inserir"
Button {
    onClicked: {
        bridge.insertKeys(insertField.text)  // "1,2,3"
        insertField.text = ""
    }
}
```

### 2. Bridge (Python)
```python
@Slot(str)
def insertKeys(self, text: str):
    # Converte "1,2,3" → [1, 2, 3]
    keys = [1, 2, 3]
    
    all_events = []
    for key in keys:
        events = self._tree.insert(key)  # Insere na árvore
        all_events.extend(events)
    
    self._emit_tree_update()      # Envia nova estrutura
    self.eventsReady.emit(all_events)  # Envia animações
```

### 3. Árvore B (Python)
```python
def insert(self, key: int):
    # Para key=1: cria raiz [1]
    # Para key=2: adiciona → [1,2] 
    # Para key=3: adiciona → [1,2,3] (pode precisar dividir)
    
    events = [{"type": "insert_leaf", "nodeId": "...", "key": key}]
    return events
```

### 4. Layout (Python)
```python
def layout(tree):
    # Calcula posições dos nós
    nodes = [
        {"id": "abc", "keys": [1,2,3], "x": 0, "y": 50, "isLeaf": True}
    ]
    edges = []
    return nodes, edges
```

### 5. Canvas (QML)
```qml
onTreeChanged: function(nodes, edges) {
    // Atualiza visualização com novos nós
    nodeRepeater.model = nodes
}

onEventsReady: function(events) {
    // Anima o nó que foi modificado
    var targetNode = findTargetNodeForHighlight(events)
    highlightNode(targetNode)
}
```

---

## 9. Pontos Técnicos Importantes

### Sistema de Eventos
O programa usa um sistema de eventos para coordenar animações:

```python
# Tipos de eventos gerados
{
    "type": "insert_root",    # Inserção na raiz
    "nodeId": "abc123",
    "key": 5
}

{
    "type": "insert_leaf",    # Inserção em folha
    "nodeId": "def456", 
    "key": 3,
    "position": 1
}

{
    "type": "split",          # Divisão de nó
    "nodeId": "ghi789",       # Nó original
    "newNodeId": "jkl012",    # Novo nó criado
    "promoted": 7             # Chave promovida
}
```

### Comunicação Python-QML
A comunicação usa o sistema de sinais do Qt:

```python
# Python → QML
class Bridge(QObject):
    treeChanged = Signal(list, list)  # Definição do sinal
    
    def _emit_tree_update(self):
        nodes, edges = layout(self._tree)
        self.treeChanged.emit(nodes, edges)  # Emissão
```

```qml
// QML recebe
Bridge {
    onTreeChanged: function(nodes, edges) {  // Receptor
        canvas.updateTree(nodes, edges)
    }
}
```

### Algoritmo da Árvore B
A implementação segue o algoritmo clássico:

1. **Inserção**: Sempre em folhas, divide quando necessário
2. **Divisão**: Pega chave do meio, sobe para pai
3. **Busca**: Desce pela árvore comparando chaves

### Cálculo de Layout
O posicionamento usa estratégia baseada em largura:

1. Calcula quantas "folhas" cada nó tem como descendentes
2. Dá espaço proporcional ao número de descendentes
3. Centraliza cada nível horizontalmente

---

## 10. Arquivos de Teste

### `tests/test_btree.py`
Contém testes automatizados para validar a implementação:

```python
def test_insertion_sequence():
    """Testa sequência específica que produz estrutura ideal."""
    tree = BTree(max_keys=2)
    
    # Insere 0,1,2,3,4,5,6,7,8,9
    for i in range(10):
        tree.insert(i)
    
    # Verifica estrutura final: [3] → [[1],[5,7]] → [[0],[2],[4],[6],[8,9]]
    assert tree.root.keys == [3]
    assert len(tree.root.children) == 2
    
    left_child = tree.root.children[0]
    assert left_child.keys == [1]
    
    right_child = tree.root.children[1] 
    assert right_child.keys == [5, 7]
```

---

## Resumo da Arquitetura

1. **main.py**: Inicia aplicação Qt/QML
2. **Bridge**: Conecta Python com QML via sinais
3. **BTree**: Implementa lógica da árvore B com eventos
4. **Layout**: Calcula posições para visualização
5. **main.qml**: Interface principal com controles
6. **TreeCanvas.qml**: Desenha e anima a árvore
7. **Node.qml/Line.qml**: Componentes visuais

O fluxo de dados é **unidirecional**: Interface → Bridge → Árvore → Layout → Bridge → Interface

A comunicação usa **sistema de eventos assíncronos**, permitindo animações fluidas e interface responsiva.