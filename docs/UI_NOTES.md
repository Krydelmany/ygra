# UI/UX — Notas de design

- **Tema**: Material (Qt Quick Controls 2), com claro/escuro.
- **Nós**: círculos/retângulos arredondados com sombra difusa.
- **Arestas**: curvas de Bézier (suaves).
- **Interações**:
  - Zoom (wheel) e Pan (arrastar canvas).
  - Hover/seleção com microanimações.
  - Atalhos: N (novo filho), Del (remover), Ctrl+S (salvar), Ctrl+F (buscar).
- **Animações**:
  - Busca: sequência com highlight temporizado.
  - Expand/Collapse: `opacity + scale + y` com easing suave.
  - Salvar: microanimação (Lottie) no botão.
