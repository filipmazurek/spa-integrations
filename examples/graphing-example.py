from spa.core import spa
from spa.properties import ThresholdProperty
from spa_integrations.gem5 import read_raw_results_simple
from spa_integrations.graphing import ci_spread_horizontal


def metric_func(l1_cache_misses, inst):
    # Simple Callable for l1 cache misses / 1k instructions
    return l1_cache_misses / (inst * 1000)


output_dir = './data/'
prob_threshold = 0.9
confidence = 0.9

# Read the gem5 sample results. We're interested in the rate of L1 cache misses / 1k instructions
# First create the metric list
metric_list = ['system.ruby.l1_cntrl0.L1Dcache.m_demand_misses', 'simInsts']

results = read_raw_results_simple(output_dir, metric_list, metric_func)

# Run SPA on our results to find the expected value. We are interested in the Threshold property
#   (row 1 of table 1 of https://doi.org/10.1145/3613424.3623785)
spa_result = spa(results, ThresholdProperty(), prob_threshold, confidence)

# Graph the final result as a horizontal confidence interval
ci_spread_horizontal([spa_result.confidence_interval], labels=['L1 cache misses / 1k instructions'])
