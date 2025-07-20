class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []
        self.locked_by = None
        self.locked_descendant_count = 0
        # NEW: Set to track locked descendants for O(locked_nodes) access
        self.locked_descendants = set()

def build_tree(node_names, m):
    """Build m-ary tree from level-order node names"""
    nodes = {name: Node(name) for name in node_names}
    n = len(node_names)
    
    for i in range(n):
        parent = nodes[node_names[i]]
        for j in range(1, m + 1):
            child_idx = m * i + j
            if child_idx < n:
                child = nodes[node_names[child_idx]]
                parent.children.append(child)
                child.parent = parent
    
    return nodes

def can_lock(node):
    """Check if node can be locked - O(log N)"""
    # Check ancestors for locks
    curr = node.parent
    while curr:
        if curr.locked_by is not None:
            return False
        curr = curr.parent
    
    # Check descendants using counter - O(1)
    return node.locked_descendant_count == 0

def update_ancestors(node, delta, locked_node=None):
    """Update ancestor counts and locked_descendants sets - O(log N)"""
    curr = node.parent
    while curr:
        curr.locked_descendant_count += delta
        if locked_node:
            if delta > 0:
                curr.locked_descendants.add(locked_node)
            else:
                curr.locked_descendants.discard(locked_node)
        curr = curr.parent

def lock(node, uid):
    """Lock node - O(log N)"""
    if node.locked_by is not None:
        return False
    
    if not can_lock(node):
        return False
    
    node.locked_by = uid
    update_ancestors(node, 1, node)
    return True

def unlock(node, uid):
    """Unlock node - O(log N)"""
    if node.locked_by != uid:
        return False
    
    node.locked_by = None
    update_ancestors(node, -1, node)
    return True



def upgrade_lock(node, uid):
    """Upgrade lock - O(locked_nodes * log N)"""
    if node.locked_by is not None:
        return False
    
    # Check ancestors - O(log N)
    curr = node.parent
    while curr:
        if curr.locked_by is not None:
            return False
        curr = curr.parent
    
    # Get locked descendants - O(locked_nodes)
    locked_nodes = list(node.locked_descendants)
    
    if not locked_nodes:
        return False
    
    # Check all locked descendants belong to uid - O(locked_nodes)
    for locked_node in locked_nodes:
        if locked_node.locked_by != uid:
            return False
    
    # Unlock all descendants - O(locked_nodes * log N)
    for locked_node in locked_nodes:
        locked_node.locked_by = None
        update_ancestors(locked_node, -1, locked_node)
    
    # Lock this node - O(log N)
    node.locked_by = uid
    update_ancestors(node, 1, node)
    return True

def main():
    """Main function"""
    N = int(input())
    m = int(input())
    Q = int(input())
    
    node_names = [input().strip() for _ in range(N)]
    nodes = build_tree(node_names, m)
    
    for _ in range(Q):
        parts = input().strip().split()
        op_type = int(parts[0])
        node_name = parts[1]
        uid = int(parts[2])
        node = nodes[node_name]
        
        if op_type == 1:
            print(str(lock(node, uid)).lower())
        elif op_type == 2:
            print(str(unlock(node, uid)).lower())
        elif op_type == 3:
            print(str(upgrade_lock(node, uid)).lower())

if __name__ == "__main__":
    main()