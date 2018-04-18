from circuitlib import Circuit
from matplotlib import pyplot as plt
import numpy as np

class AZX():
	def __init__(self, n):
		
		vs = [('vss', '1', None, 10)]
		nd = [str(i + 1) for i in range(2 * n)]
		rs = []
		ind = []
		cp = []
		iss = []
		for i in range(n):
			rs += [('res', str(2 * i + 1), str(2 * i + 2), 0.01 * (i + 1))]
			ind += [('ind', str(2 * i + 2), str(2 * i + 3), 0.003 * (i + 1))]
			cp += [('cap', str(2 * i + 2), str(2 * i + 3), 0.015 * (i + 1))]
		print nd, rs, ind, cp, vs, iss
		"""
		nd = ['1', '2', '3']
		rs = [('res', '1', '2', 0.02)]
		ind = [('ind', '2', '3', 0.3)]
		cp = [('cap', '3', None, 0.000015)]
		vs = [('vss', '1', None, 25)]
		iss = []
		"""
		self.circ = Circuit(nd, rs, ind, cp, vs, iss)
	def find_peak(self):
		margin = 500
		cur_best_loc = 500
		center = cur_best_loc
		cur_best = 0

		while margin > 0.01:
			for frq in np.arange(max(center - margin, 0), center + margin, margin / 500.0):
				w = 2 * np.pi * frq
				score = abs(self.circ.ac_analyze(w)[-1, 0])
				#if margin == 500:
				#	print frq, score
				if score > cur_best:
					cur_best_loc = frq
					cur_best = score
			center = cur_best_loc
			margin = margin / 10.0

		print center
		print cur_best

	def sketch(self):
		log = []
		min_f = 1
		max_f = 200
		for frequency in np.arange(min_f, max_f, (max_f - min_f) / 1000.0):
			w = 2 * np.pi * frequency
			mag = abs(self.circ.ac_analyze(w)[1, 0])
			log.append((frequency, mag))
		#for l in log:
		#	print l[0], l[1]
		plt.plot(*zip(*log))
		plt.show()


def example():
	nd = ['1', '2', '3']
	rs = [('res', '1', '2', 0.02)]
	ind = [('ind', '2', '3', 0.3)]
	cp = [('cap', '3', None, 0.000015)]
	vs = [('vss', '1', None, 25)]
	iss = []
	circ = Circuit(nd, rs, ind, cp, vs, iss)

	# print circ.dc_analyze()

	min_f = 0
	max_f = 0

	while min_f != 203948576:
		log = []
		min_f = input("Input lower frequency bound. Type 203948576 to exit\n")
		max_f = input("Input upper frequency bound.\n")
		for frequency in np.arange(min_f, max_f, (max_f - min_f) / 100.0):
			f = 2 * np.pi * frequency
			res = circ.ac_analyze(f)
			mag = abs(res[-1, 0])
			log.append((frequency, mag))
		plt.plot(*zip(*log))
		plt.show()

def main():
	# example()
	num = 2
	print num
	test = AZX(num)
	test.find_peak()
	test.sketch()

if __name__ == '__main__':
	main()