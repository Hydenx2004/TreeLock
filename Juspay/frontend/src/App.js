import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = 'https://treelock.ddns.net:5000';

function App() {
  const [treeData, setTreeData] = useState({});
  const [selectedNode, setSelectedNode] = useState('');
  const [uid, setUid] = useState(1);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Fetch tree data
  const fetchTreeData = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/tree`);
      setTreeData(response.data.tree);
    } catch (error) {
      console.error('Error fetching tree data:', error);
      setMessage('Error fetching tree data');
    }
  };

  // Perform lock operation
  const performOperation = async (operation) => {
    if (!selectedNode) {
      setMessage('Please select a node first');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const response = await axios.post(`${API_BASE_URL}/${operation}`, {
        node: selectedNode,
        uid: parseInt(uid)
      });

      if (response.data.success) {
        setMessage(`${operation} operation successful!`);
        fetchTreeData(); // Refresh tree data
      } else {
        setMessage(`${operation} operation failed`);
      }
    } catch (error) {
      console.error(`Error performing ${operation}:`, error);
      setMessage(`Error performing ${operation} operation`);
    } finally {
      setLoading(false);
    }
  };

  // Render tree node
  const renderNode = (nodeName, nodeData, level = 0) => {
    const isLocked = nodeData.locked_by !== null;
    const isSelected = selectedNode === nodeName;

    return (
      <div key={nodeName} style={{ marginLeft: level * 40 }}>
        <div 
          className={`tree-node ${isLocked ? 'locked' : ''} ${isSelected ? 'selected' : ''}`}
          onClick={() => setSelectedNode(nodeName)}
        >
          <span className="node-name">{nodeName}</span>
          {isLocked && (
            <span className="lock-info">🔒 Locked by {nodeData.locked_by}</span>
          )}
        </div>
        {nodeData.children && nodeData.children.length > 0 && (
          <div className="children">
            {nodeData.children.map(childName => 
              renderNode(childName, treeData[childName], level + 1)
            )}
          </div>
        )}
      </div>
    );
  };

  // Get root nodes (nodes without parents)
  const getRootNodes = () => {
    return Object.entries(treeData).filter(([name, data]) => !data.parent);
  };

  useEffect(() => {
    fetchTreeData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌳 Tree Lock Manager</h1>
      </header>
      
      <div className="main-content">
        <div className="tree-container">
          <h2>Tree Structure</h2>
          <div className="tree">
            {getRootNodes().map(([name, data]) => renderNode(name, data))}
          </div>
        </div>
        
        <div className="controls">
          <h2>Operations</h2>
          
          <div className="input-group">
            <label>Selected Node:</label>
            <input 
              type="text" 
              value={selectedNode} 
              onChange={(e) => setSelectedNode(e.target.value)}
              placeholder="Enter node name"
            />
          </div>
          
          <div className="input-group">
            <label>User ID:</label>
            <input 
              type="number" 
              value={uid} 
              onChange={(e) => setUid(e.target.value)}
              min="1"
            />
          </div>
          
          <div className="button-group">
            <button 
              onClick={() => performOperation('lock')}
              disabled={loading || !selectedNode}
              className="btn btn-lock"
            >
              🔒 Lock
            </button>
            
            <button 
              onClick={() => performOperation('unlock')}
              disabled={loading || !selectedNode}
              className="btn btn-unlock"
            >
              🔓 Unlock
            </button>
            
            <button 
              onClick={() => performOperation('upgrade')}
              disabled={loading || !selectedNode}
              className="btn btn-upgrade"
            >
              ⬆️ Upgrade
            </button>
          </div>
          
          {message && (
            <div className={`message ${message.includes('Error') ? 'error' : 'success'}`}>
              {message}
            </div>
          )}
          
          <div className="info">
            <h3>How to use:</h3>
            <ul>
              <li>Click on a node to select it</li>
              <li>Enter a User ID (1, 2, 3, etc.)</li>
              <li>Click Lock to lock the selected node</li>
              <li>Click Unlock to unlock the selected node</li>
              <li>Click Upgrade to upgrade locks from descendants</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App; 