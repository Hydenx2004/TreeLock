import threading

class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []
        self.locked_by = None
        # Set to track locked descendants for O(1) count and O(locked_nodes) access
        self.locked_descendants = set()
        # Thread safety: Each node has its own lock
        self._lock = threading.RLock()
        # Unique identifier for consistent ordering to prevent deadlocks
        self._id = id(self)

def acquire_multiple_locks(nodes):
    """
    Acquire locks on multiple nodes in a consistent order to prevent deadlocks.
    Sorts nodes by their memory id to ensure consistent locking order.
    Returns list of acquired locks for proper cleanup.
    """
    if not nodes:
        return []
    
    # Sort by node id to ensure consistent ordering across threads
    sorted_nodes = sorted(nodes, key=lambda n: n._id)
    acquired_locks = []
    
    try:
        for node in sorted_nodes:
            node._lock.acquire()
            acquired_locks.append(node._lock)
        return acquired_locks
    except:
        # If any lock acquisition fails, release all acquired locks
        for lock in acquired_locks:
            lock.release()
        raise

def release_multiple_locks(locks):
    """Release multiple locks in reverse order"""
    for lock in reversed(locks):
        lock.release()

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
    """Check if node can be locked - O(log N) - Thread Safe"""
    with node._lock:
        # Check descendants using set length - O(1)
        if len(node.locked_descendants) > 0:
            return False
    
    # Check ancestors for locks - need to acquire locks in order
    ancestors = []
    curr = node.parent
    while curr:
        ancestors.append(curr)
        curr = curr.parent
    
    if not ancestors:
        return True
    
    # Acquire locks on all ancestors in consistent order
    locks = acquire_multiple_locks(ancestors)
    try:
        for ancestor in ancestors:
            if ancestor.locked_by is not None:
                return False
        return True
    finally:
        release_multiple_locks(locks)

def update_ancestors(node, is_locking):
    """Update ancestor locked_descendants sets when node is locked/unlocked - O(log N) - Thread Safe"""
    ancestors = []
    curr = node.parent
    while curr:
        ancestors.append(curr)
        curr = curr.parent
    
    if not ancestors:
        return
    
    # Acquire locks on all ancestors in consistent order
    locks = acquire_multiple_locks(ancestors)
    try:
        for ancestor in ancestors:
            if is_locking:
                ancestor.locked_descendants.add(node)
            else:
                ancestor.locked_descendants.discard(node)
    finally:
        release_multiple_locks(locks)

def lock(node, uid):
    """Lock node - O(log N) - Thread Safe"""
    with node._lock:
        if node.locked_by is not None:
            return False
    
    if not can_lock(node):
        return False
    
    with node._lock:
        # Double-check after acquiring lock (another thread might have locked it)
        if node.locked_by is not None:
            return False
        
        node.locked_by = uid
    
    update_ancestors(node, True)  # True = locking
    return True

def unlock(node, uid):
    """Unlock node - O(log N) - Thread Safe"""
    with node._lock:
        if node.locked_by != uid:
            return False
        
        node.locked_by = None
    
    update_ancestors(node, False)  # False = unlocking
    return True



def upgrade_lock(node, uid):
    """Upgrade lock - O(locked_nodes * log N) - Thread Safe"""
    with node._lock:
        if node.locked_by is not None:
            return False
    
    # Check ancestors - need to collect them first and then lock in order
    ancestors = []
    curr = node.parent
    while curr:
        ancestors.append(curr)
        curr = curr.parent
    
    if ancestors:
        # Acquire locks on all ancestors in consistent order
        ancestor_locks = acquire_multiple_locks(ancestors)
        try:
            for ancestor in ancestors:
                if ancestor.locked_by is not None:
                    return False
        finally:
            release_multiple_locks(ancestor_locks)
    
    # Get locked descendants - need to lock node first to read safely
    with node._lock:
        locked_nodes = list(node.locked_descendants)
    
    if not locked_nodes:
        return False
    
    # Acquire locks on all locked descendants in consistent order
    descendant_locks = acquire_multiple_locks(locked_nodes)
    try:
        # Check all locked descendants belong to uid
        for locked_node in locked_nodes:
            if locked_node.locked_by != uid:
                return False
        
        # Unlock all descendants
        for locked_node in locked_nodes:
            locked_node.locked_by = None
            update_ancestors(locked_node, False)  # False = unlocking
        
        # Lock this node
        with node._lock:
            # Double-check node is still unlocked
            if node.locked_by is not None:
                return False
            node.locked_by = uid
        
        update_ancestors(node, True)  # True = locking
        return True
        
    finally:
        release_multiple_locks(descendant_locks)

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


