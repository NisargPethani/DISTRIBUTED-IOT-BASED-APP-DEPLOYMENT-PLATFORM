# az vm open-port --port 80 --resource-group final2 --name VM2 --priority 600
scp ./controller.py username@:/home/username
scp ./port_script.sh username@:/home/username
sshpass -f pass ssh -o StrictHostKeyChecking=no username@ "bash port_script.sh"
gnome-terminal --title="BUS1_LIGHT" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50611 BUS1_LIGHT; /bin/bash'"
gnome-terminal --title="BUS2_LIGHT" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50612 BUS2_LIGHT; /bin/bash'"
gnome-terminal --title="BUS3_LIGHT" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50613 BUS3_LIGHT; /bin/bash'"
gnome-terminal --title="BUS4_LIGHT" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50614 BUS4_LIGHT; /bin/bash'"
gnome-terminal --title="BUS5_LIGHT" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50615 BUS5_LIGHT; /bin/bash'"
gnome-terminal --title="BUS1_AC" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50621 BUS1_AC; /bin/bash'"
gnome-terminal --title="BUS2_AC" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50622 BUS2_AC; /bin/bash'"
gnome-terminal --title="BUS3_AC" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50623 BUS3_AC; /bin/bash'"
gnome-terminal --title="BUS4_AC" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50624 BUS4_AC; /bin/bash'"
gnome-terminal --title="BUS5_AC" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50625 BUS5_AC; /bin/bash'"
gnome-terminal --title="BUS1_BUZZER" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50631 BUS1_BUZZER; /bin/bash'"
gnome-terminal --title="BUS2_BUZZER" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50632 BUS2_BUZZER; /bin/bash'"
gnome-terminal --title="BUS3_BUZZER" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50633 BUS3_BUZZER; /bin/bash'"
gnome-terminal --title="BUS4_BUZZER" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50634 BUS4_BUZZER; /bin/bash'"
gnome-terminal --title="BUS5_BUZZER" --window-with-profile=NOCLOSEPROFILE -e "sshpass -f pass ssh -t -o StrictHostKeyChecking=no username@ 'ps;python3 controller.py 50635 BUS5_BUZZER; /bin/bash'"

