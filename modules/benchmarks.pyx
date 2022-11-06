import threading
from time import sleep
from os.path import exists

import plots
from modules.objects import *

import scipy
import warnings
warnings.filterwarnings(action='ignore', category=scipy.sparse.SparseEfficiencyWarning) # setting ignore as a parameter and further adding category


dn = "./"

def thread_bench(func, args):
	"""
	Starts a thread with the given function as target.
	:param func: target function
	:param args: target function's arguments
	:return: None
	"""
	thr = threading.Thread(target=func, args=args)
	thr.start()

def start_bench(samples, features, datatype, rps, showfig=False, savefig=False, data=None):
	"""
	Generates data, test conditions and	tarts the computation of the Isomap algorithm
	with the given parameters
	:param samples: number of samples to generate
	:param features: number of components/features the generated data describing the data
	:param datatype: type of data generated ("blobs", "regression", "gaussian quantiles")
	:param showfig: bool: shows figure using matplotlib backend (slows execution time)
	:param savefig: bool: saves figure using matplotlib, needs to show figure as well.
	:return: None
	"""
	data = TestData(n_samples=samples, n_features=features, datatype=datatype, centers=5)
	neighbors = [int(samples / 5)]
	results = list()

	for n in neighbors:
		for r in range(rps):
			result, execution_info = data.compute_isomap(n, features)
			results.append(result)
			fp = "run_results.csv"
			write_execution_info_to_file(execution_info, fp)
	if data.y is not None:
		colors = data.y
		plots.bench_neighbors(results, colors, file_prefix=fp, title=neighbors,
							  savefig=savefig) if showfig else None

def write_execution_info_to_file(info: str, file_name):
	"""
	Writes Isomap computation process information such as execution time, and used parameters
	:param info: str: information to write to file
	:param file_name: str: name of file
	:return: None
	"""
	if not exists(f"results/{dn}/{file_name}"):
		with open(f"results/{dn}/{file_name}", 'w') as f:
			f.write(
				"DATATYPE	N_SAMPLES	N_FEATURES	N_NEIGHBORS	N_COMPONENTS	TIME_ISOMAP	TIME_METRICS	SCORE_JACCARD\n")
	with open(f"results/{dn}/{file_name}", 'a') as f:
		f.write(info)

def process_dataset(dataset_name, dirname):
	data = TestData(datatype="custom", dataset=dataset_name)
	neighbors = [int(data.n_samples / 10)]
	results = list()

	for n in neighbors:
		result, execution_info = data.compute_isomap(n, data.n_features)
		results.append(result)
		fp = dirname+"run_results.csv"
		write_execution_info_to_file(execution_info, fp)

def run_dataset(dataset_name, rps=1, threads=5, dirname="default/"):
	for _ in range(rps):
		thread_bench(process_dataset, args=(dataset_name, dirname,))

def run_benchmark(samples_list=[500], features_list=[50], datatype_list=["blobs"], dirname="default/", showfig=False, savefig=False,
				  threads=5, rps=1):
	_warned = False
	global dn
	dn = dirname
	current_run = 0
	total_runs = len(samples_list) * len(features_list) * len(datatype_list) * rps

	for samples in samples_list:
		for components in features_list:
			for datatype in datatype_list:
				current_run += rps
				print(
					f"Runs (x{rps}) {current_run}/{total_runs} | samples={samples} | components={components} | datatype={datatype}")
				while threading.active_count() >= threads + 1:
					print(f"[WARN] {threads}+ threads active.. Waiting") if not _warned else ""
					sleep(1)
				_warned = False
				thread_bench(start_bench, args=(samples, components, datatype, rps, showfig, savefig))
