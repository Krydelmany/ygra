# ygra — Árvores Múltiplas com UI (PySide6 + Qt Quick)

> Linguagem: **Python 3.12.3** (compatível). GUI: **PySide6 + Qt Quick/QML**.

## Objetivo
- Implementar uma **árvore múltipla** (cada nó pode ter 0..N filhos).
- Visualizar e manipular a árvore em **interface gráfica** (zoom/pan/tema).

## Stack
- **Runtime**: PySide6 (Qt 6) + Qt Quick Controls 2 (tema Material/Universal)
- **Qualidade**: pytest, black, ruff, mypy, pre-commit
- **Empacote**: pyinstaller (fase posterior)

## Como rodar (Linux/macOS)
```bash
# Requer Python 3.12.x instalado
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
# (Futuramente) python -m ygra  # entrypoint da aplicação
```

## Como rodar (Windows PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
# (Futuramente) python -m ygra
```

## Estrutura de pastas
```
ygra/
├─ src/ygra/
│  ├─ core/      # domínio (árvore, nós, percursos, métricas)
│  ├─ io/        # json, schema, import/export
│  ├─ app/       # serviços/uso, undo/redo, validações
│  ├─ ui/        # interface gráfica (QML), assets
│  └─ utils/     # helpers gerais
├─ tests/        # pytest (core, io, app)
├─ docs/         # manual, roadmap, schema json, prints
├─ assets/       # ícones, logos, imagens
├─ scripts/      # scripts de setup e build
├─ requirements.txt
├─ requirements-dev.txt
├─ pyproject.toml
├─ .pre-commit-config.yaml
├─ .gitignore
└─ README.md
```

## Roadmap (resumido)
- **Sprint 1**: Core (estrutura de dados), IO (JSON), esqueleto da GUI
- **Sprint 2**: Desenho no canvas + interações básicas
- **Sprint 3**: Animações de percursos + métricas em tempo real
- **Sprint 4**: Drag & drop, exportar imagem (PNG/SVG), executável

## Licença
MIT © 2025

## Como executar a janela QML (bootstrap)
Depois de instalar as dependências e ativar o venv:
```bash
python -m ygra
```
Você verá:
- Janela principal com barra de ferramentas
- Painel lateral (placeholders)
- Canvas com **zoom/pan** e **nós mock**
