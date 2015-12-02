#!/bin/sh

# Deletes all previously created bridges that were created with scratch.py
sudo ovs-vsctl der-br br0
sudo ovs-vsctl der-br br1
sudo ovs-vsctl der-br br2
sudo ovs-vsctl der-br br3
sudo ovs-vsctl der-br br4

# Deletes any interfaces previously created
sudo ip link del P2-eth2
sudo ip link del PE3-eth0
sudo ip link del P2-eth1
sudo ip link del PE2-eth0
sudo ip link del P1-eth1
sudo ip link del P2-eth0
sudo ip link del PE1-eth0
sudo ip link del P1-eth0