"""
Bridge between B-tree core and QML UI.
"""
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import qmlRegisterType
from typing import List, Dict, Any

from core.btree import BTree
from core.layout import layout


class Bridge(QObject):
    """Qt Bridge for B-tree visualization."""

    # Signals
    treeChanged = Signal(list, list)  # nodes, edges
    metricsChanged = Signal('QVariant')  # metrics dict
    eventsReady = Signal(list)  # animation events
    message = Signal(str, str)  # text, kind ("info", "error", "success")
    degreeChanged = Signal()  # signal for degree property

    def __init__(self, parent=None):
        super().__init__(parent)
        self._degree = 3  # Iniciar com grau 3 
        max_keys = self._degree - 1  # grau 3 = max 2 chaves
        self._tree = BTree(max_keys=max_keys)
        self._emit_tree_update()

    @Property(int, notify=degreeChanged)
    def degree(self):
        return self._degree

    @degree.setter
    def degree(self, value):
        if value != self._degree and value >= 2:
            self._degree = value
            # Grau na UI = máximo de chaves por nó + 1
            # grau 3 na UI = máximo 2 chaves por nó
            # grau 4 na UI = máximo 3 chaves por nó, etc.
            max_keys = value - 1
            self._tree = BTree(max_keys=max_keys)
            self._emit_tree_update()
            self.degreeChanged.emit()  # emit the signal when degree changes
            self.message.emit(f"Grau {value} → máx {max_keys} chaves por nó. Árvore reiniciada.", "info")

    @Slot(str)
    def insertKeys(self, text: str):
        """Insert keys from comma-separated string."""
        if not text.strip():
            self.message.emit("Digite as chaves para inserir", "error")
            return

        try:
            # Parse keys
            keys_str = text.replace(" ", "").split(",")
            keys = []
            for key_str in keys_str:
                if key_str.strip():
                    keys.append(int(key_str.strip()))

            if not keys:
                self.message.emit("Nenhuma chave válida encontrada", "error")
                return

            # Insert keys and collect events
            all_events = []
            inserted_count = 0

            for key in keys:
                events = self._tree.insert(key)
                
                if events and events[0].get("type") != "error":
                    all_events.extend(events)
                    inserted_count += 1
                else:
                    # Handle error
                    error_msg = events[0].get("message", f"Erro ao inserir {key}")
                    self.message.emit(error_msg, "error")

            if inserted_count > 0:
                self._emit_tree_update()
                if all_events:
                    self.eventsReady.emit(all_events)
                self.message.emit(f"{inserted_count} chave(s) inserida(s)", "success")

        except ValueError:
            self.message.emit("Formato inválido. Use números separados por vírgula", "error")
        except Exception as e:
            self.message.emit(f"Erro: {str(e)}", "error")

    @Slot(str)
    def deleteKeys(self, text: str):
        """Delete keys from comma-separated string."""
        if not text.strip():
            self.message.emit("Digite as chaves para remover", "error")
            return

        try:
            # Parse keys
            keys_str = text.replace(" ", "").split(",")
            keys = []
            for key_str in keys_str:
                if key_str.strip():
                    keys.append(int(key_str.strip()))

            if not keys:
                self.message.emit("Nenhuma chave válida encontrada", "error")
                return

            # Delete keys and collect events
            all_events = []
            deleted_count = 0

            for key in keys:
                events = self._tree.delete(key)
                
                if events and events[0].get("type") != "error":
                    all_events.extend(events)
                    deleted_count += 1
                else:
                    # Handle error
                    error_msg = events[0].get("message", f"Chave {key} não encontrada")
                    self.message.emit(error_msg, "error")

            if deleted_count > 0:
                self._emit_tree_update()
                if all_events:
                    self.eventsReady.emit(all_events)
                self.message.emit(f"{deleted_count} chave(s) removida(s)", "success")

        except ValueError:
            self.message.emit("Formato inválido. Use números separados por vírgula", "error")
        except Exception as e:
            self.message.emit(f"Erro: {str(e)}", "error")

    @Slot(int)
    def deleteKey(self, key: int):
        """Delete a single key."""
        try:
            events = self._tree.delete(key)

            if events and events[0].get("type") == "error":
                error_msg = events[0].get("message", f"Erro ao remover {key}")
                self.message.emit(error_msg, "error")
            else:
                self._emit_tree_update()
                if events:
                    self.eventsReady.emit(events)
                self.message.emit(f"Chave {key} removida", "success")

        except Exception as e:
            self.message.emit(f"Erro ao remover: {str(e)}", "error")

    @Slot(int)
    def searchKey(self, key: int):
        """Search for a key and emit animation events."""
        try:
            found, events, path = self._tree.search(key)

            if found:
                self.message.emit(f"Chave {key} encontrada", "success")
            else:
                self.message.emit(f"Chave {key} não encontrada", "info")

            if events:
                self.eventsReady.emit(events)

        except Exception as e:
            self.message.emit(f"Erro na busca: {str(e)}", "error")

    @Slot()
    def clearAll(self):
        """Clear the entire tree."""
        try:
            events = self._tree.clear()
            self._emit_tree_update()

            if events:
                self.eventsReady.emit(events)

            self.message.emit("Árvore limpa", "info")

        except Exception as e:
            self.message.emit(f"Erro ao limpar: {str(e)}", "error")

    @Slot(int)
    def setDegree(self, t: int):
        """Set the minimum degree of the tree."""
        if t < 2:
            self.message.emit("Grau mínimo deve ser pelo menos 2", "error")
            return

        if t != self._degree:
            self.degree = t

    @Slot()
    def loadExample(self):
        """Load example data into the tree."""
        try:
            # Clear first
            self._tree.clear()

            # Insert example keys
            example_keys = [10, 20, 5, 6, 12, 30, 7, 17]
            all_events = []

            for key in example_keys:
                events = self._tree.insert(key)
                if events and events[0].get("type") != "error":
                    all_events.extend(events)

            self._emit_tree_update()

            if all_events:
                self.eventsReady.emit(all_events)

            self.message.emit("Exemplo carregado", "success")

        except Exception as e:
            self.message.emit(f"Erro ao carregar exemplo: {str(e)}", "error")

    @Slot(str, result=bool)
    def validateClearText(self, text: str) -> bool:
        """Validate clear confirmation text."""
        return text.upper() == "CLEAR"

    def _emit_tree_update(self):
        """Emit tree structure and metrics updates."""
        try:
            nodes, edges = layout(self._tree)
            metrics = self._tree.metrics()

            self.treeChanged.emit(nodes, edges)
            self.metricsChanged.emit(metrics)

        except Exception as e:
            self.message.emit(f"Erro na atualização: {str(e)}", "error")


# Register the type for QML
def register_bridge():
    """Register Bridge type with QML."""
    qmlRegisterType(Bridge, "BTreeApp", 1, 0, "Bridge")
