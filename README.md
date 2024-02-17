# Virtual Network Firewall
 
## Summary
The Virtual Network Firewall is a project that aims to provide a secure network environment by implementing a firewall within a virtual network. It allows you to control inbound and outbound traffic, filter packets based on predefined rules, and protect your network from unauthorized access. 

### Key Features

- **Traffic Control**: The Virtual Network Firewall enables you to manage and control the flow of network traffic, allowing you to define rules for accepting or rejecting packets based on various criteria such as source IP, destination IP, port numbers, and protocols.

- **Packet Filtering**: With the firewall in place, you can filter packets based on predefined rules. This helps in preventing unauthorized access, blocking malicious traffic, and ensuring the security of your network.

- **Network Segmentation**: By implementing the Virtual Network Firewall, you can create separate network segments within your virtual network. This allows you to isolate different parts of your network and control the communication between them, enhancing the overall security of your infrastructure.

- **Logging and Monitoring**: The firewall provides logging and monitoring capabilities, allowing you to track network activity, detect potential security threats, and analyze traffic patterns. This helps in identifying and mitigating security incidents effectively.

### Benefits

- **Enhanced Security**: By implementing a firewall within your virtual network, you can strengthen the security of your infrastructure and protect your sensitive data from unauthorized access.

- **Flexibility**: The Virtual Network Firewall offers flexibility in defining and modifying firewall rules, allowing you to adapt to changing network requirements and security policies.

- **Cost-Effective**: As the firewall is implemented within a virtual network, it eliminates the need for physical hardware, reducing costs associated with traditional firewall solutions.

- **Scalability**: The solution can be easily scaled to accommodate growing network demands, ensuring that your network remains secure even as your infrastructure expands.


## How to Run

To run the Virtual Network Firewall, follow these steps:

### Environment Setup
Kali OS - This can be used through a Virtual Environment (VM) such as Ubuntu Version 18+ or any other VM that supports Kali.

Once you have your VM setup you will need to install Mininet emulater and a POX controller with the following instructions:

### Installing Mininet
~$ sudo apt install mininet

If installed correctly, you can run the following command that will create a simple test network and can follow by using the "pingall" command to see if host1 can ping to host2 or not.
~$ sudo mn

### Installing Pox Controller(through source)
~$ git clone http://github.com/noxrepo/pox
~$ cd pox
~/pox$ git checkout dart

To run pox controller, you need to run the pox.py or debug-pox.py file as below
~/pox$ ./pox.py "your_controller_module"

This will drop you into the CLI with the network topology defined in the python script.
NOTE: You might have to use a slightly different command if you have a newer version of python such as Python3 which would instead look like "sudo python3 yourFolder/topos/part1.py".

To run this part you will need to do the following:

1. Place controller.py in ~pox/ext/directory. Then from the pox directory run "./pox.py controller".

2. Ensure, in the topology program the following import statement is added:
"from mininet.node import RemoteController".

3. Ensure that in the topology program's main, mininet call uses the RemoteController:
net = Mininet(topo = topo, controller = RemoteController)

## Technologies Used
The Virtual Network Firewall project utilizes the following technologies:

- Kali OS
- Mininet emulator
- POX controller


