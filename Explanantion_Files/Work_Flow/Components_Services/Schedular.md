# Schedular

## Data Structures

### **StartHeap (Min Heap)**

- Comparison will be based on StartTime of Application_Instace_Id
- Other Stored Info
    - application_instace_id
    
### **EndHeap (Min Heap)**

- Comparison will be based on EndTime of Application_Instace_Id

---

## Working

### Thread 1

- Constantly Check current time with **StartHeap** top Element
    - In Case of Match → Following msg will be sent to Deployer (Through Kafka)
        
        ```python
        run application_instance_id
        ```
        
    - Pop top element → StartTime
    - EndTime → StartTime + Duration
    - push EndTime element to **EndHeap**
    

### Thread 2

- Constantly Check current time with **EndHeap**  top Element
    - In Case of Match → Following msg will be sent to Deployer (Through Kafka)
        
        ```python
        kill application_instance_id
        ```
        
    - Pop top element → EndTime
    - NewStartTime → EndTime + Interval
    - If Repeatation == True:
        - push NewStartTime  to **StartHeap**
        
---

## Fault Tollerance

- Following Info will be continuously updated in SchedularDB
    
    ```python
    application_instace_id

    start_date
    start_time
    
    end_date
    end_time
    
    duration
    repetition
    interval
    ```