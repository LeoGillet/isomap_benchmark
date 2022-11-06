import warnings
from timeit import default_timer as timer

from sklearn.manifold import Isomap
from sklearn.metrics import f1_score
from sklearn.neighbors import BallTree
from sklearn.cluster import KMeans
import sklearn.datasets as skds

import pandas as pd
from statistics import mean

def _load_dataset(filename="dataset.csv", **kwargs):
	return pd.read_csv(filename, **kwargs)

def _load_pam():
	pam50 = _load_dataset(filename="Data_Pam50.csv", index_col=0)
	print(pam50.head())
	pam50.drop('subtype', axis=1, inplace=True)
	return pam50

def _compute_balltree(x_before, x_after, n_features):
	return BallTree(x_before, leaf_size=2), BallTree(x_after, leaf_size=2)

def jaccard_index(list_original, list_predicted):
	intersection = [value for value in list_predicted if value in list_original]
	union = list(set(list_predicted) | set(list_original))
	return intersection, union


class TestData:
	def __init__(self, n_samples=100, n_features=2, centers=5, datatype="blobs", dataset=None):
		self.n_samples = n_samples
		self.n_features = n_features
		self.datatype = datatype
		self.centers = centers
		self.jaccard_score = 0
		self.info = ""
		self.x = self.y = None
		if datatype == "custom":
			self.x = _load_dataset(filename=dataset)
			self.n_samples, self.n_features = self.x.shape
			self.n_components = self.n_features
		elif datatype == "blobs":
			self.x, self.y = skds.make_blobs(n_samples=n_samples,
											 n_features=n_features,
											 centers=centers)
		elif datatype == "gaussian_quantiles":
			self.x, self.y = skds.make_gaussian_quantiles(n_samples=n_samples,
														  n_features=n_features)
		elif datatype == "swiss_roll":
			self.x, self.y = skds.make_swiss_roll(n_samples)
		elif datatype == "friedman1":
			self.x, self.y = skds.make_friedman1(n_samples, n_features=n_features)
		elif datatype == "friedman2":
			self.x, self.y = skds.make_friedman2(n_samples)
		elif datatype == "friedman3":
			self.x, self.y = skds.make_friedman3(n_samples)
		elif datatype == "moons":
			self.x, self.y = skds.make_moons(n_samples)
		elif datatype == "s_curve":
			self.x, self.y = skds.make_s_curve(n_samples)
		else:
			print(f"Data type '{datatype}' not supported, generating blobs instead...")
			self.x, self.y = skds.make_blobs(n_samples,
											 n_features,
											 centers)
			self.isomap = None
			self.x_transformed = None

	def compute_isomap(self, n_neighbors, n_components, p_neighbors=0.25) -> Isomap:
		jaccard = list()
		start_isomap = timer()
		self.isomap = Isomap(path_method='FW')
		self.x_transformed = self.isomap.fit_transform(self.x)
		end_isomap = timer()
		start_metrics = timer()
		n_neighbors_keep = int(len(self.x) * p_neighbors)
		balltree_before, balltree_after = _compute_balltree(self.x, self.x_transformed, n_features=n_components)
		ind = balltree_before.query(self.x, k=n_neighbors, return_distance=False).tolist()
		ind_transformed = balltree_after.query(self.x_transformed, k=n_neighbors_keep, return_distance=False).tolist()
		try:
			for i in range(len(self.x)):
				inter, union = jaccard_index(ind[i], ind_transformed[i])
				jaccard.append(float(len(inter)) / float(len(union)))
			self.jaccard_score = mean(jaccard)
		except Exception as E:
			self.jaccard_score = None
			print("[ERROR] Error occured when calculating Jaccard Score", E)
		end_metrics = timer()

		# DATATYPE	N_SAMPLES	N_FEATURES	N_NEIGHBORS	N_COMPONENTS	MAX_ITER	TIME_ISOMAP	TIME_METRICS SCORE_JACCARD
		info = f"""{self.datatype}\t{self.n_samples}\t{self.n_features}\t{n_neighbors}\t{n_components}\t{end_isomap - start_isomap}\t{end_metrics - start_metrics}\t{self.jaccard_score}\n"""
		self.info = info
		return self.x_transformed, info
