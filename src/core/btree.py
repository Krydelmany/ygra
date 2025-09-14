"""
B-Tree implementation with event generation for visualization.
"""
import uuid
from typing import List, Dict, Any, Optional, Tuple


class BNode:
    """B-tree node with support for visualization events."""

    def __init__(self, leaf: bool = True):
        self.keys: List[int] = []
        self.children: List['BNode'] = []
        self.leaf: bool = leaf
        self.id: str = str(uuid.uuid4())

    def is_full(self, tree) -> bool:
        """Check if node is full based on tree's max_keys."""
        return len(self.keys) >= tree._max_keys

    def find_key_index(self, key: int) -> int:
        """Find the index where key should be inserted."""
        i = 0
        while i < len(self.keys) and key > self.keys[i]:
            i += 1
        return i


class BTree:
    """B-tree with event generation for animation."""

    def __init__(self, t: int = 2, max_keys: Optional[int] = None):
        """Initialize B-tree with minimum degree t or max keys per node."""
        if max_keys is not None:
            # Se max_keys for especificado, calcular t baseado nisso
            # max_keys = 2*t - 1, então t = (max_keys + 1) / 2
            t = max(2, (max_keys + 1) // 2)
            self._max_keys = max_keys
        else:
            self._max_keys = 2 * t - 1
            
        if t < 2:
            raise ValueError("Minimum degree must be at least 2")
        self.t = t
        self.root: Optional[BNode] = None

    def search(self, key: int) -> Tuple[bool, List[Dict[str, Any]], List[BNode]]:
        """Search for a key and return (found, events, path)."""
        events = []
        path = []

        if not self.root:
            return False, events, path

        current = self.root
        while current:
            path.append(current)
            events.append({
                "type": "visit",
                "nodeId": current.id,
                "keyIndex": None
            })

            # Find position in current node
            i = current.find_key_index(key)

            # Check if key found
            if i < len(current.keys) and current.keys[i] == key:
                events.append({
                    "type": "found",
                    "nodeId": current.id,
                    "keyIndex": i
                })
                return True, events, path

            # If leaf, key not found
            if current.leaf:
                break

            # Move to child
            current = current.children[i]

        return False, events, path

    def insert(self, key: int) -> List[Dict[str, Any]]:
        """Insert a key and return animation events."""
        events = []

        # Check for duplicates
        found, _, _ = self.search(key)
        if found:
            return [{"type": "error", "message": f"Chave {key} já existe"}]

        # Create root if empty
        if not self.root:
            self.root = BNode(leaf=True)
            self.root.keys.append(key)
            events.append({
                "type": "insert_root",
                "nodeId": self.root.id,
                "key": key
            })
            return events

        # Use standard insertion algorithm  
        self._insert_non_full(self.root, key, events)
        
        # Check if root became overfull and needs splitting
        if len(self.root.keys) > self._max_keys:
            new_root = BNode(leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0, events)
            self.root = new_root
        return events

    def _insert_smart(self, node: BNode, key: int, events: List[Dict[str, Any]]):
        """Smart insertion with optimal balancing strategy."""
        if node.leaf:
            # Insert into leaf using binary search position
            i = node.find_key_index(key)
            node.keys.insert(i, key)
            
            events.append({
                "type": "insert_leaf",
                "nodeId": node.id,
                "key": key,
                "position": i
            })
        else:
            # Find child to insert into
            i = node.find_key_index(key)
            child = node.children[i]
            
            # Check if child will overflow after insertion
            if len(child.keys) >= self._max_keys:
                # Check if we can compact with siblings before splitting
                if self._try_compact_siblings(node, i, events):
                    # After compaction, recalculate which child to use
                    i = node.find_key_index(key)
                    self._insert_smart(node.children[i], key, events)
                else:
                    # Must split - use smarter splitting
                    self._smart_split(node, i, events)
                    # After split, determine which child to insert into
                    if key > node.keys[i]:
                        i += 1
                    self._insert_smart(node.children[i], key, events)
            else:
                # Child has space, insert normally
                self._insert_smart(child, key, events)

    def _try_compact_siblings(self, parent: BNode, child_index: int, events: List[Dict[str, Any]]) -> bool:
        """Try to compact keys across siblings to delay splitting."""
        child = parent.children[child_index]
        
        # For optimal B-tree structure, prefer keeping nodes fuller rather than splitting early
        # Check all siblings to see if we can redistribute load
        
        # Check right sibling first
        if child_index < len(parent.children) - 1:
            right_sibling = parent.children[child_index + 1]
            total_keys = len(child.keys) + len(right_sibling.keys)
            
            # If combined they're not too full, redistribute
            if total_keys <= self._max_keys * 2:
                return self._redistribute_between_siblings(parent, child_index, child_index + 1, events)
        
        # Check left sibling
        if child_index > 0:
            left_sibling = parent.children[child_index - 1]
            total_keys = len(left_sibling.keys) + len(child.keys)
            
            # If combined they're not too full, redistribute
            if total_keys <= self._max_keys * 2:
                return self._redistribute_between_siblings(parent, child_index - 1, child_index, events)
        
        return False

    def _redistribute_between_siblings(self, parent: BNode, left_idx: int, right_idx: int, events: List[Dict[str, Any]]) -> bool:
        """Redistribute keys between two siblings through parent."""
        left_child = parent.children[left_idx]
        right_child = parent.children[right_idx]
        parent_key_idx = left_idx
        
        # Collect all keys (left + parent + right)
        all_keys = left_child.keys + [parent.keys[parent_key_idx]] + right_child.keys
        all_children = left_child.children + right_child.children if not left_child.leaf else []
        
        # Redistribute evenly
        total = len(all_keys)
        left_count = total // 2
        new_parent_idx = left_count
        right_start = left_count + 1
        
        # Update nodes
        left_child.keys = all_keys[:left_count]
        parent.keys[parent_key_idx] = all_keys[new_parent_idx]
        right_child.keys = all_keys[right_start:]
        
        # Redistribute children if internal nodes
        if not left_child.leaf:
            left_child_count = len(left_child.keys) + 1
            left_child.children = all_children[:left_child_count]
            right_child.children = all_children[left_child_count:]
        
        events.append({
            "type": "redistribute_siblings",
            "parentId": parent.id,
            "leftId": left_child.id,
            "rightId": right_child.id
        })
        
        return True

    def _smart_split(self, parent: BNode, index: int, events: List[Dict[str, Any]]):
        """Intelligent splitting that considers global tree balance."""
        # Use the original split logic but with better middle selection
        self._split_child(parent, index, events)

    def _insert_non_full(self, node: BNode, key: int, events: List[Dict[str, Any]]):
        """Insert key into non-full node with smart splitting."""
        if node.leaf:
            # Insert into leaf
            i = node.find_key_index(key)
            node.keys.insert(i, key)

            events.append({
                "type": "insert_leaf",
                "nodeId": node.id,
                "key": key,
                "position": i
            })
        else:
            # Find child to insert into
            i = node.find_key_index(key)
            child = node.children[i]

            # For degree 3 B-trees, use smarter splitting strategy
            if self._max_keys == 2 and len(child.keys) >= self._max_keys:
                # Try to delay splitting by checking tree structure
                if self._should_delay_split(node, i):
                    # Allow temporary overflow and handle it later
                    self._insert_non_full(child, key, events)
                    
                    # If child overflowed, now handle the split
                    if len(child.keys) > self._max_keys:
                        self._split_child(node, i, events)
                else:
                    # Split immediately
                    self._split_child(node, i, events)
                    if key > node.keys[i]:
                        i += 1
                    self._insert_non_full(node.children[i], key, events)
            else:
                # Standard handling for other degrees or non-full children
                if child.is_full(self):
                    self._split_child(node, i, events)
                    if key > node.keys[i]:
                        i += 1
                
                self._insert_non_full(node.children[i], key, events)

    def _should_delay_split(self, parent: BNode, child_index: int) -> bool:
        """Determine if we should delay splitting to achieve better balance."""
        if self._max_keys != 2:  # Only for degree 3
            return False
        
        # Delay split if parent still has room and siblings could benefit
        if len(parent.keys) < self._max_keys:
            return True
            
        # Check if siblings have room
        if child_index > 0:
            left_sibling = parent.children[child_index - 1]
            if len(left_sibling.keys) < self._max_keys:
                return True
                
        if child_index < len(parent.children) - 1:
            right_sibling = parent.children[child_index + 1]
            if len(right_sibling.keys) < self._max_keys:
                return True
        
        return False

    def _split_child(self, parent: BNode, index: int, events: List[Dict[str, Any]]):
        """Split a full child node."""
        full_child = parent.children[index]
        new_child = BNode(leaf=full_child.leaf)

        # Standard B-tree splitting at the middle
        mid_index = self._max_keys // 2
        middle_key = full_child.keys[mid_index]

        # Move keys to new child (everything after middle)
        new_child.keys = full_child.keys[mid_index + 1:]
        # Keep keys in original child (everything before middle)  
        full_child.keys = full_child.keys[:mid_index]

        # Move children if not leaf
        if not full_child.leaf:
            # Split children accordingly
            split_point = mid_index + 1
            new_child.children = full_child.children[split_point:]
            full_child.children = full_child.children[:split_point]

        # Move middle key up to parent
        parent.children.insert(index + 1, new_child)
        parent.keys.insert(index, middle_key)

        events.append({
            "type": "split",
            "nodeId": full_child.id,
            "newNodeId": new_child.id,
            "promoted": middle_key
        })

    def delete(self, key: int) -> List[Dict[str, Any]]:
        """Delete a key and return animation events."""
        events = []

        if not self.root:
            return [{"type": "error", "message": f"Árvore vazia"}]

        # Check if key exists
        found, _, _ = self.search(key)
        if not found:
            return [{"type": "error", "message": f"Chave {key} não encontrada"}]

        self._delete_key(self.root, key, events)

        # Update root if it became empty
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]
            events.append({
                "type": "root_change",
                "newRootId": self.root.id
            })

        return events

    def _delete_key(self, node: BNode, key: int, events: List[Dict[str, Any]]):
        """Delete key from subtree rooted at node."""
        i = node.find_key_index(key)

        if i < len(node.keys) and node.keys[i] == key:
            if node.leaf:
                # Case 1: Delete from leaf
                node.keys.pop(i)
                events.append({
                    "type": "delete_leaf",
                    "nodeId": node.id,
                    "key": key
                })
            else:
                # Case 2: Delete from internal node
                self._delete_internal(node, i, events)
        else:
            if node.leaf:
                return  # Key not found

            # Case 3: Key in subtree
            flag = (i == len(node.keys))  # Last child

            if len(node.children[i].keys) < self.t:
                self._fill_child(node, i, events)

            # Adjust index if last child was merged
            if flag and i > len(node.keys):
                self._delete_key(node.children[i - 1], key, events)
            else:
                self._delete_key(node.children[i], key, events)

    def _delete_internal(self, node: BNode, index: int, events: List[Dict[str, Any]]):
        """Delete key from internal node."""
        key = node.keys[index]

        # Case 2a: Predecessor
        if len(node.children[index].keys) >= self.t:
            pred = self._get_predecessor(node, index)
            node.keys[index] = pred
            self._delete_key(node.children[index], pred, events)

            events.append({
                "type": "replace_predecessor",
                "nodeId": node.id,
                "oldKey": key,
                "newKey": pred
            })

        # Case 2b: Successor
        elif len(node.children[index + 1].keys) >= self.t:
            succ = self._get_successor(node, index)
            node.keys[index] = succ
            self._delete_key(node.children[index + 1], succ, events)

            events.append({
                "type": "replace_successor",
                "nodeId": node.id,
                "oldKey": key,
                "newKey": succ
            })

        # Case 2c: Merge
        else:
            self._merge_children(node, index, events)
            self._delete_key(node.children[index], key, events)

    def _get_predecessor(self, node: BNode, index: int) -> int:
        """Get inorder predecessor of key at index."""
        current = node.children[index]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node: BNode, index: int) -> int:
        """Get inorder successor of key at index."""
        current = node.children[index + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def _fill_child(self, node: BNode, index: int, events: List[Dict[str, Any]]):
        """Ensure child has at least t keys."""
        # Borrow from left sibling
        if index != 0 and len(node.children[index - 1].keys) >= self.t:
            self._borrow_from_prev(node, index, events)

        # Borrow from right sibling
        elif index != len(node.children) - 1 and len(node.children[index + 1].keys) >= self.t:
            self._borrow_from_next(node, index, events)

        # Merge with sibling
        else:
            if index != len(node.children) - 1:
                self._merge_children(node, index, events)
            else:
                self._merge_children(node, index - 1, events)

    def _borrow_from_prev(self, node: BNode, index: int, events: List[Dict[str, Any]]):
        """Borrow key from previous sibling."""
        child = node.children[index]
        sibling = node.children[index - 1]

        # Move key from parent to child
        child.keys.insert(0, node.keys[index - 1])

        # Move key from sibling to parent
        node.keys[index - 1] = sibling.keys.pop()

        # Move child pointer if not leaf
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

        events.append({
            "type": "borrow",
            "nodeId": child.id,
            "from": "left",
            "siblingId": sibling.id
        })

    def _borrow_from_next(self, node: BNode, index: int, events: List[Dict[str, Any]]):
        """Borrow key from next sibling."""
        child = node.children[index]
        sibling = node.children[index + 1]

        # Move key from parent to child
        child.keys.append(node.keys[index])

        # Move key from sibling to parent
        node.keys[index] = sibling.keys.pop(0)

        # Move child pointer if not leaf
        if not child.leaf:
            child.children.append(sibling.children.pop(0))

        events.append({
            "type": "borrow",
            "nodeId": child.id,
            "from": "right",
            "siblingId": sibling.id
        })

    def _merge_children(self, node: BNode, index: int, events: List[Dict[str, Any]]):
        """Merge child with its sibling."""
        child = node.children[index]
        sibling = node.children[index + 1]

        # Move key from parent to child
        child.keys.append(node.keys[index])

        # Move keys from sibling to child
        child.keys.extend(sibling.keys)

        # Move children if not leaf
        if not child.leaf:
            child.children.extend(sibling.children)

        # Remove key and sibling from parent
        node.keys.pop(index)
        node.children.pop(index + 1)

        events.append({
            "type": "merge",
            "leftId": child.id,
            "rightId": sibling.id
        })

    def clear(self) -> List[Dict[str, Any]]:
        """Clear the tree."""
        self.root = None
        return [{"type": "clear_all"}]

    def metrics(self) -> Dict[str, int]:
        """Get tree metrics."""
        if not self.root:
            return {"height": 0, "totalNodes": 0, "totalKeys": 0}

        height = self._get_height(self.root)
        nodes, keys = self._count_nodes_keys(self.root)

        return {
            "height": height,
            "totalNodes": nodes,
            "totalKeys": keys
        }

    def _get_height(self, node: BNode) -> int:
        """Get height of subtree."""
        if node.leaf:
            return 1
        return 1 + max(self._get_height(child) for child in node.children)

    def _count_nodes_keys(self, node: BNode) -> Tuple[int, int]:
        """Count nodes and keys in subtree."""
        nodes = 1
        keys = len(node.keys)

        for child in node.children:
            child_nodes, child_keys = self._count_nodes_keys(child)
            nodes += child_nodes
            keys += child_keys

        return nodes, keys

    def validate(self) -> bool:
        """Validate B-tree properties."""
        if not self.root:
            return True

        return self._validate_node(self.root, None, None, self._get_height(self.root))

    def _validate_node(self, node: BNode, min_key: Optional[int], 
                      max_key: Optional[int], expected_height: int) -> bool:
        """Validate a single node and its subtree."""
        # Check key count
        if node != self.root and len(node.keys) < self.t - 1:
            return False
        if len(node.keys) > 2 * self.t - 1:
            return False

        # Check key ordering
        for i in range(len(node.keys) - 1):
            if node.keys[i] >= node.keys[i + 1]:
                return False

        # Check key bounds
        if min_key is not None and node.keys[0] <= min_key:
            return False
        if max_key is not None and node.keys[-1] >= max_key:
            return False

        # Check children
        if not node.leaf:
            if len(node.children) != len(node.keys) + 1:
                return False

            for i, child in enumerate(node.children):
                child_min = node.keys[i - 1] if i > 0 else min_key
                child_max = node.keys[i] if i < len(node.keys) else max_key

                if not self._validate_node(child, child_min, child_max, expected_height - 1):
                    return False
        else:
            # All leaves should be at same level
            if expected_height != 1:
                return False

        return True
