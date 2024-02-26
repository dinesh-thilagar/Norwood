from netmiko import ConnectHandler

CSR = {
    "device_type": "cisco_ios",
    "ip": "sandbox-iosxr-1.cisco.com",
    "username": "admin",
    "password": "C1sco12345",
    "port": 22,
    'timeout': 60,  # Adjust timeout if needed
    'fast_cli': False,  # Try setting fast_cli to False
    'session_log': 'output.log',  # Save session log for debugging
    'verbose': True,  # Enable verbose mode for debugging
    'global_delay_factor': 2,  # Adjust delay factor if needed
    'allow_agent': False,  # Disable SSH agent forwarding
    'ssh_strict': False,  # Disable strict SSH key checking
    'conn_timeout': 10,  # Adjust connection timeout if needed
    'blocking_timeout': 10,  # Adjust blocking timeout if needed
    'keepalive': 5,  # Adjust keepalive interval if needed
    'session_timeout': 90,  # Adjust session timeout if needed
    'default_enter': '\r\n',  # Adjust default enter character if needed
}

net_connect = ConnectHandler(**CSR)

loopback_config = [
    'interface Loopback0',
    'description My Loopback Interface',
    'ipv4 address 10.0.0.1 255.255.255.0',  # Replace with desired IP address and subnet mask
    'exit',
    'commit'
]

net_connect.send_config_set(loopback_config)

loopback_remove = [
    'no interface Loopback0',  # Command to remove the loopback interface
    'commit'
]
# res = net_connect.send_config_set(loopback_remove)
# print(res)
output = net_connect.send_command('show running-config interface Loopback0')
print(output)

net_connect.disconnect()
