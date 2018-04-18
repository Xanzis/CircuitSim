# Python implementation of the MNA algorithm.
# https://www.nada.kth.se/kurser/kth/2D1266/MNA.pdf used as reference

import numpy as np

class Circuit():
	def __init__(self, nodes, resistors, inductors, capacitors, voltage_sources, current_sources):
		# nodes is list of strings representing name of node
		# components should be (component type, start, end, relevant value)
		# resistances in conductances - NOT OHMS
		# res, ind, cap, vss, iss
		branches = resistors + inductors + capacitors + voltage_sources + current_sources
		self.nodes = nodes

		n_b = len(branches)
		n_n = len(nodes)

		# Compile incidence matrices. First R, then L, then C, then V, then I
		self.As = {}
		types = ['res', 'ind', 'cap', 'vss', 'iss']
		self.As['res'] = make_instance(resistors, n_n, nodes)
		self.As['ind'] = make_instance(inductors, n_n, nodes)
		self.As['cap'] = make_instance(capacitors, n_n, nodes)
		self.As['vss'] = make_instance(voltage_sources, n_n, nodes)
		self.As['iss'] = make_instance(current_sources, n_n, nodes)

		# Interesting note - for A, the sum of all As, Ai = 0 by Kirchoff, where i is the vector of branch currents

		# Compile component value matrices
		# To check on later - may throw error - dimensions and whatnot of I and E may be totally wrong

		self.I = make_vect(current_sources)
		self.E = make_vect(voltage_sources)
		self.G, self.Y_R = make_diag(resistors)
		self.L, self.Y_L = make_diag(inductors)
		self.C, self.Y_C = make_diag(capacitors)

	def dc_analyze(self):
		thingy11 = self.As['res'] * self.G * self.As['res'].T
		thingy12 = self.As['vss']
		thingy21 = self.As['vss'].T
		thingy22 = np.zeros((self.As['vss'].shape[1],) * 2)

		thingy = np.block([[thingy11, thingy12], [thingy21, thingy22]])

		ins = np.concatenate((-self.As['iss'] * self.I, self.E))
		values = np.linalg.inv(thingy) * ins

		return values

	def ac_analyze(self, freq):
		r_term = self.As['res'] * self.Y_R * self.As['res'].T
		l_term = self.As['ind'] * (self.Y_L / freq) * self.As['ind'].T
		c_term = self.As['cap'] * (self.Y_C * freq) * self.As['cap'].T

		thingy11 = r_term + l_term + c_term
		thingy12 = self.As['vss']
		thingy21 = self.As['vss'].T
		thingy22 = np.zeros((self.As['vss'].shape[1],) * 2)

		thingy = np.block([[thingy11, thingy12], [thingy21, thingy22]])

		ins = np.concatenate((-self.As['iss'] * self.I, self.E))
		values = np.linalg.inv(thingy) * ins

		return values

def make_instance(components, n_nodes, node_names):
	mat = np.matrix(np.zeros((n_nodes, len(components))))
	for b in range(len(components)):
		cur_branch = components[b]
		for n in range(n_nodes):
			cur_node = node_names[n]
			if cur_branch[1] == cur_node:
				mat[n, b] = 1
			elif cur_branch[2] == cur_node:
				mat[n, b] = -1
	return mat

def make_diag(components):
	mat = np.zeros(len(components))
	mat_y = np.zeros(len(components), dtype=np.complex_)
	for i in range(len(components)):
		mat[i] = components[i][3]
		if components[i][0] == 'res':
			mat_y[i] = res_admittance(components[i][3])
		if components[i][0] == 'ind':
			mat_y[i] = ind_admittance(components[i][3])
		if components[i][0] == 'cap':
			mat_y[i] = cap_admittance(components[i][3])
	return np.matrix(np.diag(mat)), np.matrix(np.diag(mat_y))

def make_vect(components):
	mat = np.zeros(len(components))
	for i in range(len(components)):
		mat[i] = components[i][3]
	return np.matrix(mat).T

def res_admittance(r):
	return complex(1.0 / r)

def ind_admittance(l):
	return complex(1.0 / (1j * l)) # missing frequency term - will need to divide by it once value is given

def cap_admittance(c):
	return complex(1j * c) # missing frequency term - will need to multiply by it once value is given

def main():
	nd = ['1', '2', '3']
	rs = [('res', '1', None, 1), ('res', '2', None, 1)]
	ind = [('ind', '2', '3', 2)]
	cp = [('cap', '1', '2', 3)]
	vs = [('vss', '3', None, 9)]
	iss = [('iss', None, '2', 1)]
	circ = Circuit(nd, rs, ind, cp, vs, iss)
	print circ.dc_analyze()
	for foo in range(1, 100):
		f = foo / 100.0
		res = circ.ac_analyze(f)
		print 'Freq: ' + str(f).zfill(4) + ' V1: ' + "{num.real:+0.04f} {num.imag:+0.04f}j".format(num=res[0, 0]) + \
		' V2: ' + "{num.real:+0.04f} {num.imag:+0.04f}j".format(num=res[1, 0]) + ' V3: ' + "{num.real:+0.04f} {num.imag:+0.04f}j".format(num=res[2, 0])\
		+ ' V Source Current: ' + "{num.real:+0.04f} {num.imag:+0.04f}j".format(num=res[3, 0])

if __name__ == '__main__':
	main()
