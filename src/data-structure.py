from datetime import datetime

class CANNode:
    """The most simplest data structure
    which is self implied by CAN dump
    """
    def __init__(self, time=None, addr=None, data=None):
        """Initializer
        Args:
            time: time at which the data dump was taken
        """
        if time:
            self.time = time

        if addr:
            self.addr = addr

        if data:
            self.data = data

    def parse_line(self, line):
        """Parses a string filled with data
        in such format:
        (123456.789) interface1 0C94#001A
        The number in clauses is unix timestamp
        interface1 - interface name
        hex number before hash (#) - address
        hex number after hash (#) - data

        Args:
            line: string filled with data
        """
        m = re.match("\((\d+\.\d+)\) (\S+) ([0-9a-fA-F]+)#([0-9a-fA-F]+)", line)
        #first match group: time
        self.time = datetime.utcfromtimestamp(float(m.group(1)))
        #second match group is not needed yet,
        #but leaving it for later implementation
        self.addr = m.group(3).strip()
        self.data = m.group(4).strip()

    def __str__(self):
        return "{0} {1}:{2}".format(self.time,
                                    self.addr,
                                    self.data)

class 