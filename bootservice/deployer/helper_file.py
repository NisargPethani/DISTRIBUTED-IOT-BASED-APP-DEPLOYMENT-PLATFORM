import paramiko
import os,sys,time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from conf import ssh_conf as conf_file   
import socket

class ssh_util():
    def __init__(self):
        # self.ssh_output = None
        # self.ssh_error = None
        self.client = None
        self.host= ""
        self.username = "aditya"
        self.password = "Abc@12345xyz"
        # self.timeout = float(conf_file.TIMEOUT)
        # self.commands = conf_file.COMMANDS
        # self.pkey = conf_file.PKEY
        # self.port = conf_file.PORT
        # self.uploadremotefilepath = conf_file.UPLOADREMOTEFILEPATH
        # self.uploadlocalfilepath = conf_file.UPLOADLOCALFILEPATH
        # self.downloadremotefilepath = conf_file.DOWNLOADREMOTEFILEPATH
        # self.downloadlocalfilepath = conf_file.DOWNLOADLOCALFILEPATH

    def connect(self):
        "Login to the remote server"
        try:
            #Paramiko.SSHClient can be used to make connections to the remote server and transfer files
            # print("Establishing ssh connection")
            self.client = paramiko.SSHClient()
            #Parsing an instance of the AutoAddPolicy to set_missing_host_key_policy() changes it to allow any host.
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            #Connect to the server
            
            self.client.connect(hostname=self.host, username=self.username, password=self.password, allow_agent=False,look_for_keys=False)    
            # print("Connected to the server",self.host)
        except paramiko.AuthenticationException:
            # print("Authentication failed, please verify your credentials")
            result_flag = False
        except paramiko.SSHException as sshException:
            # print("Could not establish SSH connection: %s" % sshException)
            result_flag = False
        except socket.timeout as e:
            # print("Connection timed out")
            result_flag = False
        except Exception as e:
            # print("Exception in connecting to the server")
            # print("PYTHON SAYS:",e)
            result_flag = False
            self.client.close()
        else:
            result_flag = True
 
        return result_flag

    def execute_command(self,commands, vm_ip, vm_username):
        """Execute a command on the remote host.Return a tuple containing
        an integer status and a two strings, the first containing stdout
        and the second containing stderr from the command."""


        self.host= vm_ip
        self.username = vm_username

        self.ssh_output = None
        result_flag = True
        try:
            if self.connect():
                for command in commands:
                    # print("Executing command --> {}".format(command))
                    stdin, stdout, stderr = self.client.exec_command(command,timeout=10)
                    self.ssh_output = stdout.read()
                    self.ssh_error = stderr.read()
                    if self.ssh_error:
                        # print("Problem occurred while running command:"+ command + " The error is " + self.ssh_error)
                        result_flag = False
                    else:    
                        pass
                        # print("Command execution completed successfully",command, self.ssh_output)
                    self.client.close()
            else:
                # print("Could not establish SSH connection")
                result_flag = False   
        except socket.timeout as e:
            # print("Command timed out.", command)
            self.client.close()
            result_flag = False                
        except paramiko.SSHException:
            # print("Failed to execute the command!",command)
            self.client.close()
            result_flag = False   
        if result_flag:
            return result_flag, self.ssh_output
        else:
            return result_flag, self.ssh_error

# obj = ssh_util()
# obj.execute_command(["vmstat -s"])