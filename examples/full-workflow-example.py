from spa.core import spa
from spa.properties import ThresholdProperty
from spa.util import min_num_samples
from spa_integrations.gem5 import read_raw_results_simple, run_gem5_samples
from spa_integrations.graphing import ci_spread_horizontal

gem5_executable_path = 'my/path/to/gem5.opt'
gem5_args = '--runscript="my/path/to/runscript.rcs"'
output_dir = 'my/output/dir/'


def metric_func(l1_cache_misses, inst):
    # Simple Callable for l1 cache misses / 1k instructions
    return l1_cache_misses / (inst * 1000)


# Decide the desired probability threshold and confidence level
prob_threshold = 0.9
confidence = 0.9

# Calculate the minium number of samples needed to reach a conclusion
min_samples = min_num_samples(prob_threshold, confidence)

# We will want to use at least 24 samples because we are running on a 24-core machine and want to use all of them
num_cores = 24
# The number of samples to run is completely up to the user, as long as they use at least the minimum number
num_samples = max(min_samples, num_cores)

# Run the samples
run_gem5_samples(gem5_executable_path, gem5_args, output_dir, num_samples, num_cores)

# Wait for gem5 to finish running

# Read the gem5 sample results. We're interested in the rate of L1 cache misses / 1k instructions
# First create the metric list
metric_list = ['system.ruby.l1_cntrl0.L1Dcache.m_demand_misses', 'simInsts']


results = read_raw_results_simple(output_dir, metric_list, metric_func)

# Run SPA on our results to find the expected value. We are interested in the Threshold property
#   (row 1 of table 1 of https://doi.org/10.1145/3613424.3623785)
spa_result = spa(results, ThresholdProperty(), prob_threshold, confidence)

# Graph the final result as a horizontal confidence interval
ci_spread_horizontal([spa_result.confidence_interval], labels=['L1 cache misses / 1k instructions'])
