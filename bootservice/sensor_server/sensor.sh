# az vm open-port --port 80 --resource-group final2 --name VM2 --priority 600
gnome-terminal --title="BUS1_sensor_biometric" -e "bash -c 'python3 sensor_biometric.py 50741 50741; bash'"
gnome-terminal --title="BUS2_sensor_biometric" -e "bash -c 'python3 sensor_biometric.py 50742 50742; bash'"
gnome-terminal --title="BUS3_sensor_biometric" -e "bash -c 'python3 sensor_biometric.py 50743 50743; bash'"
gnome-terminal --title="BUS4_sensor_biometric" -e "bash -c 'python3 sensor_biometric.py 50744 50744; bash'"
gnome-terminal --title="BUS5_sensor_biometric" -e "bash -c 'python3 sensor_biometric.py 50745 50745; bash'"

gnome-terminal --title="BUS1_sensor_gps" -e "bash -c 'python3 sensor_gps.py 50731 -2 3; bash'"
gnome-terminal --title="BUS2_sensor_gps" -e "bash -c 'python3 sensor_gps.py 50732 -1 -3; bash'"
gnome-terminal --title="BUS3_sensor_gps" -e "bash -c 'python3 sensor_gps.py 50733 4 -0.5; bash'"
gnome-terminal --title="BUS4_sensor_gps" -e "bash -c 'python3 sensor_gps.py 50734 2 3'; bash"
gnome-terminal --title="BUS5_sensor_gps" -e "bash -c 'python3 sensor_gps.py 50735 1.5 3.4'; bash"

gnome-terminal --title="BUS1_sensor_light" -e "bash -c 'python3 sensor_light.py 50721; bash'" 
gnome-terminal --title="BUS2_sensor_light" -e "bash -c 'python3 sensor_light.py 50722; bash'" 
gnome-terminal --title="BUS3_sensor_light" -e "bash -c 'python3 sensor_light.py 50723; bash'" 
gnome-terminal --title="BUS4_sensor_light" -e "bash -c 'python3 sensor_light.py 50724; bash'" 
gnome-terminal --title="BUS5_sensor_light" -e "bash -c 'python3 sensor_light.py 50725; bash'"

gnome-terminal --title="BUS1_sensor_temp" -e "bash -c 'python3 sensor_temp.py 50711; bash'"
gnome-terminal --title="BUS2_sensor_temp" -e "bash -c 'python3 sensor_temp.py 50712; bash'"
gnome-terminal --title="BUS3_sensor_temp" -e "bash -c 'python3 sensor_temp.py 50713; bash'"
gnome-terminal --title="BUS4_sensor_temp" -e "bash -c 'python3 sensor_temp.py 50714; bash'"
gnome-terminal --title="BUS5_sensor_temp" -e "bash -c 'python3 sensor_temp.py 50715; bash'"
