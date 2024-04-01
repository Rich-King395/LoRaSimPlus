# LoRaSim for Parameter Allocation
[LoRaSim](https://www.lancaster.ac.uk/scc/sites/lora/lorasim.html) is a LoRa Simulator developed based on simpy, a Python library for discrete events simulation. LoRaSim provides a complete network packet transmission process and proposes a collision detection mechanism. However, LoRaSim does not provide LoRa parameter allocation methods during packet transmission, which is now the research focus of many LoRa researchers. LoRaSimPlus provides researchers with richer programmable services based on LoRaSim, which can help researchers do deeper research on energy consumption and packet transmission of the LoRaWAN network.

## Requirement
* Python == 3.x
* simpy
* matplotlib
* numpy
  
## How to Use
The file ParameterConfig.py includes all the default parameter settings supported by the simulator. You can modify the default settings in ParameterConfig.py and use the following command line to run the simulator:

```
python main.py
```
You can also leave the default settings unchanged and set the parameters through the command line:

```
python main.py <NodeNum> <SendInterval> <AllocationType> <AllocationMethod> <SimulationDuration> <GWNum> <CollioosionCheck> <AntennaType> <NetworkNum> <TopologyRadius> <PayloadSize>
```

**NodeNum**: Number of nodes

**SendInterval**: Average packet send interval of node, ms

**AllocationType**: "Local" means nodes allocate LoRa parameters each time it generate a packet in the simulation process. "Global" means the loRa parameters settings are allocated when a node is set up and each node sends packets with its determined parameters during the simulation process.

**SimulationDuration**: Total simulation time, ms

**GWNum**: Number of gateways

**CollioosionCheck**: "0" for simple collision check and "1" for full collision check. Simple collision check only consider frequency collision and SF collision.

**AntennaType**: "0" for omnidirectional antenna and "1" for directional antenna. The directional antenna has different gains for different directions.

**NetworkNum**：Number of networks

**TopologyRadius**: Radius of network topology,m

**PayloadSize**: Packet payload size

For example:

```
python main.py 100 5000 Local random 3600000 1 1 1 1 3000 20
```

During the simulation, the simulation configurations and results will be printed out in the terminal. After the simulation, the configurations and results are recorded in a text file.

## Software Framework
The simulator is composed of 8 files and their respective functions are shown as follows:

### ParameterConfig.py
Include all the global variables and LoRaWAN parameters. 

### main.py
The main program of the simulator starts the simulation and outputs the results, which also provides command line interface for users to set LoRa parameters. 

### simulation.py
Define a class called Simulation, which provides methods that can be called by the main program.

Run the simulation
```
Simulation.run()
```
Calculate the simulation results 
```
simulation.results_calculation()
```
Show the results in the terminal 
```
simulation.results_show()
```
Record the parameter settings and simulation results in a text file
```
simulation.simulation_record()
```

### Node.py
Define node class. The position of each node is generated randomly. Each node generates packets with the allocation method. 

### Gateway.py
Define node class. The position of gateways is set according to their quantity.

### Packet.py
Define packet class, which provides functions to calculate the airtime, receive sensitivity, minimum SNR and transmission energy of each packet.

### Propagation.py
The simulator's propagation model includes packet collision checking and the path loss model. Packet collision checking includes frequency collision, SF collision, time collision and power collision. There are two conditions for a packet to be successfully received by the gateway: no collision during transmission and the packet is not lost. The simulator uses RSSI(Received Signal Strength Indication) and SNR(Signal Noise Ratio) to determine whether the packet is lost. The RSSI should be larger than the receive sensitivity and SNR should be larger than the minimum SNR requirement to make the packet received successfully.

### Allocation.py
Include LoRa parameters(SF, Bandwidth, Carrier frequency) allocation method. Three allocation methods are included: random allocation, polling allocation and closest allocation. The closest method allocates the minimum parameter setting to the node that enables its packet to be received successfully.  



