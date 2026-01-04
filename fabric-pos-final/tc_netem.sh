#!/bin/bash

# Network interface to apply emulation (change if needed)
IFACE=eth0

# Clear existing traffic control rules
sudo tc qdisc del dev $IFACE root 2>/dev/null

# Add root queue discipline with HTB for bandwidth control
sudo tc qdisc add dev $IFACE root handle 1: htb default 10
sudo tc class add dev $IFACE parent 1: classid 1:10 htb rate 100mbit ceil 100mbit

# Add netem for delay, jitter, and packet loss
sudo tc qdisc add dev $IFACE parent 1:10 handle 10: netem \
    delay 5ms 1ms distribution normal \
    loss 0.1%

echo "Network emulation applied:"
echo "RTT ≈ 10 ms, Jitter ≈ 2 ms, Packet loss = 0.1%, Bandwidth = 100 Mbps"
