# Benchmark for Isomap Reduction

* [Installation](#installation)
* [Usage](#usage)
* [Examples](#examples)

## Installation
Clone this repository or download the release from the releases page.

## Usage
iso_bench.py [-h] (-l PATH_TO_DATASET | -g DATA_TYPE [DATA_TYPE ...]) [--clean-cython] [--clean-results] [-i N_RUNS] [-t N_THREADS] [-s N_SAMPLES [N_SAMPLES ...]] [-f N_FEATURES [N_FEATURES ...]]

options:

 - -h, --help  
	 - show this help message and exit

  

 - -l PATH_TO_DATASET, --load PATH_TO_DATASET
	 - Loads a dataset file PATH_TO_DATASET_FILE needs to be relative, if located in datasets folder, only file name can be mentioned
	 - -g DATA_TYPE [DATA_TYPE ...], --generate DATA_TYPE [DATA_TYPE ...]
		 - Generates data using the scikit-learn library DATA_TYPES will be separated by spaces Supported DATA_TYPES are: 
			 - blobs, 
			 - gaussian_quantiles, 
			 - friedman1, friedman2, friedman3, 
			 - moons, 
			 - swiss_roll,
			 -  s_curve
 - --clean-cython
	 - Removes compiled files, forcing total recompilation before execution
 - --clean-results
	 - Removes previous benchmark results from results folder
 - -i N_RUNS, --runs-per-iteration N_RUNS
	 - Number of runs per set of parameters (default=1)
 - -t N_THREADS, --max-threads N_THREADS
	 - Maximum number of threads to use (default=1)
 - -s N_SAMPLES [N_SAMPLES ...], --samples N_SAMPLES [N_SAMPLES ...]
	 - Maximum number of threads to use (default=1)
 - -f N_FEATURES [N_FEATURES ...], --features N_FEATURES [N_FEATURES ...]
	 - Set of features used for data generation (default=50)

## Examples

    ./iso_bench.py -g blobs -s 50 100 200 400 -f 50 100 -t 15
Computes Isomap from datasets generated from scikit-learn's blobs, following these shapes : (50,50) (100,50) (200,50) (400,50) (50,100)... using 15 threads maximum.

	./iso_bench.py -l Data_Pam50.csv -t 8 -i 10 --clean-results --clean-cython
Deletes previous results files and folder, as well as results of compilation by Cython & Computes Isomap from dataset file "Data_Pam50.csv" 10 times.