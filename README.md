# Visualizador de Árvore B

**Implementação de Árvore Múltipla com Interface Gráfica**

Este projeto demonstra uma **árvore B** (árvore múltipla) onde cada nó pode ter vários filhos, diferente das árvores binárias tradicionais. A aplicação permite visualizar e manipular a estrutura em tempo real através de uma interface gráfica moderna.

## O que é uma Árvore B?

Uma **árvore B** é uma estrutura de dados que permite que cada nó tenha múltiplos filhos (não apenas 2 como nas árvores binárias). Principais características:

- 📊 **Múltiplos filhos**: Cada nó pode ter de 2 até 2*grau filhos
- ⚖️ **Autobalanceamento**: Mantém todas as folhas na mesma altura
- 🔍 **Busca eficiente**: Operações em O(log n)
- 💾 **Uso prático**: Bancos de dados, sistemas de arquivos

## Funcionalidades do Programa

- 🖥️ **Interface interativa** para inserir, remover e buscar números
- 🎬 **Animações** que mostram onde cada operação acontece
- 🔧 **Grau configurável** (padrão: 3, ou seja, máximo 2 números por nó)
- 📈 **Métricas em tempo real** (altura, número de nós, etc.)
- 🖱️ **Navegação** com zoom e pan usando o mouse
├── requirements-dev.txt  # Dependências de desenvolvimento
├── test_structure.py     # Teste de verificação
└── README.md            # Documentação

```

## Como Instalar e Executar

### Requisitos
- **Python 3.12.3** (recomendado)
- Windows, macOS ou Linux

### Instalação Passo a Passo

1. **Navegue para o projeto**:
```bash
cd btree-visualizer
```

2. **Crie um ambiente virtual**:
```bash
python -m venv .venv
```

3. **Ative o ambiente virtual**:
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux  
source .venv/bin/activate
```

4. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

5. **Execute o programa**:
```bash
python main.py
```

6. **Teste se funcionou** (opcional):
```bash
python test_structure.py
```

## Como Usar o Programa

### Operações Básicas

**Inserir números**: Digite números separados por vírgula (ex: `1,2,3,4,5`) e clique em "Inserir"

**Buscar**: Digite um número e clique "Buscar" - o programa mostrará o caminho percorrido

**Remover**: Digite um número e clique "Remover" 

**Configurar grau**: Mude o valor do grau (ex: grau 3 = máximo 2 números por nó)

### Navegação
- **Roda do mouse**: Zoom in/out
- **Espaço + arrastar**: Mover a visualização
- **Duplo clique**: Centralizar em um nó

### Exemplo Prático

Para ver como funciona:
1. Configure grau = 3
2. Insira os números: `0,1,2,3,4,5,6,7,8,9`
3. Observe a estrutura final:

```
        [3]
      /     \
    [1]     [5,7]  
   /  \     / | \
 [0] [2]  [4][6][8,9]
```

Esta é a estrutura **ideal** de uma árvore B com grau 3!

## Estrutura do Código

O projeto está organizado de forma simples:

```
btree-visualizer/
├── main.py              # Arquivo principal - inicia o programa
├── requirements.txt     # Lista das bibliotecas necessárias
├── src/
│   ├── core/
│   │   ├── btree.py     # Lógica da árvore B
│   │   └── layout.py    # Calcula onde desenhar cada nó
│   ├── app/
│   │   └── bridge.py    # Conecta Python com a interface
│   └── ui/
│       ├── main.qml     # Interface principal
│       ├── TreeCanvas.qml  # Área onde a árvore é desenhada
│       ├── Node.qml     # Como cada nó aparece
│       └── ...outros arquivos da interface
└── tests/
    └── test_btree.py    # Testes para verificar se está funcionando
```

## Tecnologias Usadas

- **Python 3.12.3**: Linguagem principal
- **PySide6**: Biblioteca para criar a interface gráfica
- **QML**: Linguagem para desenhar a interface
- **Pytest**: Para executar os testes

## Para Desenvolvedores

### Executar os testes
```bash
python -m pytest tests/ -v
```

### Arquivos importantes
- `src/core/btree.py`: Contém toda a lógica da árvore B
- `src/ui/main.qml`: Interface principal do programa
- `src/app/bridge.py`: Faz a comunicação entre Python e interface

### Como funciona
1. O usuário interage com a interface (QML)
2. A interface chama funções no `bridge.py`
3. O bridge chama as operações da árvore B no `btree.py`
4. A árvore é atualizada e redesenhada na tela

---

**Projeto desenvolvido para fins educacionais - demonstração de estruturas de dados**
