# Node Manager

## Database
 ---
### Active Node Database

```sql
CREATE TABLE nodes (
    ip VARCHAR(255) NOT NULL, 
    port VARCHAR(255) NOT NULL, 
    status VARCHAR(255) NOT NULL, 
    user VARCHAR(255) NOT NULL, 
    PRIMARY KEY(ip,port)
)
```

---

## Working

### Interaction With Deployer

- List of Active Nodes
    
    ```python
    def get_active_node_list(message_content):
        if message_content == "node_list":
            active_node_list = fetch_active_nodes()
            send_message = "{};{}".format('multiple', form_string(active_node_list))
    ```
    
    ```python
    def fetch_active_nodes():
        mycursor.execute("select ip, port, user from nodes where status='active'")
        active_nodes = mycursor.fetchall()
    
        return active_nodes
    ```
    
- Asking For new Node to run Application
    
    ```python
    def get_active_node_list(message_content):
        elif message_content == "new_node":
    
            new_node = create_new_node()
            set_active(new_node)
    ```
    
    ```python
    #create and send the new node. <ip and port>
    def create_new_node():
    		
        mycursor.execute("select ip, port, user from nodes where status='free' limit 1;")
        free_node = mycursor.fetchall()
        
        return free_node
    ```
    
    ```python
    def set_active(ip, port,user):
    
        Q = "update nodes set status = 'active' " + \
    				"where ip = '{}' and port = '{}' " + \
    				"and user = '{}';".format(ip,port,user)
    		
        mycursor.execute(Q)
    ```
    
 ---
### Interaction With Node

- Insert New Node to Database
    
    ```python
    def insert_free_node(ip, port, user):
    
       if Node_Exists:
            Q = "update nodes set status = 'active'" + \
                " where ip = '{}' and port = '{}' " + \ 
                "and user = '{}';".format(ip,port,user)
    
            mycursor.execute(Q)
    
        else:
            Q = "insert into nodes " + \
                "values('{}', '{}', '{}', '{}');".format(ip,port, "free", user)
    
            mycursor.execute(Q)
    		
    ```
    
 ---
### Interaction With Fault Tollerance

- Delete Node from Database
    
    ```python
    def set_deleted(ip, port):
        Q = "update nodes set status = 'deleted' " + \
            "where ip = '{}' and port = '{}';".format(ip,port)
    
        mycursor.execute(Q)
    ```