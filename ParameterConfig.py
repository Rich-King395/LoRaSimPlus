"""
    LoRaWAN Parameters
"""
import numpy as np
import math
import simpy
import matplotlib.pyplot as plt
# turn on/off graphics
graphics = 1

# do the full collision check
full_collision = False

# RSSI global values for antenna
dir_30 = 4
dir_90 = 2
dir_150 = -4
dir_180 = -3

# this is an array with measured values for sensitivity
# [SF,125KHz,250kHz,500kHz]
sf7 = np.array([7,-126.5,-124.25,-120.75])
sf8 = np.array([8,-127.25,-126.75,-124.0])
sf9 = np.array([9,-131.25,-128.25,-127.5])
sf10 = np.array([10,-132.75,-130.25,-128.75])
sf11 = np.array([11,-134.5,-132.75,-128.75])
sf12 = np.array([12,-133.25,-132.25,-132.25])

# receiver sensitivities of different SF and Bandwidth combinations
sensi = np.array([sf7,sf8,sf9,sf10,sf11,sf12])

# minimum SNR required for demodulation at different spreading factors
SNR_Req = np.array([-7.5,-10,-12.5,-15,-17.5,-20])

Carrier_Frequency = np.array([867100000,867300000,867500000,867700000,
                       867900000,868100000,868300000,868500000])

# adaptable LoRaWAN parameters to users
nrNodes = 100
nrBS = 1
radius = 2000
PayloadSize = 65
avgSendTime = 5000
allocation_type = "Local"
allocation_method = "random"
nrNetworks = 1
simtime = 3600000 * 24
directionality = 1
full_collision = 1

# global stuff
nodes = [] # list of nodes
env = simpy.Environment() # simulation environment

# max distance: 300m in city, 3000 m outside (5 km Utz experiment)
# also more unit-disc like according to Utz

# list of received packets
recPackets=[]
# list of collided packets
collidedPackets=[]
# list of lost packets
lostPackets = []

# global value of packet sequence numbers
packetSeq = 0

Ptx = 14 # packet transmission power
gamma = 2.32
d0 = 1000.0
std = 7.8           
Lpld0 = 128.95
GL = 0

# prepare graphics and add sink
if (graphics == 1):
    plt.ion()
    plt.figure()
    ax = plt.gcf().gca()

# list of base stations
bs = []
packetsAtBS = [] # Packets sent to each GW
packetsRecBS = [] # Packets received by each GW

class LoRaParameters:
    sf = 9
    cr = 1
    bw = 125
    tp = 14
    fre = 868000000
    PayloadSize = PayloadSize

        