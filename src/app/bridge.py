from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import qmlRegisterType
from typing import List, Dict, Any

from core.btree import BTree
from core.layout import layout


class Bridge(QObject):

    treeChanged = Signal(list, list)
    metricsChanged = Signal(dict)
    eventsReady = Signal(list)
    message = Signal(str, str)
    degreeChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._grau = 3
        chaves_maximas = self._grau - 1
        self._arvore = BTree(max_keys=chaves_maximas)
        self._emit_tree_update()

    @Property(int, notify=degreeChanged)
    def degree(self):
        return self._grau

    @degree.setter
    def degree(self, valor):
        if valor != self._grau and valor >= 2:
            self._grau = valor
            chaves_maximas = valor - 1
            self._arvore = BTree(max_keys=chaves_maximas)
            self._emit_tree_update()
            self.degreeChanged.emit()
            self.message.emit(f"Grau {valor} → máx {chaves_maximas} chaves por nó. Arvore reiniciada.", "info")

    @Slot(str)
    def insertKeys(self, texto: str):
        if not texto.strip():
            self.message.emit("Digite as chaves para inserir", "error")
            return

        try:
            chaves_str = texto.replace(" ", "").split(",")
            chaves = []
            for chave_str in chaves_str:
                if chave_str.strip():
                    chaves.append(int(chave_str.strip()))

            if not chaves:
                self.message.emit("Nenhuma chave valida encontrada", "error")
                return

            todos_eventos = []
            contador_inseridas = 0

            for chave in chaves:
                eventos = self._arvore.insert(chave)
                
                if eventos and eventos[0].get("type") != "error":
                    todos_eventos.extend(eventos)
                    contador_inseridas += 1
                else:
                    mensagem_erro = eventos[0].get("message", f"Erro ao inserir {chave}")
                    self.message.emit(mensagem_erro, "error")

            if contador_inseridas > 0:
                self._emit_tree_update()
                if todos_eventos:
                    self.eventsReady.emit(todos_eventos)
                self.message.emit(f"{contador_inseridas} chave(s) inserida(s)", "success")

        except ValueError:
            self.message.emit("Formato inválido. Use números separados por vírgula", "error")
        except Exception as e:
            self.message.emit(f"Erro: {str(e)}", "error")

    @Slot(str)
    def deleteKeys(self, texto: str):
        if not texto.strip():
            self.message.emit("Digite as chaves para remover", "error")
            return

        try:
            chaves_str = texto.replace(" ", "").split(",")
            chaves = []
            for chave_str in chaves_str:
                if chave_str.strip():
                    chaves.append(int(chave_str.strip()))

            if not chaves:
                self.message.emit("Nenhuma chave válida encontrada", "error")
                return

            todos_eventos = []
            contador_removidas = 0

            for chave in chaves:
                eventos = self._arvore.delete(chave)
                
                if eventos and eventos[0].get("type") != "error":
                    todos_eventos.extend(eventos)
                    contador_removidas += 1
                else:
                    mensagem_erro = eventos[0].get("message", f"Chave {chave} não encontrada")
                    self.message.emit(mensagem_erro, "error")

            if contador_removidas > 0:
                self._emit_tree_update()
                if todos_eventos:
                    self.eventsReady.emit(todos_eventos)
                self.message.emit(f"{contador_removidas} chave(s) removida(s)", "success")

        except ValueError:
            self.message.emit("Formato inválido. Use números separados por vírgula", "error")
        except Exception as e:
            self.message.emit(f"Erro: {str(e)}", "error")

    @Slot(int)
    def deleteKey(self, chave: int):
        try:
            eventos = self._arvore.delete(chave)

            if eventos and eventos[0].get("type") == "error":
                mensagem_erro = eventos[0].get("message", f"Erro ao remover {chave}")
                self.message.emit(mensagem_erro, "error")
            else:
                self._emit_tree_update()
                if eventos:
                    self.eventsReady.emit(eventos)
                self.message.emit(f"Chave {chave} removida", "success")

        except Exception as e:
            self.message.emit(f"Erro ao remover: {str(e)}", "error")

    @Slot(int)
    def searchKey(self, chave: int):
        try:
            encontrou, eventos, caminho = self._arvore.search(chave)

            if encontrou:
                self.message.emit(f"Chave {chave} encontrada", "success")
            else:
                self.message.emit(f"Chave {chave} não encontrada", "info")

            if eventos:
                self.eventsReady.emit(eventos)

        except Exception as e:
            self.message.emit(f"Erro na busca: {str(e)}", "error")

    @Slot()
    def clearAll(self):
        try:
            eventos = self._arvore.clear()
            self._emit_tree_update()

            if eventos:
                self.eventsReady.emit(eventos)

            self.message.emit("Árvore limpa", "info")

        except Exception as e:
            self.message.emit(f"Erro ao limpar: {str(e)}", "error")

    @Slot(int)
    def setDegree(self, t: int):
        if t < 2:
            self.message.emit("Grau mínimo deve ser pelo menos 2", "error")
            return

        if t != self._grau:
            self.degree = t

    @Slot()
    def loadExample(self):
        try:
            self._arvore.clear()

            chaves_exemplo = [10, 20, 5, 6, 12, 30, 7, 17]
            todos_eventos = []

            for chave in chaves_exemplo:
                eventos = self._arvore.insert(chave)
                if eventos and eventos[0].get("type") != "error":
                    todos_eventos.extend(eventos)

            self._emit_tree_update()

            if todos_eventos:
                self.eventsReady.emit(todos_eventos)

            self.message.emit("Exemplo carregado", "success")

        except Exception as e:
            self.message.emit(f"Erro ao carregar exemplo: {str(e)}", "error")

    @Slot(str, result=bool)
    def validateClearText(self, texto: str) -> bool:
        return texto.upper() == "CLEAR"

    def _emit_tree_update(self):
        try:
            nos, arestas = layout(self._arvore)
            metricas = self._arvore.metrics()

            self.treeChanged.emit(nos, arestas)
            self.metricsChanged.emit(metricas)

        except Exception as e:
            self.message.emit(f"Erro na atualização: {str(e)}", "error")


def register_bridge():
    qmlRegisterType(Bridge, "BTreeApp", 1, 0, "Bridge")
