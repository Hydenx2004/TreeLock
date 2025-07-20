#!/usr/bin/env python3
"""
Test script for the Tree Lock Management API
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api():
    print("🧪 Testing Tree Lock Management API")
    print("=" * 50)
    
    # Test 1: Get initial tree state
    print("\n1. Getting initial tree state...")
    try:
        response = requests.get(f"{BASE_URL}/tree")
        if response.status_code == 200:
            tree_data = response.json()
            print("✅ Tree state retrieved successfully")
            print(f"   Nodes: {list(tree_data['tree'].keys())}")
        else:
            print(f"❌ Failed to get tree state: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return
    
    # Test 2: Lock a node
    print("\n2. Testing lock operation...")
    try:
        response = requests.post(f"{BASE_URL}/lock", 
                               json={"node": "Asia", "uid": 1})
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Lock operation successful")
            else:
                print("❌ Lock operation failed")
        else:
            print(f"❌ Lock request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error during lock operation: {e}")
    
    # Test 3: Try to lock a child node (should fail)
    print("\n3. Testing lock on child node (should fail)...")
    try:
        response = requests.post(f"{BASE_URL}/lock", 
                               json={"node": "China", "uid": 2})
        if response.status_code == 200:
            result = response.json()
            if not result['success']:
                print("✅ Lock on child correctly failed (parent is locked)")
            else:
                print("❌ Lock on child should have failed")
        else:
            print(f"❌ Lock request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error during child lock test: {e}")
    
    # Test 4: Unlock the node
    print("\n4. Testing unlock operation...")
    try:
        response = requests.post(f"{BASE_URL}/unlock", 
                               json={"node": "Asia", "uid": 1})
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Unlock operation successful")
            else:
                print("❌ Unlock operation failed")
        else:
            print(f"❌ Unlock request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error during unlock operation: {e}")
    
    # Test 5: Lock child nodes for upgrade test
    print("\n5. Locking child nodes for upgrade test...")
    try:
        # Lock China
        response = requests.post(f"{BASE_URL}/lock", 
                               json={"node": "China", "uid": 1})
        if response.status_code == 200 and response.json()['success']:
            print("✅ Locked China")
        
        # Lock India
        response = requests.post(f"{BASE_URL}/lock", 
                               json={"node": "India", "uid": 1})
        if response.status_code == 200 and response.json()['success']:
            print("✅ Locked India")
        
        # Lock Japan
        response = requests.post(f"{BASE_URL}/lock", 
                               json={"node": "Japan", "uid": 1})
        if response.status_code == 200 and response.json()['success']:
            print("✅ Locked Japan")
    except Exception as e:
        print(f"❌ Error locking children: {e}")
    
    # Test 6: Test upgrade operation
    print("\n6. Testing upgrade operation...")
    try:
        response = requests.post(f"{BASE_URL}/upgrade", 
                               json={"node": "Asia", "uid": 1})
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Upgrade operation successful")
            else:
                print("❌ Upgrade operation failed")
        else:
            print(f"❌ Upgrade request failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error during upgrade operation: {e}")
    
    # Test 7: Get final tree state
    print("\n7. Getting final tree state...")
    try:
        response = requests.get(f"{BASE_URL}/tree")
        if response.status_code == 200:
            tree_data = response.json()
            print("✅ Final tree state retrieved")
            
            # Show locked nodes
            locked_nodes = []
            for name, data in tree_data['tree'].items():
                if data['locked_by'] is not None:
                    locked_nodes.append(f"{name} (locked by {data['locked_by']})")
            
            if locked_nodes:
                print(f"   Locked nodes: {', '.join(locked_nodes)}")
            else:
                print("   No locked nodes")
        else:
            print(f"❌ Failed to get final tree state: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting final tree state: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 API testing completed!")

if __name__ == "__main__":
    test_api() 