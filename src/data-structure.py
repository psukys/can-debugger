from datetime import datetime


class CANData:

    """The most simplest data structure
    which is self implied by CAN dump
    """

    def __init__(self, time=None, addr=None, data=None):
        """Initializer
        Args:
            time: time at which the data dump was taken
            data: specific data sent at that point
        """
        if time:
            self.time = time

        if data:
            self.data = data

    def __str__(self):
        return "{0} {2}".format(self.time,
                                self.data)


class CANNode:

    """A little more advanced instance
    which groups data to addresses"""

    def __init__(self, addr):
        """Initializer
        Args:
            addr: the address representable in a string
        """
        self.addr = addr
        self.data = {}

    def add_data(self, line):
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
        m = re.match(
            "\((\d+\.\d+)\) (\S+) ([0-9a-fA-F]+)#([0-9a-fA-F]+)", line)

        if m.group(3).strip() == self.addr:
            self.data.update({utcfromtimestamp(float(m.group(1))):
                              m.group(4).strip()})
        else:
            raise("Wrong address CAN address found in parsed line")

    def __str__(self):
        return "Address: {0}, data points: {1}".format(self.addr,
                                                       len(self.data))