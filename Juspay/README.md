# Tree Lock Management System

A Flask-based REST API with a React frontend for managing hierarchical locks on tree structures. This system implements thread-safe locking operations with support for lock, unlock, and upgrade operations.

## Features

- **Thread-safe operations**: All locking operations are thread-safe using RLock
- **Hierarchical locking**: Prevents locking parent nodes when children are locked
- **Upgrade operations**: Upgrade locks from descendants to parent nodes
- **Real-time UI**: React frontend with live tree visualization
- **RESTful API**: Clean HTTP endpoints for all operations

## Project Structure

```
Juspay/
├── app.py                 # Flask server with tree locking logic
├── requirements.txt       # Python dependencies
├── frontend/             # React frontend application
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.js        # Main React component
│       ├── App.css       # Styling
│       ├── index.js      # React entry point
│       └── index.css     # Global styles
└── README.md
```

## Setup Instructions

### Backend (Flask Server)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask server:**
   ```bash
   python app.py
   ```
   
   The server will start on `http://localhost:5000`

### Frontend (React App)

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   
   The frontend will start on `http://localhost:3000`

## API Endpoints

### POST /lock
Lock a node in the tree.

**Request:**
```json
{
  "node": "Asia",
  "uid": 1
}
```

**Response:**
```json
{
  "success": true
}
```

### POST /unlock
Unlock a node in the tree.

**Request:**
```json
{
  "node": "Asia",
  "uid": 1
}
```

**Response:**
```json
{
  "success": true
}
```

### POST /upgrade
Upgrade locks from descendants to parent node.

**Request:**
```json
{
  "node": "Asia",
  "uid": 1
}
```

**Response:**
```json
{
  "success": true
}
```

### GET /tree
Get the current state of the entire tree.

**Response:**
```json
{
  "tree": {
    "World": {
      "name": "World",
      "locked_by": null,
      "children": ["Asia", "Europe", "Africa"],
      "parent": null
    },
    "Asia": {
      "name": "Asia",
      "locked_by": 1,
      "children": ["China", "India", "Japan"],
      "parent": "World"
    }
  }
}
```

## Frontend Usage

1. **Select a node**: Click on any node in the tree to select it
2. **Enter User ID**: Input a numeric user ID (1, 2, 3, etc.)
3. **Perform operations**:
   - **Lock**: Lock the selected node (if possible)
   - **Unlock**: Unlock the selected node (if you own the lock)
   - **Upgrade**: Upgrade locks from descendants to the selected node

## Locking Rules

- A node cannot be locked if any of its descendants are locked
- A node cannot be locked if any of its ancestors are locked
- Only the user who locked a node can unlock it
- Upgrade operation requires all descendants to be locked by the same user

## Tree Structure

The system initializes with a sample tree:
```
World
├── Asia
│   ├── China
│   ├── India
│   └── Japan
├── Europe
│   ├── Germany
│   ├── France
│   └── Italy
└── Africa
```

## Thread Safety

The system uses `threading.RLock()` for each node to ensure thread-safe operations:
- Multiple threads can safely perform lock/unlock operations simultaneously
- Deadlock prevention through consistent lock ordering
- Atomic operations for complex operations like upgrade

## Development

### Modifying the Tree Structure

To change the tree structure, edit the `node_names` list in the `initialize_tree()` function in `app.py`:

```python
node_names = ["Your", "Custom", "Node", "Names", "Here"]
```

### Adding New Operations

To add new operations, create new Flask endpoints in `app.py` and corresponding frontend functionality in `App.js`.

## Testing

You can test the API endpoints using curl:

```bash
# Lock a node
curl -X POST http://localhost:5000/lock \
  -H "Content-Type: application/json" \
  -d '{"node": "Asia", "uid": 1}'

# Get tree state
curl http://localhost:5000/tree
```

## Technologies Used

- **Backend**: Flask, Flask-CORS
- **Frontend**: React, Axios
- **Threading**: Python threading.RLock
- **Styling**: CSS3 with modern design patterns 