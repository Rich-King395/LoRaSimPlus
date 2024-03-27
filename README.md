# LoRaWANSim
LoRaWANSim is a LoRa Simulator developed based on simpy, which is a Python library used for discrete events simulation. 

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

### Gateway.py

### Packet.py

### Propagation.py

### Allocation.py




