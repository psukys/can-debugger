from data_structure import CANNode, CANTestCase


class CANDiff:
    """A class for finding differences between testcase
    """
    def __init__(self):
        pass

    def get_diff_addrs(self, src, trg):
        """Gets the difference through data in the same addresses
        Args:
            src: test case to be compared against
            trg: test case to be compared
        Returns:
            a list of addresses which have differed data
            (or the address do not exist)
        """
        addrs = []
        #check the test case that is being compared
        for node in trg.nodes:
            #check if address exists in source
            src_addr = src.get_index_by_addr(node.addr)
            if src_addr is not None:
                #linear check for data difference 
                for idx, time in enumerate(node.data):
                    #check if there's any difference between data points
                    if not any(src.nodes[src_addr].data[t] == node.data[time]
                               for t in src.nodes[src_addr].data):
                        addrs.append(node.addr)
                        break
            else:
                addrs.append(node.addr)
        return addrs