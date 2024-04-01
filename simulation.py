import random
import os
from ParameterConfig import *
from Propagation import checkcollision
from Gateway import myBS
from Node import myNode
from datetime import datetime

class Simulation:
    def __init__(self):
        self.sum = 0
        self.sumSent = 0
        self.sent = []
        self.der = []
        self.simstarttime = 0
        self.simendtime = 0
        self.avgDER = 0
        self.derALL = 0
        self.RecPacketSize = 0
        self.TotalPacketSize = 0
        self.TotalPacketAirtime = 0
        self.TotalEnergyConsumption = 0
        self.throughput = 0
        self.EffectEnergyConsumPerByte = 0
        self.file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.folder_path = os.path.join(os.getcwd(), "results")
        self.folder_path = os.path.join(self.folder_path,self.file_name)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

    def run(self):
        # generate BS
        for i in range(0,nrBS):
            b = myBS(i)
            bs.append(b) # append the BS to the list
            # append new list for each BS
            packetsAtBS.append([]) 
            packetsRecBS.append([])

        # generate node
        id = 0
        while len(nodes) < nrNodes*nrBS:
            # myNode takes period (in ms), base station id packetlen (in Bytes)
            # 1000000 = 16 min
            x = random.randint(-radius, radius)
            y = random.randint(-radius, radius)
            # make sure the nodes are inside the circle
            if (x ** 2 + y ** 2) > (radius ** 2):
                continue
            for j in range(0,nrBS):
                # create nrNodes for each base station
                node = myNode(id*nrBS+j,x,y,avgSendTime,bs[j]) # For different BS, same node has different id
                nodes.append(node)
                
                # when we add directionality, we update the RSSI here
                if (directionality == 1):
                    node.updateRSSI()
                env.process(Simulation.transmit(self,env,node)) # create a transmission process for each node
            id += 1

            # store nodes and basestation locations
        node_path = os.path.join(self.folder_path, self.file_name+"-node.txt")
        with open(node_path, 'w') as nfile:
            for node in nodes:
                nfile.write('{x} {y} {id}\n'.format(**vars(node)))

        basestation = os.path.join(self.folder_path, self.file_name+"-basestation.txt")
        with open(basestation, 'w') as bfile:
            for basestation in bs:
                bfile.write('{x} {y} {id}\n'.format(**vars(basestation)))

        #prepare show
        if (graphics == 1):
            plt.xlim([-radius, radius])
            plt.ylim([-radius, radius])
            plt.draw()
            plt.show()  
            
        # start simulation
        env.run(until=simtime)

    def results_calculation(self):
        for i in range(0,nrBS):
            self.sum = self.sum + len(packetsRecBS[i]) # calculate total received packets
        for i in range(0, nrBS):
            self.sent.append(0)
        for i in range(0,nrNodes*nrBS):
            self.sumSent = self.sumSent + nodes[i].sent
            #print ("id for node ", nodes[i].id, "BS:", nodes[i].bs.id, " sent: ", nodes[i].sent)
            self.sent[nodes[i].bs.id] = self.sent[nodes[i].bs.id] + nodes[i].sent

        # der = []
        # data extraction rate = Packet Dilvery Rate PDR
        self.derALL = 100*(len(recPackets)/float(self.sumSent))
        self.sumder = 0
        for i in range(0, nrBS):
            self.der.append(100*(len(packetsRecBS[i])/float(self.sent[i])))
            self.sumder = self.sumder + self.der[i]
        self.avgDER = (self.sumder)/nrBS

        self.throughput = 8 * float(self.RecPacketSize) / self.TotalPacketAirtime
        self.EffectEnergyConsumPerByte = float(self.TotalEnergyConsumption) / self.RecPacketSize
    
    def results_show(self):
        # print stats and save into file
        print ("Number of received packets (independent of right base station)", len(recPackets))
        print ("Number of collided packets", len(collidedPackets))
        print ("Number of lost packets (not correct)", len(lostPackets))
        print ("Total number of packets sent: ", self.sumSent)

        for i in range(0, nrBS):
            print ("send to BS[",i,"]:", self.sent[i]) # number of packets sent to each BS
        print ("sent packets: ", packetSeq) # total sent packets of nodes
        for i in range(0,nrBS):
            print ("packets at BS",i, ":", len(packetsRecBS[i])) # received packets of each BS
        print ("overall received at right BS: ", self.sum)

        for i in range(0, nrBS):
            print ("DER BS[",i,"]: {:.2f}".format(self.der[i]))    
        print ("avg DER: {:.2f}".format(self.avgDER))
        print ("DER with 1 network:{:.2f}".format(self.derALL))

        print ("Total payload size: {} bytes".format(self.TotalPacketSize))
        print ("Received payload size: {} bytes".format(self.RecPacketSize))
        print ("Total transmission energy consumption: {:.3f} Joule".format(self.TotalEnergyConsumption))
        print ("Network throughput: {:.3f} bps".format(self.throughput))
        print ("Effective energy consumption per byte: {:.3e} Joule".format(self.EffectEnergyConsumPerByte))

        # this can be done to keep graphics visible
        if (graphics == 1):
            input('Press Enter to continue ...')
    
    def simulation_record(self):
        result_file_name = self.file_name+"-result.txt"
        file_path = os.path.join(self.folder_path, result_file_name)
        with open(file_path, 'w') as file:
            file.write('Simulation start at {}'.format(self.simstarttime))
            file.write(' and end at {}\n'.format(self.simendtime))
            file.write('--------Parameter Setting--------\n')
            file.write('Nodes per base station: {}\n'.format(nrNodes))
            file.write('Packet generation interval: {} ms\n'.format(avgSendTime))
            file.write('LoRa parameters allocation type: {}\n'.format(allocation_type))
            file.write('LoRa parameters allocation method: {}\n'.format(allocation_method))
            file.write('Simulation duration: {} h\n'.format(int(simtime/3600000)))
            file.write('Number of gateways: {}\n'.format(nrBS))
            if full_collision == 1:
                file.write('Collision check mode: Full Collision Check\n')
            else:
                file.write('Collision check mode: Simple Collision Check\n')
            if directionality == 1:
                file.write('Antenna type: Directional antenna\n')
            else:
                file.write('Antenna type: Omnidirectional antenna\n')
            file.write('Number of networks: {}\n'.format(nrNetworks))
            file.write('Network topology radius: {} m\n'.format(radius))
            file.write('Packet payload size: {}\n\n'.format(PayloadSize))

            file.write('--------Simulation Results--------\n')
            file.write("Total number of packets sent: {}\n".format(self.sumSent))
            file.write("Number of received packets: {}\n".format(len(recPackets)))
            file.write("Number of collided packets: {}\n".format(len(collidedPackets)))
            file.write("Number of lost packets: {}\n".format(len(lostPackets)))
            for i in range(0, nrBS):
                file.write("send to BS[{}".format(i))
                file.write("]: {}\n".format(self.sent[i])) # number of packets sent to each BS
            for i in range(0,nrBS):
                file.write("packets at BS {}".format(i))
                file.write(": {}\n".format(len(packetsRecBS[i]))) # received packets of each BS
            file.write("overall received at right BS: {}\n".format(self.sum))
            for i in range(0, nrBS):
                file.write("DER BS[".format(i))
                file.write("]: {:.2f}%\n".format(self.der[i]))    
            file.write("avg DER: {:.2f}%\n".format(self.avgDER))
            file.write("DER with 1 network: {:.2f}%\n".format(self.derALL))
            file.write("Total payload size: {} bytes\n".format(self.TotalPacketSize))
            file.write("Received payload size: {} bytes\n".format(self.RecPacketSize))
            file.write("Total transmission energy consumption: {:.3f} Joule\n".format(self.TotalEnergyConsumption))
            file.write("Network throughput: {:.3f} bps\n".format(self.throughput))
            file.write("Effective energy consumption per byte: {:.3e} Joule\n".format(self.EffectEnergyConsumPerByte))


    #
    # main discrete event loop, runs for each node
    # a global list of packet being processed at the gateway
    # is maintained
    #
    @staticmethod       
    def transmit(self,env,node):
        while True:
            # time before sending anything (include prop delay)
            # send up to 2 seconds earlier or later
            # simulate the time interval of discrete events happened in a system
            yield env.timeout(random.expovariate(1.0/float(node.period)))

            # time sending and receiving
            # packet arrives -> add to base station
            node.sent = node.sent + nrBS # number of packets sent by the node       
            global packetSeq
            packetSeq += nrBS # total number of packet of the network

            if allocation_type == "Local":
                node.Generate_Packet()

            for bs in range(0, nrBS):
                if (node in packetsAtBS[bs]):
                        print ("ERROR: packet already in")
                else:
                        # adding packet if no collision
                        if (checkcollision(node.packet[bs])==1):
                            node.packet[bs].collided = 1
                        else:
                            node.packet[bs].collided = 0
                        packetsAtBS[bs].append(node)
                        node.packet[bs].addTime = env.now
                        node.packet[bs].seqNr = packetSeq
                self.TotalPacketSize += node.packet[bs].PS
                self.TotalEnergyConsumption += float(node.packet[bs].tx_energy / 1000)
                self.TotalPacketAirtime += float(node.packet[bs].rectime / 1000)            
                
            # take first packet rectime, stop for rectime        
            yield env.timeout(node.packet[0].rectime)

            # if packet did not collide, add it in list of received packets
            # unless it is already in
            for bs in range(0, nrBS):
                if node.packet[bs].lost:
                    lostPackets.append(node.packet[bs].seqNr)
                else:
                    if node.packet[bs].collided == 0:
                        if (nrNetworks == 1):
                            packetsRecBS[bs].append(node.packet[bs].seqNr)
                        else:
                            # now need to check for right BS
                            if (node.bs.id == bs):
                                packetsRecBS[bs].append(node.packet[bs].seqNr)
                        # recPackets is a global list of received packets
                        # not updated for multiple networks        
                        if (recPackets):
                            if (recPackets[-1] != node.packet[bs].seqNr):
                                recPackets.append(node.packet[bs].seqNr)
                                self.RecPacketSize += node.packet[bs].PS
                        else:
                            recPackets.append(node.packet[bs].seqNr)
                            self.RecPacketSize += node.packet[bs].PS
                    else:
                        # XXX only for debugging
                        collidedPackets.append(node.packet[bs].seqNr)

            # complete packet has been received by base station
            # can remove it for next transmission
            for bs in range(0, nrBS):                    
                if (node in packetsAtBS[bs]):
                    packetsAtBS[bs].remove(node)
                    # reset the packet
                    node.packet[bs].collided = 0
                    # node.packet[bs].processed = 0
            


    