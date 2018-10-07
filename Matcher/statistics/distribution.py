import unittest

from scipy.stats import norm


class EstimatedNormal:
	fifty_percent_z_score = 0.67448

	def __init__(self, mean, iqr_low, iqr_high):
		self.mean = mean
		self.iqr_low = iqr_low
		self.iqr_high = iqr_high
		self.stdev = self.estimated_standard_dev()

	def estimated_standard_dev(self):
		value_difference = self.iqr_high - self.mean
		return value_difference / EstimatedNormal.fifty_percent_z_score

	def calculate_z_score(self, test_score):
		difference_from_mean = test_score - self.mean
		return difference_from_mean / self.stdev

	def cdf(self, test):
		return norm.cdf(self.calculate_z_score(test))

	def pdf(self, test):
		return norm.pdf(self.calculate_z_score(test))


class TestDistribution(unittest.TestCase):

	def testCDF(self):
		estimatedNormal = EstimatedNormal(20, 18, 22)
		self.assertEqual(0.5, estimatedNormal.cdf(20))


if __name__ == "__main__":
	unittest.main()
