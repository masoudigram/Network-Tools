# CGNAT Mikrotik Configuration Generator

This Python script generates Mikrotik RouterOS NAT configuration rules for CGNAT (Carrier-Grade NAT) implementation. It creates a configuration file that can be imported into Mikrotik routers to set up NAT rules for multiple clients sharing public IP addresses.

## Overview

The script generates NAT rules that:
- Maps private IP addresses to public IP addresses
- Allocates specific port ranges for each client
- Handles both TCP and UDP protocols
- Includes ICMP protocol handling
- Creates hierarchical NAT rules for better organization

## Optimization Benefits

The script implements an optimized NAT rule structure that significantly reduces router resource usage:

### Hierarchical Rule Structure
- Uses Mikrotik's jump rules to create a tree-like structure of NAT rules
- Instead of checking all rules sequentially, the router only needs to match a few rules to find the correct NAT configuration
- Example flow:
  1. First match: Main chain (all clients)
  2. Second match: Client-specific chain
  3. Final match: Specific protocol and port rules

### Resource Efficiency
- **Memory Usage**: Despite generating many NAT rules, the hierarchical structure ensures minimal memory impact
- **CPU Load**: The router only needs to process a small subset of rules for each packet
- **Performance**: Packet processing time is optimized by reducing the number of rule checks

### Scalability
- The optimization allows for handling large numbers of clients without significant performance degradation
- Each additional client adds minimal overhead due to the efficient rule structure
- Perfect for ISPs and large networks implementing CGNAT

## Configuration Parameters

The script uses the following parameters that can be modified at the top of the file. Each parameter serves a specific purpose in the CGNAT configuration:

### Network Configuration
- `StartingAddress`: The initial private IP address (default: 100.64.0.0)
  - This is the first IP address in the CGNAT range (100.64.0.0/10)
  - Used as the base address for all client allocations
  - Should be within the CGNAT range (100.64.0.0/10)

- `PublicAddress`: The starting public IP address (default: 85.85.85.0)
  - This is the public IP address that will be used for NAT
  - Each client's traffic will be translated to this address
  - Should be a valid public IP address assigned to your network

### Client Configuration
- `ClientCount`: Number of clients to configure (default: 8)
  - Determines how many separate clients will be configured
  - Each client gets its own NAT rules and port ranges
  - Affects the total number of rules generated

- `AddressesPerClient`: Number of private IP addresses per client (default: 1)
  - Specifies how many private IP addresses each client can use
  - If set to 1, each client gets a single private IP
  - If set higher, each client gets a range of private IPs

### Port Configuration
- `StartingPort`: The initial port number for NAT (default: 11024)
  - The first port number used for NAT translation
  - Should be above 1024 (non-privileged ports)
  - Each client's port range starts from this number

- `PortsPerAddress`: Number of ports allocated per address (default: 5000)
  - Determines how many ports each client can use
  - Total ports per client = PortsPerAddress × AddressesPerClient
  - Should be large enough to handle expected client traffic
  - Example: With default settings, each client gets 5000 ports

## Output

The script generates a `configuration.rsc` file containing Mikrotik RouterOS commands that:
1. Creates main NAT chains for all clients
2. Creates specific chains for each client
3. Sets up NAT rules for TCP, UDP, and ICMP protocols
4. Configures port forwarding ranges for each client

## Usage

1. Modify the configuration parameters at the top of the script if needed
2. Run the script:
   ```bash
   python CGNAT-Mikrotik-Configuration-Generator.py
   ```
3. The script will generate a `configuration.rsc` file
4. Import the generated configuration into your Mikrotik router

## Example Configuration

The script generates rules in the following format:
```
/ip firewall nat add chain=srcnat action=jump jump-target="100.64.0.0-100.64.0.7" src-address="100.64.0.0-100.64.0.7"
/ip firewall nat add chain="100.64.0.0-100.64.0.7" action=src-nat protocol=icmp src-address="100.64.0.0-100.64.0.7" to-address=85.85.85.0
```

## Notes

- The script automatically increments IP addresses and ports for each iteration
- Each client gets a dedicated port range for TCP and UDP traffic
- ICMP traffic is handled separately with direct NAT rules
- The configuration is organized in a hierarchical structure for better management

## Requirements

- Python 3.x
- `ipaddress` module (included in Python standard library)

## Security Considerations

- Ensure proper firewall rules are in place
- Monitor port usage to prevent exhaustion
- Consider implementing rate limiting
- Regularly review and update NAT rules as needed 
