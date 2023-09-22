from concurrent import futures
import csv
from inspect import signature
from pathlib import Path
import re
from subprocess import Popen
from typing import Callable, Union, List, Any


def _run_gem5(gem5_executable_path: str, gem5_args, output_dir: str, run_num: int):
    """Run gem5 with the given arguments and output directory. Meant for use with the ProcessPoolExecutor"""
    # Create the output directory
    output_path = Path(output_dir + f'/run_{run_num}')
    output_path.mkdir(parents=True, exist_ok=True)
    # Run gem5
    Popen(f'{gem5_executable_path} {gem5_args} --outdir={output_dir}', shell=True).wait()


def run_gem5_samples(gem5_executable_path: str, gem5_args: str, output_dir: str, num_samples: int = 1,
                     num_simultaneous_runs: int = 1):
    """Run gem5 with the specified number of samples. The runs are automatically numbered as run_0, run_1, etc. The run
    value is incremented to be higher than the current highest value in the current output directory.
    :param gem5_executable_path: path to the gem5 executable
    :param gem5_args: all arguments to pass to gem5
    :param output_dir: path to the output directory
    :param num_samples: number of additional samples to run
    :param num_simultaneous_runs: number of runs to run simultaneously (each run is a single-threaded process)
    """
    # Change the output directory into a Path object
    output_path = Path(output_dir)

    # Check if the output directory already contains directories labelled run_0, run_1, etc.
    pattern = r'^run_(\d+)$'

    # Initialize a variable to store the maximum X value
    max_x = -1

    # Iterate over every directory in the output directory
    for directory_path in output_path.iterdir():
        match = re.match(pattern, directory_path.name)

        if match:
            # Extract the X value and convert it to an integer
            x = int(match.group(1))

            # Update max_x if a higher value is found
            max_x = max(max_x, x)

    # The new run number is the maximum X value + 1
    new_run_start = max_x + 1

    args = []

    for i in range(new_run_start, new_run_start + num_samples):
        args.append([gem5_executable_path, gem5_args, output_dir, i])

    with futures.ProcessPoolExecutor(max_workers=num_simultaneous_runs) as pool:
        pool.map(_run_gem5, args)

    print(f'Finished running gem5 with {num_samples} samples')


def _return_self(val: Any) -> Any:
    """Helper function to directly pass through data. Used when directly reading metrics from stats.txt files."""
    return val


def _get_regex_list(keys: List[str]) -> List[str]:
    """Helper function to generate regex strings for reading metrics from stats.txt files."""
    return [f'(?<={key})\s+(\d+(?:\.\d+)?)' for key in keys]


def read_raw_results_simple(path: str, metric: Union[str, List[str]], metric_function: Callable = None) -> List[float]:
    """Reads metrics from all stats.txt files in a directory.
    :param path: Path to directory containing all gem5 outputs. The stats.txt files must be somewhere in this directory.
    :param metric: Name of the metric to read. If a list is provided, metric_function must be provided.
    :param metric_function: Function to apply to the metrics.
    """
    # If only a single metric is provided, then directly collect those values
    if isinstance(metric, str):
        metric = [metric]
        metric_function = _return_self
    else:
        # If a list of metrics is provided, then a function must be provided to calculate the final value per stats.txt
        if metric_function is None:
            raise ValueError('metric_function must be provided if metric is a list')
        if len(signature(metric_function).parameters) != len(metric):
            raise ValueError('metric_function must accept the same number of arguments as metric provides')

    # Generate regex strings for reading metrics from stats.txt files
    regex_list = _get_regex_list(metric)
    results = []

    # Search for all stats.txt files in the provided directory
    for stats_file in Path(path).rglob('stats.txt'):
        with open(stats_file, 'r') as f:
            file_contents = f.read()
        # Read out all metrics from the stats.txt file
        found_regex_vals = [float(re.search(regex, file_contents).group(0)) for regex in regex_list]
        # Apply the metric_function to the found metrics
        calculated_val = metric_function(*found_regex_vals)
        results.append(calculated_val)

    return results


def save_result_to_csv_simple(results: List[float], csv_title: str) -> None:
    """Saves a list of results to a csv file.
    :param results: List of results to save.
    :param csv_title: Name of the csv file to save the results to.
    """

    with open(csv_title, 'w') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerow(results)


def read_csv_simple(csv_title: str) -> List[float]:
    """Reads a csv file and returns the values as a list.
    :param csv_title: Name of the csv file to read.
    """

    with open(csv_title, 'r') as file:
        reader = csv.reader(file, dialect='excel')
        string_vals = next(reader)
        values = [float(s) for s in string_vals]
        return values
