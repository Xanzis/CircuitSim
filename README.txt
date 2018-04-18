A matrix-based solver for AC and DC analysis of an arbitrary circuit. Based on this paper: https://www.nada.kth.se/kurser/kth/2D1266/MNA.pdf

Use the paper for reference on what is happening inside the program and for a general overview of how to construct a circuit.

How to build a circuit using circuitlib.py:

component lists should be lists of tuples. Each tuple must start with the 3-letter abbreviation for the component type (res, ind, cap, vss, iss). The next two entries should be the name of the beginning node and the end node. Finally, the tuple should contain the relevant value (resistance, inductance, capacitance, voltage, or current). 

The node list should be a list of the names of nodes.

See the example circuit.py file for an example of how to build a circuit using the library.

the methods dc_analyze and ac_analyze each return a vector containing the node potentials and the current through the voltage sources (see the paper for reference on the exact format).

ac_analyze takes the frequency at which to analyze as an input.

Questions? Comments? Call or text me at (650) 924-5202
