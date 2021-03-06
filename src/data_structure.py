from datetime import datetime
import re


class CANData:

    """The most simplest data structure
    which is self implied by CAN dump
    """

    def __init__(self, time=None, data=None):
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
        return "{0} {1}".format(self.time,
                                self.data)


class CANNode:

    """A little more advanced instance
    which groups data to addresses"""

    def __init__(self, addr=None):
        """Initializer
        Args:
            addr: the address representable in a string
        """
        self.addr = addr
        self.data = []

    def add_data(self, time, data):
        """Adds a single data point
        Args:
            time: time when can dump data point was taken
            data: data dump point
        """
        self.data.append(CANData(time, data))

    def data_exists(self, data):
        """Checks if specified data code is existant
        Args:
            data: data code
        Returns:
            True/False depending if existant
        """
        return any(d.data == data for d in self.data)

    def list_data(self):
        """List data list
        """
        string = ''
        last_data = None
        last_data_count = 0
        for idx, time in enumerate(sorted(self.data)):
            if last_data == self.data[time]:
                last_data_count += 1
            else:
                if last_data_count != 0:
                    string += " count {0}".format(last_data_count)
                last_data = self.data[time]
                last_data_count = 1
                string += "\n\t{0}: {1}".format(time, self.data[time])
        string += " count {0}\n".format(last_data_count)
        return string

    def __str__(self):
        return "Address: {0}, data points: {1}".format(self.addr,
                                                       len(self.data))


class CANTestCase:

    """CAN test case
    it is used for setting up a test case for reading data
    one test case resides some kind of can dump on specific interest
    this can dump would be compared unto other can dumps and thus 
    """

    def __init__(self, filepath):
        self.nodes = []
        # take last instance after spliting by dir
        self.filename = filepath.split("/")[-1]
        # parse the data into objects

        tmp_nodes = []
        with open(filepath) as f:
            for line in f:
                (time, addr, data) = self.parse_line(line)
                tmp_nodes.append((time, addr, data))

        # group up
        for time, addr, data in tmp_nodes:
            idx = self.get_index_by_addr(addr)
            if idx is not None:
                self.nodes[idx].add_data(time, data)
            else:
                n = CANNode(addr)
                n.add_data(time, data)
                self.nodes.append(n)

    def get_index_by_addr(self, addr):
        for idx, val in enumerate(self.nodes):
            if val.addr == addr:
                return idx

    def get_data(self, addrs):
        """
        Simply returns a list of data points under given addresses
        Args:
            addrs: a string or an array of strings
        Returns:
            Node or an array of nodes
        """
        if isinstance(addrs, list):
            nodes = []
            for addr in addrs:
                nodes.append(self.nodes[self.get_index_by_addr(addrs)])
        else:
            nodes = self.nodes[self.get_index_by_addr(addrs)]

        return nodes

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
        #m = re.match(
        #    "\((\d+\.\d+)\) (\S+) ([0-9a-fA-F]+)#([0-9a-fA-F]+)", line)
        m = line.split()
        time = '0'
        addr = m[1]
        data = ''.join(m[3:])
        return (time, addr, data)
