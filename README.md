# LoRaWANSim
LoRaWANSim is a LoRa Simulator developed based on simpy, which is a Python library used for discrete events simulation. 

## Requirement
* Python == 3.x
* simpy
* matplotlib
* numpy
  
## How to Use
The file ParameterConfig.py includes all the default parameters settings supported by the simulator. You can modify the default settings in ParameterConfig.py and use the following command line to run the simulator:

```
python main.py
```
You can also leave the default settings unchanged and set the parameters through the command line:

```
python main.py <NodeNum> <SendInterval> <AllocationType> <AllocationMethod> <SimulationDuration> <GWNum> <CollioosionCheck> <AntennaType> <NetworkNum> <TopologyRadius> <PayloadSize>
```

<NodeNum>: Number of nodes

<SendInterval>: Average packet send interval of node, ms

<AllocationType>: "Local" means nodes allocate lora parameters each time it generate a packet in the simulation process. "Global" means the lora parameters settings are allocated when node is set up and the each node sends packet with its determined parameters during the whole simulation process.

SimulationDuration: Total simulation time, ms

GWNum: Number of gateways

CollioosionCheck: "0" for simple collision cheak and "1" for full collision check. Simple collision check only consider frequency collision and SF collision.

AntennaType: "0" for omnidirectional antenna and "1" for directional antenna. Directional antenna has different gains for different directions.

NetworkNum：Number of networks

TopologyRadius: Radius of network topology

PayloadSize: Packet payload size







## Software Framework
