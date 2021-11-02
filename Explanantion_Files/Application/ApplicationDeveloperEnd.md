# Application Developer

## **Configuration Files**

- `appname.json`
    
    ```json
    {
        "app_name" : "COVID VACCINATION"
    }
    ```
    
- `controller.json`
    
    ```json
    {
        "controller_instance_count": 15,
        "controller_instance_info": [
            {
                "controller_instance_index": 0,
                "controller_instance_type": "controller_type_LIGHT"
            },
            {
                "controller_instance_index": 1,
                "controller_instance_type": "controller_type_AC"
            },
            {
                "controller_instance_index": 2,
                "controller_instance_type": "controller_type_BUZZER"
            },
            {
                "controller_instance_index": 3,
                "controller_instance_type": "controller_type_LIGHT"
            }
        ]
    }
    ```
    
- `sensor.json`
    
    ```json
    {
        "sensor_instance_count": 20,
        "sensor_instance_info": [
            {
                "sensor_instance_index": 0,
                "sensor_instance_type": "sensor_type_GPS"
            },
            {
                "sensor_instance_index": 1,
                "sensor_instance_type": "sensor_type_TEMP"
            },
            {
                "sensor_instance_index": 2,
                "sensor_instance_type": "sensor_type_LIGHT"
            },
            {
                "sensor_instance_index": 3,
                "sensor_instance_type": "sensor_type_BIOMETRIC"
            }
        ]
    }
    ```

---  

## **Application Code**

- **Application Driver Code**
    
    ```cpp
    AlgoNumber = int(sys.argv[2])
    
    ####################################
    
    def ALGO1():
        a1.run()
    
    def ALGO2():
        a2.run()
    
    def ALGO3():
        a3.run()
    
    ###################################
    
    if AlgoNumber == 0:
        threading.Thread(target=ALGO1).start()
    
    elif AlgoNumber == 1:
        threading.Thread(target=ALGO2).start()
    
    else:
        threading.Thread(target=ALGO3).start()
    ```
    
- **Algorithm Code**
    
    ```python
    def get_specific_sensor_data(busid, sensor_type):
    		
        id = sensor_type + busid*4
        sensor_data = interface_to_get_data_new.get_sensor_data( id )

        return sensor_data
    ```
    
    ```python
    threading.Thread(
    
        target = action_and_notification_api.send_notification,
        args=(message,)

    ).start()
    ```
    
    ```python
    threading.Thread(
    
        target = send_sms_api.send_email, 
        args=(message,)
    
    ).start()
    ```