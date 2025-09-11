# Estrutura QML (Bootstrap)

- `src/ygra/ui/main.qml`
  - `ApplicationWindow` com:
    - `ToolBar` (Novo/Abrir/Salvar/Exportar, busca, toggle de tema)
    - `Drawer` lateral (propriedades/ações/percursos — placeholders)
    - `StatusBar` (zoom/pos/dicas)
    - `CanvasView` (com zoom/pan e nós/arestas **mock**)
  - **Tema**: Material claro/escuro com persistência via `Settings`

- Componentes inline:
  - `CanvasView`: item com **grade**, **zoom/pan** e placeholders de nós/arestas
  - `NodeBubble`: cartão arredondado com sombra e hover
  - `EdgeCurve`: aresta curva com Bézier

> Próximo passo: substituir os **mock nodes** por um **modelo vindo do core** (Python) e ligar sinais/slots para ações reais.
