# The raspberry pi works on digital inputs where as the gas sensor MQ135 provides the analog output, hence in order to bridge the conversion from analog to digital 
# MCP3008 10 Bit ADC is used.

from spidev import SpiDev                                   #Spidev is a python module that allows us to interface with the Pi’s SPI bus.

class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000                     # Unless the spi.max_speed_hz field is a value accepted by the driver, the script will fail when you run it.

    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz
    
    ############ Function to read SPI data from MCP3008 chip ############### 
    # Read the current value of the specified ADC channel (0-7). 
    # The values can range from 0 to 1023 (10-bits).
    ########################################################################
    
    def read(self, channel = 0):                            # CH-0 (Channel-0) of MCP3008 is used to acquire input from the MQ135              
        cmd1 = 4 | 2 | (( channel & 4) >> 2)                # Input configuration for CH-0 to be set as 'single ended' which is 1000 as per the datasheet.
        cmd2 = (channel & 3) << 6

        adc = self.spi.xfer2([cmd1, cmd2, 0])
        data = ((adc[1] & 15) << 8) + adc[2]
        return data
            
    def close(self):
        self.spi.close()
