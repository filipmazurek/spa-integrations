from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Union

ConfidenceInterval = namedtuple('ConfidenceInterval', ['low', 'high'])

_T_NUMBER = Union[int, float]


def distribution_graph(data: List[_T_NUMBER], quantiles: List[float], num_bins: int = None, xlabel: str = None,
                       title: str = None, output_file: str = None) -> None:
    """Create a distribution graph of the given data. Recommended for 50+ data points. As seen in figure 1 of
    https://doi.org/10.1145/3613424.3623785.
    :param data: The data to plot
    :param quantiles: What data quantiles to plot. Compared to SMC, this is 1-prob_threshold
    :param num_bins: How many bins to add in the histogram
    :param xlabel: xlabel on the graph
    :param title: title of the graph
    :param output_file: when using savefig, what the output file should be called
    """
    # Create a default number of bins value
    if num_bins is None:
        num_bins = int(len(data) / 10)

    # Create the histogram
    _, ax = plt.subplots()
    ax.hist(data, bins=num_bins, color='skyblue')

    # Add vertical lines for the percentiles
    for quantile in quantiles:
        ax.axvline(np.quantile(data, quantile), color='black', linestyle='--', label=f'F = {quantile}')

    # Set the axis labels, title, and legend
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Frequency')
    ax.set_title(title)
    ax.legend()

    # Show or save the graph
    if output_file is None:
        plt.show()
    else:
        plt.savefig(output_file)


def ci_spread_horizontal(conf_intervals: List[ConfidenceInterval], labels: List[str], xlabel: str = None,
                         title: str = None, output_file: str = None) -> None:
    """Create a horizontal confidence interval spread graph. As seen in figure 5 of https://doi.org/10.1145/3613424.3623785.
    :param conf_intervals: The confidence intervals to plot
    :param labels: The labels for each confidence interval
    :param xlabel: xlabel on the graph
    :param title: title of the graph
    :param output_file: when using savefig, what the output file should be called
    """

    _, ax = plt.subplots()

    # Plot the confidence intervals
    for i in range(len(conf_intervals)):
        low = conf_intervals[i].low
        high = conf_intervals[i].high
        ax.errorbar([(low + high) / 2], [i], xerr=[[(high - low) / 2]], fmt='', capsize=5,
                    label=labels[i])

    # Find the lowest value in the confidence intervals
    min_val = min([x.low for x in conf_intervals])
    # Find the highest value in the confidence intervals
    max_val = max([x.high for x in conf_intervals])
    ax.set_xlim(min_val - 0.1 * min_val, max_val + 0.1 * min_val)
    ax.set_ylim(-0.5, len(conf_intervals) - 0.5)
    # Set ticks and corresponding labels
    ax.set_yticks(range(len(conf_intervals)))
    ax.set_yticklabels(labels)
    # Set the axis labels, title, and legend
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.legend()

    # Show or save the graph
    if output_file is None:
        plt.show()
    else:
        plt.savefig(output_file)


def ci_spread_vertical(conf_intervals: List[ConfidenceInterval], labels: List[str], ylabel: str = None,
                       title: str = None, output_file: str = None) -> None:
    """A version of the confidence interval spread graph that plots the confidence intervals vertically.
    :param conf_intervals: The confidence intervals to plot
    :param labels: The labels for each confidence interval
    :param ylabel: ylabel on the graph
    :param title: title of the graph
    :param output_file: when using savefig, what the output file should be called
    """

    _, ax = plt.subplots()

    # Plot the confidence intervals
    for i in range(len(conf_intervals)):
        low = conf_intervals[i].low
        high = conf_intervals[i].high
        ax.errorbar([i], [(low + high) / 2], yerr=[[(high - low) / 2]], fmt='', capsize=5,
                    label=labels[i])

    # Find the lowest value in the confidence intervals
    min_val = min([x.low for x in conf_intervals])
    # Find the highest value in the confidence intervals
    max_val = max([x.high for x in conf_intervals])
    # Set graph limits
    ax.set_ylim(min_val - 0.1 * min_val, max_val + 0.1 * min_val)
    ax.set_xlim(-0.5, len(conf_intervals) - 0.5)
    # Set ticks and corresponding labels
    ax.set_xticks(range(len(conf_intervals)))
    ax.set_xticklabels(labels)
    # Set the axis labels, title, and legend
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()

    # Show or save the graph
    if output_file is None:
        plt.show()
    else:
        plt.savefig(output_file)
