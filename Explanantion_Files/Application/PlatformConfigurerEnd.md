# Platform Configurer

## **Sensor**

- **Sensor Type Configuration**
    
    ```json
    {
    	"company" : "GPS:ABC",
    	"model" : "MODEL1",
    	"data_rate" : "1 SEC",
    	"field_count" : 2,
    	"field_1": "int",
    	"field_2": "int"			
    }
    ```
    
- **Sensor Instance Configuration**
    
    ```json
    {
        "sensor_type": "sensor_type_GPS",
        "sensor_location": {
            "ip": "",
            "port": ""
        },
        "geo_location": {
            "room_no": "0",
            "house_no": "0",
            "street": "UNK",
            "city": "HYD"
        }
    }
    ```

--- 

## **Controller**

- **Controller Type Configuration**
    
    ```json
    {
    	"company" : "AC:ABC",
    	"model" : "MODEL1",
    	"input" : "string"		
    }
    ```
    
- **Controller Instance Configuration**
    
    ```json
    {
        "controller_type": "controller_type_AC",
        "controller_location": {
            "ip": "",
            "port": ""
        },
        "geo_location": {
            "room_no": "0",
            "house_no": "0",
            "street": "UNK",
            "city": "HYD"
        }
    }
    ```
    
---
Multiple same **configuration** Json files can **uploaded **simultaneously** by **zipping them together**