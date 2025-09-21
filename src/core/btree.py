import uuid
from typing import List, Dict, Any, Optional, Tuple


class BNode:

    def __init__(self, leaf: bool = True):
        self.keys: List[int] = []
        self.children: List['BNode'] = []
        self.leaf: bool = leaf
        self.id: str = str(uuid.uuid4())

    def is_full(self, tree) -> bool:
        return len(self.keys) >= tree._max_keys

    def find_key_index(self, key: int) -> int:
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        return i


class BTree:

    def __init__(self, t: int = 2, max_keys: Optional[int] = None):
        if max_keys is not None:
            t = max(2, (max_keys + 1) // 2)
            self._max_keys = max_keys
        else:
            self._max_keys = 2 * t - 1
            
        if t < 2:
            raise ValueError("O grau mínimo deve ser pelo menos 2")
        self._t = t
        self.root: Optional[BNode] = None

    def search(self, key: int) -> Tuple[bool, List[Dict[str, Any]], List[BNode]]:
        eventos = []
        caminho = []

        if not self.root:
            return False, eventos, caminho

        atual = self.root
        while atual:
            caminho.append(atual)
            eventos.append({
                "type": "visit",
                "nodeId": atual.id,
                "keyIndex": None
            })

            indice = atual.find_key_index(key)

            if indice < len(atual.keys) and atual.keys[indice] == key:
                eventos.append({
                    "type": "found",
                    "nodeId": atual.id,
                    "keyIndex": indice
                })
                return True, eventos, caminho

            if atual.leaf:
                break

            atual = atual.children[indice]

        return False, eventos, caminho

    def insert(self, key: int) -> List[Dict[str, Any]]:
        eventos = []

        encontrado, _, _ = self.search(key)
        if encontrado:
            return []

        if not self.root:
            self.root = BNode(leaf=True)
            self.root.keys.append(key)
            eventos.append({
                "type": "insert_root",
                "nodeId": self.root.id,
                "key": key
            })
            return eventos
        self._insert_non_full(self.root, key, eventos)
        
        if len(self.root.keys) > self._max_keys:
            nova_raiz = BNode(leaf=False)
            nova_raiz.children.append(self.root)
            self._split_child(nova_raiz, 0, eventos)
            self.root = nova_raiz
        return eventos

    def _insert_smart(self, no: BNode, chave: int, eventos: List[Dict[str, Any]]):
        if no.leaf:
            indice = no.find_key_index(chave)
            no.keys.insert(indice, chave)
            
            eventos.append({
                "type": "insert_leaf",
                "nodeId": no.id,
                "key": chave,
                "position": indice
            })
        else:
            indice = no.find_key_index(chave)
            filho = no.children[indice]
            
            if len(filho.keys) >= self._max_keys:
                if self._try_compact_siblings(no, indice, eventos):
                    indice = no.find_key_index(chave)
                    self._insert_smart(no.children[indice], chave, eventos)
                else:
                    self._smart_split(no, indice, eventos)
                    if chave > no.keys[indice]:
                        indice += 1
                    self._insert_smart(no.children[indice], chave, eventos)
            else:
                self._insert_smart(filho, chave, eventos)

    def _try_compact_siblings(self, pai: BNode, indice_filho: int, eventos: List[Dict[str, Any]]) -> bool:
        filho = pai.children[indice_filho]
        
        if indice_filho < len(pai.children) - 1:
            irmao_direito = pai.children[indice_filho + 1]
            total_chaves = len(filho.keys) + len(irmao_direito.keys)
            
            if total_chaves <= self._max_keys * 2:
                return self._redistribute_between_siblings(pai, indice_filho, indice_filho + 1, eventos)
        
        if indice_filho > 0:
            irmao_esquerdo = pai.children[indice_filho - 1]
            total_chaves = len(irmao_esquerdo.keys) + len(filho.keys)
            
            if total_chaves <= self._max_keys * 2:
                return self._redistribute_between_siblings(pai, indice_filho - 1, indice_filho, eventos)
        
        return False

    def _redistribute_between_siblings(self, pai: BNode, indice_esq: int, indice_dir: int, eventos: List[Dict[str, Any]]) -> bool:
        filho_esq = pai.children[indice_esq]
        filho_dir = pai.children[indice_dir]
        indice_chave_pai = indice_esq
        
        todas_chaves = filho_esq.keys + [pai.keys[indice_chave_pai]] + filho_dir.keys
        todos_filhos = filho_esq.children + filho_dir.children if not filho_esq.leaf else []
        
        total = len(todas_chaves)
        qtd_esq = total // 2
        novo_indice_pai = qtd_esq
        inicio_dir = qtd_esq + 1
        
        filho_esq.keys = todas_chaves[:qtd_esq]
        pai.keys[indice_chave_pai] = todas_chaves[novo_indice_pai]
        filho_dir.keys = todas_chaves[inicio_dir:]
        
        if not filho_esq.leaf:
            qtd_filhos_esq = len(filho_esq.keys) + 1
            filho_esq.children = todos_filhos[:qtd_filhos_esq]
            filho_dir.children = todos_filhos[qtd_filhos_esq:]
        
        eventos.append({
            "type": "redistribute_siblings",
            "parentId": pai.id,
            "leftId": filho_esq.id,
            "rightId": filho_dir.id
        })
        
        return True

    def _smart_split(self, pai: BNode, indice: int, eventos: List[Dict[str, Any]]):
        self._split_child(pai, indice, eventos)

    def _insert_non_full(self, no: BNode, chave: int, eventos: List[Dict[str, Any]]):
        if no.leaf:
            indice = no.find_key_index(chave)
            no.keys.insert(indice, chave)
            eventos.append({
                "type": "insert_leaf",
                "nodeId": no.id,
                "key": chave,
                "position": indice
            })
        else:
            indice = no.find_key_index(chave)
            filho = no.children[indice]
            if self._max_keys == 2 and len(filho.keys) >= self._max_keys:
                if self._should_delay_split(no, indice):
                    self._insert_non_full(filho, chave, eventos)
                    if len(filho.keys) > self._max_keys:
                        self._split_child(no, indice, eventos)
                else:
                    self._split_child(no, indice, eventos)
                    if chave > no.keys[indice]:
                        indice += 1
                    self._insert_non_full(no.children[indice], chave, eventos)
            else:
                if filho.is_full(self):
                    self._split_child(no, indice, eventos)
                    if chave > no.keys[indice]:
                        indice += 1
                self._insert_non_full(no.children[indice], chave, eventos)

    def _should_delay_split(self, pai: BNode, indice_filho: int) -> bool:
        if self._max_keys != 2:
            return False
        if len(pai.keys) < self._max_keys:
            return True
        if indice_filho > 0:
            irmao_esquerdo = pai.children[indice_filho - 1]
            if len(irmao_esquerdo.keys) < self._max_keys:
                return True
        if indice_filho < len(pai.children) - 1:
            irmao_direito = pai.children[indice_filho + 1]
            if len(irmao_direito.keys) < self._max_keys:
                return True
        return False

    def _split_child(self, pai: BNode, indice: int, eventos: List[Dict[str, Any]]):
        filho_cheio = pai.children[indice]
        novo_filho = BNode(leaf=filho_cheio.leaf)

        indice_meio = self._max_keys // 2
        chave_meio = filho_cheio.keys[indice_meio]

        novo_filho.keys = filho_cheio.keys[indice_meio + 1:]
        filho_cheio.keys = filho_cheio.keys[:indice_meio]

        if not filho_cheio.leaf:
            ponto_divisao = indice_meio + 1
            novo_filho.children = filho_cheio.children[ponto_divisao:]
            filho_cheio.children = filho_cheio.children[:ponto_divisao]

        pai.children.insert(indice + 1, novo_filho)
        pai.keys.insert(indice, chave_meio)

        eventos.append({
            "type": "split",
            "nodeId": filho_cheio.id,
            "newNodeId": novo_filho.id,
            "promoted": chave_meio
        })

    def delete(self, key: int) -> List[Dict[str, Any]]:
        eventos = []
        if not self.root:
            return []
        encontrado, _, _ = self.search(key)
        if not encontrado:
            return []
        self._delete_key(self.root, key, eventos)
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]
            eventos.append({
                "type": "root_change",
                "newRootId": self.root.id
            })
        return eventos

    def _delete_key(self, no: BNode, chave: int, eventos: List[Dict[str, Any]]):
        indice = no.find_key_index(chave)

        if indice < len(no.keys) and no.keys[indice] == chave:
            if no.leaf:
                no.keys.pop(indice)
                eventos.append({
                    "type": "delete_leaf",
                    "nodeId": no.id,
                    "key": chave
                })
            else:
                self._delete_internal(no, indice, eventos)
        else:
            if no.leaf:
                return

            eh_ultimo = (indice == len(no.keys))

            if len(no.children[indice].keys) < self.t:
                self._fill_child(no, indice, eventos)

            if eh_ultimo and indice > len(no.keys):
                self._delete_key(no.children[indice - 1], chave, eventos)
            else:
                self._delete_key(no.children[indice], chave, eventos)

    def _delete_internal(self, no: BNode, indice: int, eventos: List[Dict[str, Any]]):
        chave = no.keys[indice]

        if len(no.children[indice].keys) >= self.t:
            predecessor = self._get_predecessor(no, indice)
            no.keys[indice] = predecessor
            self._delete_key(no.children[indice], predecessor, eventos)

            eventos.append({
                "type": "replace_predecessor",
                "nodeId": no.id,
                "oldKey": chave,
                "newKey": predecessor
            })

        elif len(no.children[indice + 1].keys) >= self.t:
            sucessor = self._get_successor(no, indice)
            no.keys[indice] = sucessor
            self._delete_key(no.children[indice + 1], sucessor, eventos)

            eventos.append({
                "type": "replace_successor",
                "nodeId": no.id,
                "oldKey": chave,
                "newKey": sucessor
            })

        else:
            self._merge_children(no, indice, eventos)
            self._delete_key(no.children[indice], chave, eventos)

    def _get_predecessor(self, no: BNode, indice: int) -> int:
        atual = no.children[indice]
        while not atual.leaf:
            atual = atual.children[-1]
        return atual.keys[-1]

    def _get_successor(self, no: BNode, indice: int) -> int:
        atual = no.children[indice + 1]
        while not atual.leaf:
            atual = atual.children[0]
        return atual.keys[0]

    def _fill_child(self, no: BNode, indice: int, eventos: List[Dict[str, Any]]):
        if indice != 0 and len(no.children[indice - 1].keys) >= self.t:
            self._borrow_from_prev(no, indice, eventos)

        elif indice != len(no.children) - 1 and len(no.children[indice + 1].keys) >= self.t:
            self._borrow_from_next(no, indice, eventos)

        else:
            if indice != len(no.children) - 1:
                self._merge_children(no, indice, eventos)
            else:
                self._merge_children(no, indice - 1, eventos)

    def _borrow_from_prev(self, no: BNode, indice: int, eventos: List[Dict[str, Any]]):
        filho = no.children[indice]
        irmao = no.children[indice - 1]

        filho.keys.insert(0, no.keys[indice - 1])

        no.keys[indice - 1] = irmao.keys.pop()

        if not filho.leaf:
            filho.children.insert(0, irmao.children.pop())

        eventos.append({
            "type": "borrow",
            "nodeId": filho.id,
            "from": "left",
            "siblingId": irmao.id
        })

    def _borrow_from_next(self, no: BNode, indice: int, eventos: List[Dict[str, Any]]):
        filho = no.children[indice]
        irmao = no.children[indice + 1]

        filho.keys.append(no.keys[indice])

        no.keys[indice] = irmao.keys.pop(0)

        if not filho.leaf:
            filho.children.append(irmao.children.pop(0))

        eventos.append({
            "type": "borrow",
            "nodeId": filho.id,
            "from": "right",
            "siblingId": irmao.id
        })

    def _merge_children(self, no: BNode, indice: int, eventos: List[Dict[str, Any]]):
        filho = no.children[indice]
        irmao = no.children[indice + 1]

        filho.keys.append(no.keys[indice])

        filho.keys.extend(irmao.keys)

        if not filho.leaf:
            filho.children.extend(irmao.children)

        no.keys.pop(indice)
        no.children.pop(indice + 1)

        eventos.append({
            "type": "merge",
            "leftId": filho.id,
            "rightId": irmao.id
        })

    def clear(self) -> List[Dict[str, Any]]:
        self.root = None
        return [{"type": "clear_all"}]

    def metrics(self) -> Dict[str, int]:
        if not self.root:
            return {"height": 0, "totalNodes": 0, "totalKeys": 0}

        altura = self._get_height(self.root)
        nos, chaves = self._count_nodes_keys(self.root)

        return {
            "height": altura,
            "totalNodes": nos,
            "totalKeys": chaves
        }

    def _get_height(self, no: BNode) -> int:
        if no.leaf:
            return 1
        return 1 + max(self._get_height(filho) for filho in no.children)

    def _count_nodes_keys(self, no: BNode) -> Tuple[int, int]:
        nos = 1
        chaves = len(no.keys)

        for filho in no.children:
            nos_filho, chaves_filho = self._count_nodes_keys(filho)
            nos += nos_filho
            chaves += chaves_filho

        return nos, chaves

    def validate(self) -> bool:
        if not self.root:
            return True

        return self._validate_node(self.root, None, None, self._get_height(self.root))

    def _validate_node(self, no: BNode, chave_min: Optional[int], 
                      chave_max: Optional[int], altura_esperada: int) -> bool:
        if no != self.root and len(no.keys) < self.t - 1:
            return False
        if len(no.keys) > 2 * self.t - 1:
            return False

        for i in range(len(no.keys) - 1):
            if no.keys[i] >= no.keys[i + 1]:
                return False

        if chave_min is not None and no.keys[0] <= chave_min:
            return False
        if chave_max is not None and no.keys[-1] >= chave_max:
            return False

        if not no.leaf:
            if len(no.children) != len(no.keys) + 1:
                return False

            for i, filho in enumerate(no.children):
                filho_min = no.keys[i - 1] if i > 0 else chave_min
                filho_max = no.keys[i] if i < len(no.keys) else chave_max

                if not self._validate_node(filho, filho_min, filho_max, altura_esperada - 1):
                    return False
        else:
            if altura_esperada != 1:
                return False

        return True
