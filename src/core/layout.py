from typing import List, Dict, Any, Tuple
from .btree import BTree, BNode


def layout(arvore: BTree) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    if not arvore.root:
        return [], []

    nos = []
    arestas = []

    niveis = _build_level_data(arvore.root)
    _assign_positions(niveis, nos, arestas)

    return nos, arestas


def _build_level_data(raiz: BNode) -> List[List[BNode]]:
    niveis = []
    fila = [raiz]

    while fila:
        tamanho_nivel = len(fila)
        nivel_atual = []

        for _ in range(tamanho_nivel):
            no = fila.pop(0)
            nivel_atual.append(no)

            for filho in no.children:
                fila.append(filho)

        niveis.append(nivel_atual)

    return niveis


def _assign_positions(niveis: List[List[BNode]], 
                     nos: List[Dict[str, Any]], 
                     arestas: List[Dict[str, Any]]):
    ALTURA_NIVEL = 120
    ESPACAMENTO_MIN_NO = 150 

    larguras_subarvores = _calculate_subtree_widths(niveis)

    for indice_nivel, nivel in enumerate(niveis):
        y = indice_nivel * ALTURA_NIVEL + 50 

        largura_total = 0
        for no in nivel:
            largura = max(larguras_subarvores[no.id] * ESPACAMENTO_MIN_NO, ESPACAMENTO_MIN_NO)
            largura_total += largura

        inicio_x = -largura_total / 2
        x_atual = inicio_x

        for no in nivel:
            largura_no = max(larguras_subarvores[no.id] * ESPACAMENTO_MIN_NO, ESPACAMENTO_MIN_NO)
            x = x_atual + largura_no / 2

            nos.append({
                "id": no.id,
                "keys": no.keys.copy(),
                "x": x,
                "y": y,
                "isLeaf": no.leaf
            })

            x_atual += largura_no

    _create_edges(niveis, arestas)


def _calculate_subtree_widths(niveis: List[List[BNode]]) -> Dict[str, int]:
    larguras = {}

    for nivel in reversed(niveis):
        for no in nivel:
            if no.leaf:
                larguras[no.id] = 1
            else:
                largura_total = sum(larguras[filho.id] for filho in no.children)
                larguras[no.id] = max(largura_total, 1)

    return larguras


def _create_edges(niveis: List[List[BNode]], arestas: List[Dict[str, Any]]):
    for nivel in niveis:
        for no in nivel:
            for filho in no.children:
                arestas.append({
                    "fromId": no.id,
                    "toId": filho.id
                })


def get_node_bounds(nos: List[Dict[str, Any]]) -> Dict[str, float]:
    if not nos:
        return {"minX": 0, "maxX": 0, "minY": 0, "maxY": 0}

    coordenadas_x = [no["x"] for no in nos]
    coordenadas_y = [no["y"] for no in nos]

    return {
        "minX": min(coordenadas_x) - 100,
        "maxX": max(coordenadas_x) + 100,
        "minY": min(coordenadas_y) - 50,
        "maxY": max(coordenadas_y) + 100
    }
