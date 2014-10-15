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
        # check the test case that is being compared
        for node in trg.nodes:
            # check if address exists in source
            src_addr = src.get_index_by_addr(node.addr)
            if src_addr is not None:
                # linear check for data difference
                for d in node.data:
                    # check if there's any difference between data points
                    if not src.nodes[src_addr].data_exists(d.data):
                        addrs.append(node.addr)
                        break
            else:
                addrs.append(node.addr)
        return addrs

    def get_diff_data(self, src, trg, addr):
        """Gets the difference through differentiated addresses
        Args:
            src: test case to be compared against
            trg: test case to be compared
        Returns:
            a list of tuples where src diff data and trg diff data is
        """
        idx = src.get_index_by_addr(addr)
        if idx is not None:
            src_data = src.nodes[idx]
        else:
            src_data = None

        idx = trg.get_index_by_addr(addr)
        if idx is not None:
            trg_data = trg.nodes[idx]
        else:
            trg_data = None

        return (src_data, trg_data)

    def get_diffs_data(self, src, trg):
        """Gets the difference through differentiated addresses
        Args:
            src: test case to be compared against
            trg: test case to be compared
        Returns:
            a list of tuples where src diff data and trg diff data is
        """
        data = []  # empty tuple
        diff_addrs = self.get_diff_addrs(src, trg)

        for addr in diff_addrs:
            data.append(self.get_diff_data(src, trg, addr))

        return data
