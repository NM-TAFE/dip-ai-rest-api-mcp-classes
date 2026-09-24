data = { 
  "jsonrpc": "2.0", 
  "id": 1, 
  "error": { 
    "code": -32601, 
    "message": "Method not found" 
  } 
}  

if data['error']['code'] == -32601:
    print(f"{data['error']['message']}")