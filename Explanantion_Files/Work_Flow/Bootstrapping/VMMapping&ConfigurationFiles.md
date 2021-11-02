# VM Mapping & Configuration Files

```bash
services = [
	"kafka", 
	"scheduler", 
	"Deployer", 
	"Sensor_manager", 
	"ui_appmanager", 
	"node_manager",
	"fault_tolerence",
	"monitoring",
	"sensor_server",
	"controller_server"
]
```

Allocating `VM IP` to `each service`  (Round Robin Fashion) 

---

## VM Mappings : `provisioned_vms.txt`

```bash
'' 'VM1' 'username' 'kafka'
'' 'VM2' 'username' 'scheduler'
'' 'VM1' 'username' 'deployer'
'' 'VM2' 'username' 'sensor_manager'
'' 'VM1' 'username' 'ui_appmanager'
'' 'VM2' 'username' 'node_manager'
'' 'VM1' 'username' 'fault_tolerence'
'' 'VM2' 'username' 'monitoring'
'' 'VM1' 'username' 'sensor_server'
'' 'VM2' 'username' 'controller_server'
```

---

## Config

### `kafka_config.json`

```bash
{
    "username": "", 
    "ip": "", 
    "port": 9092, 
    "vm_name": "VM1"
}
```

### `services_config.json`

```bash
{
    "monitoring": {
        "username": "", 
        "ip": "", 
        "vm_name": "VM2"
    }, 
    "controller_server": {
        "username": "", 
        "ip": "", 
        "vm_name": "VM2"
    }, 
    "other_service_name": {
        "username": "", 
        "ip": "", 
        "vm_name": "VM"
    }
}
```