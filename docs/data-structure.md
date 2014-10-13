#Data structure

The world of CAN is matrix. It simply is, that's the first thing I thought when I started live CAN data dumping through Raspberry Pi CAN module into my green-black terminal.

The simplest structure that is obtained from the dump is as follows:
One dump line represents one data dump (DATA_DUMP) from and address(ADDRESS_WHERE_DATA_DUMP_CARE_FROM) at a specific time(TIME_DATA_DUMP_TAKEN), that is:

    <TIME_DATA_DUMP_TAKEN> ADDRESS_WHERE_DATA_DUMP_CAME_FROM DATA_DUMP

For receiving this data I used [candump from can-utils](https://gitorious.org/linux-can/can-utils). Regardless, you can always adapt data read by changing the source (See defaults.conf).

Next step is connecting this simple data-structure by a truly unique identifier: the address.

For implementation see [data-structure.py](../src/data-structure.py)
