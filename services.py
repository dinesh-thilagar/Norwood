from fastapi import FastAPI, HTTPException
from netmiko import ConnectHandler
import docker
app = FastAPI()

CSR = {
    "device_type": "cisco_ios",
    "ip": "sandbox-iosxr-1.cisco.com",
    "username": "admin",
    "password": "C1sco12345",
    "port": 22,
    'timeout': 60
    # 'session_log': 'output.log',  # Save session log for debugging
}


# Function to create interface
def configure_loopback(loopback_num: int, description: str, ipv4_address: str, subnet_mask: str):
    try:
        loopback_config = [
            f'interface Loopback{loopback_num}',
            f'description {description}',
            f'ipv4 address {ipv4_address} {subnet_mask}',
            'exit',
            'commit'
        ]
        net_connect = ConnectHandler(**CSR)   # Establish SSH connection
        res = net_connect.send_config_set(loopback_config)
        net_connect.disconnect()
        return {"message": "Loopback configured successfully", "output": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Function to delete interface
def delete_loopback(loopback_num):
    try:
        loopback_remove = [
            f'no interface Loopback{loopback_num}',
            'commit'
        ]
        net_connect = ConnectHandler(**CSR)  # Establish SSH connection
        res = net_connect.send_config_set(loopback_remove)
        net_connect.disconnect()
        return {"message": "Loopback deleted successfully", "output": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Function to get interface status
def get_interface_status():
    try:
        # Establish SSH connection
        net_connect = ConnectHandler(**CSR)
        # Send command to get interface status
        output = net_connect.send_command("show ip interface brief")
        # Close SSH connection
        net_connect.disconnect()

        # Parse output to extract interface status
        interface_status = {}
        for line in output.splitlines()[1:]:
            if line:
                parts = line.split()
                interface_status[parts[0]] = parts[2]

        return interface_status
    except Exception as e:
        return {"error": str(e)}

# API endpoint to list interface status
@app.get("/interfaces/")
def list_interfaces():
    return get_interface_status()


# API endpoint to create interface
@app.post("/configure_loopback/")
def configure_loopback_endpoint(loopback_num: int, description: str, ipv4_address: str, subnet_mask: str):
    return configure_loopback(loopback_num, description, ipv4_address, subnet_mask)


# API endpoint to delete interface
@app.delete("/delete_loopback/{loopback_num}")
def delete_loopback_endpoint(loopback_num: int):
    return delete_loopback(loopback_num)
