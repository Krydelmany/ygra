# ROADMAP — ygra

## Sprint 1 — Fundamentos (sem código funcional de UI ainda)
- [ ] Definir modelo `Node`/`Tree` (core) com add/remover/mover subárvore.
- [ ] Percursos: pré-ordem, pós-ordem, BFS.
- [ ] Métricas: altura, total de nós, folhas, grau máximo.
- [ ] IO: salvar/abrir JSON + validação básica (schema descritivo).
- [ ] Esqueleto da GUI (QML): janela, tema, canvas “placeholder” (sem lógica).

## Sprint 2 — GUI utilizável
- [ ] Layout Tidy (posições x/y) e desenho de nós/arestas.
- [ ] Seleção de nó + painel de propriedades (rótulo/nota).
- [ ] Ações básicas (adicionar filho, remover nó) com confirmações.
- [ ] Salvar/Abrir integrados à GUI.
- [ ] Testes unitários do core.

## Sprint 3 — Brilho e animações
- [ ] Busca animada (BFS/DFS com passo-a-passo e métricas).
- [ ] Expand/Collapse subárvore com transitions (opacity/scale/y).
- [ ] Tema claro/escuro com toggle animado.
- [ ] Exportar imagem (PNG) do canvas.

## Sprint 4 — Extras (competição)
- [ ] Drag & drop de subárvores com snapping e animação de paths.
- [ ] Estatísticas avançadas (ramificação média, histograma por nível).
- [ ] Undo/Redo simples (stack de comandos).
- [ ] Empacotar com PyInstaller (Windows/Linux).
