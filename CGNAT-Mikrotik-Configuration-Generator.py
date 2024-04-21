import ipaddress

StartingAddress = ipaddress.IPv4Address('100.64.0.0')
ClientCount = 8
AddressesPerClient = 1
PublicAddress = ipaddress.IPv4Address('85.85.85.0')
StartingPort = 11024
PortsPerAddress = 5000

with open('configuration.rsc', 'w') as file:
    for _ in range(128):
        # All client chain jump
        file.write('/ip firewall nat add chain=srcnat action=jump jump-target="{0}-{1}" \\\n'.format(StartingAddress, StartingAddress + (ClientCount * AddressesPerClient) - 1))
        file.write('    src-address="{0}-{1}"\n'.format(StartingAddress, StartingAddress + (ClientCount * AddressesPerClient) - 1))
        file.write('/ip firewall nat add chain="{0}-{1}" action=src-nat protocol=icmp src-address="{0}-{1}" to-address={2}\n\n'.format(StartingAddress, StartingAddress + (ClientCount * AddressesPerClient) - 1, PublicAddress))

        currentPort = StartingPort

        for c in range(1, ClientCount + 1):
            # Specific client chain jumps
            if AddressesPerClient > 1:
                file.write('/ip firewall nat add chain="{0}-{1}" action=jump jump-target="{2}-{3}" \\\n'.format(StartingAddress, StartingAddress + (ClientCount * AddressesPerClient) - 1, StartingAddress + (AddressesPerClient * (c - 1)), StartingAddress + (AddressesPerClient * c) - 1))
                file.write('    src-address="{0}-{1}"\n'.format(StartingAddress + (AddressesPerClient * (c - 1)), StartingAddress + (AddressesPerClient * c) - 1))
            else:
                file.write('/ip firewall nat add chain="{0}-{1}" action=jump jump-target="{2}-{3}" \\\n'.format(StartingAddress, StartingAddress + (ClientCount * AddressesPerClient) - 1, StartingAddress + (AddressesPerClient * (c - 1)), StartingAddress + (AddressesPerClient * c) - 1))
                file.write('    src-address="{0}"\n'.format(StartingAddress + (AddressesPerClient * (c - 1))))

            # Translation rules
            for a in range(1, AddressesPerClient + 1):
                file.write('/ip firewall nat add chain="{0}-{1}" action=src-nat protocol=tcp \\\n'.format(StartingAddress + (AddressesPerClient * (c - 1)), StartingAddress + (AddressesPerClient * c) - 1))
                file.write('    src-address="{0}" to-address={1} to-ports="{2}-{3}"\n'.format(StartingAddress + ((c -1) * AddressesPerClient) + a - 1, PublicAddress, currentPort, currentPort + PortsPerAddress - 1))
                file.write('/ip firewall nat add chain="{0}-{1}" action=src-nat protocol=udp \\\n'.format(StartingAddress + (AddressesPerClient * (c - 1)), StartingAddress + (AddressesPerClient * c) - 1))
                file.write('    src-address="{0}" to-address={1} to-ports="{2}-{3}"\n'.format(StartingAddress + ((c -1) * AddressesPerClient) + a - 1, PublicAddress, currentPort, currentPort + PortsPerAddress - 1))
                currentPort += PortsPerAddress

        # Increment IP addresses for the next iteration
        StartingAddress += 8
        PublicAddress += 1
