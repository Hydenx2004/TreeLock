class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []
        self.locked_by = None  # None if unlocked, else user id
        self.locked_descendant_count = 0  # For efficient descendant lock checking

def build_tree(node_names, m):
    """Build m-ary tree from level-order node names"""
    nodes = {name: Node(name) for name in node_names}
    n = len(node_names)
    
    # Build parent-child relationships for m-ary tree
    for i in range(n):
        parent = nodes[node_names[i]]
        # For m-ary tree, node at index i has children at indices m*i+1 to m*i+m
        for j in range(1, m + 1):
            child_idx = m * i + j
            if child_idx < n:
                child = nodes[node_names[child_idx]]
                parent.children.append(child)
                child.parent = parent
    
    return nodes

def can_lock(node):
    """Check if node can be locked (no ancestors or descendants locked)"""
    # Check ancestors for locks
    curr = node.parent
    while curr:
        if curr.locked_by is not None:
            return False
        curr = curr.parent
    
    # Check descendants using the counter (O(1) instead of O(subtree size))
    return node.locked_descendant_count == 0

def update_ancestors(node, delta):
    """Update locked_descendant_count for all ancestors by delta"""
    curr = node.parent
    while curr:
        curr.locked_descendant_count += delta
        curr = curr.parent

def lock(node, uid):
    """Lock node for user uid"""
    # Already locked
    if node.locked_by is not None:
        return False
    
    # Check if locking is allowed
    if not can_lock(node):
        return False
    
    # Lock the node
    node.locked_by = uid
    update_ancestors(node, 1)  # Increment ancestor counts
    return True

def unlock(node, uid):
    """Unlock node if locked by same user"""
    # Wrong user or not locked
    if node.locked_by != uid:
        return False
    
    # Unlock
    node.locked_by = None
    update_ancestors(node, -1)  # Decrement ancestor counts
    return True

def collect_locked_descendants(node, locked_nodes):
    """Recursively collect all locked descendants"""
    if node.locked_by is not None:
        locked_nodes.append(node)
    
    for child in node.children:
        collect_locked_descendants(child, locked_nodes)

def upgrade_lock(node, uid):
    """Upgrade lock: unlock all descendants and lock this node"""
    # Already locked
    if node.locked_by is not None:
        return False
    
    # Check if any ancestors are locked
    curr = node.parent
    while curr:
        if curr.locked_by is not None:
            return False
        curr = curr.parent
    
    # Collect all locked descendants
    locked_nodes = []
    collect_locked_descendants(node, locked_nodes)
    
    # Must have at least one locked descendant
    if not locked_nodes:
        return False
    
    # All locked descendants must be locked by the same user (uid)
    for ln in locked_nodes:
        if ln.locked_by != uid:
            return False
    
    # All conditions met - perform upgrade
    # Unlock all locked descendants
    for ln in locked_nodes:
        ln.locked_by = None
        update_ancestors(ln, -1)
    
    # Lock this node
    node.locked_by = uid
    update_ancestors(node, 1)
    return True

def main():
    """Main function to handle input and process queries"""
    N = int(input())
    m = int(input())
    Q = int(input())
    
    # Read node names in level-order
    node_names = [input().strip() for _ in range(N)]
    nodes = build_tree(node_names, m)
    
    # Process queries
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