#!/usr/bin/env python3
"""
Debug dos eventos de animação da B-tree.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.btree import BTree

def debug_animation_events():
    """Debug dos eventos gerados durante inserção sequencial."""
    
    print("🔍 DEBUG DOS EVENTOS DE ANIMAÇÃO")
    print("="*50)
    
    tree = BTree(max_keys=2)
    
    # Inserir 1, 2, 3 sequencialmente e ver os eventos
    for value in [1, 2, 3]:
        print(f"\n--- Inserindo {value} ---")
        events = tree.insert(value)
        
        print(f"Número de eventos: {len(events)}")
        for i, event in enumerate(events):
            print(f"  Evento {i+1}: {event}")
        
        # Mostrar estrutura atual
        print("Estrutura atual:")
        print_tree_simple(tree.root)

def print_tree_simple(node, level=0):
    """Imprime estrutura simples da árvore."""
    if node is None:
        return
    
    indent = "  " * level
    print(f"{indent}ID: {node.id[:8]}... Chaves: {node.keys}")
    
    if not node.leaf:
        for child in node.children:
            print_tree_simple(child, level + 1)

if __name__ == "__main__":
    debug_animation_events()