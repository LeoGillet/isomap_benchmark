#!/usr/bin/env python3

import argparse
import os
import platform
import sys
from datetime import date, datetime
from os.path import exists, isdir
from timeit import default_timer as timer

import pyximport

# TODO:
#	✅ Plot Isomap computation using OOP & Modules
#	✅ Loop over different test parameters
#	✅ Save figures & execution logs
#	✅ Implement multithreading
#  	✅ Cython implementation for faster data generation
#		✅ Integrate isolated data gen. module
#	✅ Add multiple data generation methods
#		✅ Blobs (sklearn.datasets.make_blobs)
#		✅ Regression (sklearn.datasets.make_regression)
#		✅ Gaussian Quantiles (sklearn.datasets.make_gaussian_quantiles)
#		✅ Swiss Roll (sklearn.datasets.make_swiss_roll)
#		✅ Friedman1 (sklearn.datasets.make_friedman1)
#		✅ Friedman2 (sklearn.datasets.make_friedman2)
#		✅ Friedman3 (sklearn.datasets.make_friedman3
#		❎ Circles (sklearn.datasets.make_circles)
#		❎ Biclusters (sklearn.datasets.make_biclusters)
#		✅ Moons (sklearn.datasets.make_moons)
#		✅ S Curve (sklearn.datasets.make_s_curve)
#		❎ Sparse Uncorrelated (sklearn.datasets.make_sparse_uncorrelated)
#	✅ Add metrics
#		✅ Jaccard Score (manual)
#		❎ F1 Score
#	✅ Run from CLI with parameters

global OS_WINDOWS, IMPLEMENTED_DATATYPES, DOC
OS_WINDOWS = platform.system() == "Windows"
IMPLEMENTED_DATATYPES = ("blobs",
						 "gaussian_quantiles",
						 "friedman1", "friedman2", "friedman3",
						 "moons",
						 "swiss_roll",
						 "s_curve")
DOC = {
	"load": "Loads a dataset file\nPATH_TO_DATASET_FILE needs to be relative, if located in datasets folder, file name only can be mentioned",
	"generate": """Generates data using the scikit-learn library\n
					DATA_TYPES will be separated by spaces\n
					Supported DATA_TYPES are: %(choices)s""",
	"clean": "Removes compiled files, forcing total recompilation before execution",
	"rps": "Number of runs per set of parameters (default=%(default)s)",
	"threads": "Maximum number of threads to use (default=%(default)s)",
	"samples": "Set of samples used for data generation (default=%(default)s)",
	"features": "Set of features used for data generation (default=%(default)s)"}


def _dataset_exists(filepath):
	if exists(filepath):
		return filepath
	if exists(str("datasets/" + filepath)):
		return "datasets/" + filepath
	return None


def _create_directory(dirname) -> bool:
	"""
	Creates directory with given path
	:param dirname: relative path to directory
	:return: bool:  returns True if directory has been created
					returns False if directory already exists or if any other error occured
	"""
	try:
		os.mkdir(f"{dirname}")
		return True
	except FileExistsError:
		return False
	except Exception as e:
		print("[ERROR] Unknown error occurred when creating directory", dirname)
		print(e)
		sys.exit(101)


def _clear_std():
	if OS_WINDOWS:
		os.system("cls")
	else:
		os.system("clear")


def init_folders() -> str:
	"""
	Creates directory where benchmark results will be stored
	:return:
	"""
	print("Creating results directory...") if _create_directory("results") else ''

	today = date.today().strftime("%d%m%y")
	dirname = today + "_"
	dirnum = 1
	while not _create_directory(f"results/{dirname}{dirnum}"):
		dirnum += 1
	dirname += str(dirnum)
	dirname += '/'

	print("[INFO] Bench files will be saved in directory : results/" + dirname)
	return dirname


def clean_results() -> None:
	if isdir('results'):
		os.system("del results/") if OS_WINDOWS else os.system("rm -rf results")


def clean_cython() -> None:
	"""
	Deletes previous compilation results from directory, forcing regeneration
	"""
	if OS_WINDOWS:
		os.system("del modules/benchmarks.c")
		os.system("del modules/objects.c")
		os.system("del *.cpython*")
	else:
		os.system("rm modules/benchmarks.c")
		os.system("rm modules/objects.c")
		os.system("rm *.cpython*")
	os.system("python3 setup.py build_ext --inplace")


if __name__ == '__main__':
	arg_parser = argparse.ArgumentParser(description="Benchmark for Isomap Reduction")
	group = arg_parser.add_mutually_exclusive_group(required=True)
	group.add_argument("-l", "--load", help=DOC.get("load"), metavar="PATH_TO_DATASET")
	group.add_argument("-g", "--generate", help=DOC.get("generate"), metavar="DATA_TYPE", nargs='+',
					   choices=IMPLEMENTED_DATATYPES)
	arg_parser.add_argument("--clean-cython", dest="clean_cython", action="store_true")
	arg_parser.add_argument("--clean-results", dest="clean_results", action="store_true")
	arg_parser.add_argument("-i", "--runs-per-iteration", dest='rps', metavar='N_RUNS', default=1, type=int)
	arg_parser.add_argument("-t", "--max-threads", dest='threads', metavar='N_THREADS', default=1, type=int)
	arg_parser.add_argument("-s", "--samples", metavar="N_SAMPLES", default=100, type=int, nargs='+')
	arg_parser.add_argument("-f", "--features", metavar="N_FEATURES", default=50, type=int, nargs='+')

	args = arg_parser.parse_args()

	args.samples = set(args.samples) if type(args.samples) is list else [args.samples]
	args.features = set(args.features) if type(args.features) is list else [args.features]

	### Compares and compiles quietly with Cython here
	pyximport.install(setup_args={"script_args": ["--quiet"]}, build_in_temp=True)
	# pyximport.install(setup_args={"script_args": ["--verbose"]})
	### Late import after compilation
	from modules.benchmarks import run_benchmark, run_dataset

	if args.clean_cython:
		clean_cython()
	if args.clean_results:
		clean_results()

	_clear_std()
	dirname = init_folders()
	runs_per_set = args.rps
	max_threads = args.threads
	start = end = None

	if args.load:  # User loads dataset from file path
		dataset = _dataset_exists(args.load)
		start = timer()
		run_dataset(dataset_name=dataset, rps=runs_per_set, threads=max_threads, dirname=dirname)
		end = timer()

	if args.generate:  # User generates data
		start = timer()

		run_benchmark(samples_list=args.samples, features_list=args.features, datatype_list=args.generate,
					  dirname=dirname, threads=max_threads, rps=runs_per_set)
		end = timer()  # Specific dataset is mentioned in launch arguments
	with open(f"results/{dirname}bench_info.txt", 'w') as file:
		file.write(f"Bench {date.today().strftime('%d%m%y')} {datetime.now().strftime('%H:%M:%S')}\n")
		file.write(f"Total time : {round(end - start, 5)} seconds\n")
		file.write(f"Max threads : {max_threads}\n")
		file.write(f"Samples : {str(args.samples)}\n")
		file.write(f"Components : {str(args.features)}\n")
		file.write(f"Data types : {str(args.generate)}\n")
