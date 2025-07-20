import threading
import time
import random
from Test import build_tree, lock as tree_lock, unlock as tree_unlock, upgrade_lock as tree_upgrade

def test_concurrent_operations():
    """Test concurrent lock operations on the same tree"""
    
    # Create a simple tree: World -> Asia, Africa -> India, China, Egypt, SouthAfrica  
    node_names = ["World", "Asia", "Africa", "China", "India", "SouthAfrica", "Egypt"]
    nodes = build_tree(node_names, 2)
    
    results = []
    results_lock = threading.Lock()
    
    def worker(thread_id, operations):
        """Worker function that performs lock operations"""
        thread_results = []
        for op_type, node_name, uid in operations:
            node = nodes[node_name]
            
            if op_type == 1:  # lock
                result = tree_lock(node, uid)
                thread_results.append(f"Thread {thread_id}: Lock {node_name} by {uid} -> {result}")
            elif op_type == 2:  # unlock  
                result = tree_unlock(node, uid)
                thread_results.append(f"Thread {thread_id}: Unlock {node_name} by {uid} -> {result}")
            elif op_type == 3:  # upgrade
                result = tree_upgrade(node, uid)
                thread_results.append(f"Thread {thread_id}: Upgrade {node_name} by {uid} -> {result}")
            
            # Small random delay to increase chance of race conditions
            with results_lock:
                results.extend(thread_results)
            time.sleep(random.uniform(0.001, 0.01))
        
    
    # Define operations for different threads
    operations_set = [
        [(1, "India", 1), (1, "China", 1), (2, "India", 1)],  # Thread 1
        [(1, "Egypt", 2), (1, "SouthAfrica", 2), (2, "Egypt", 2)],  # Thread 2  
        [(1, "Africa", 3), (2, "Africa", 3)],  # Thread 3
        [(1, "Asia", 4), (2, "Asia", 4)],  # Thread 4
        [(1, "India", 5), (1, "China", 5), (3, "Asia", 5)]  # Thread 5 - try upgrade
    ]
    
    # Create and start threads
    threads = []
    for i, operations in enumerate(operations_set):
        thread = threading.Thread(target=worker, args=(i+1, operations))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Print results
    print("Concurrent operations completed:")
    for result in results:
        print(result)

if __name__ == "__main__":
    print("Testing thread safety of tree locking system...")
    test_concurrent_operations()
    print("Test completed successfully!")
