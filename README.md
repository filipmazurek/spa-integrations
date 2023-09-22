# SPA Integrations
Integrations to make using SPA easier. This includes functions for running gem5, extracting data from gem5 `stats.txt` files, and graphing confidence intervals.

## Installing

First, please follow the installation instructions from the [SPA Library](https://github.com/filipmazurek/spa-library). Then, clone this repository and 

```bash
cd spa-integrations/
pip install ./
```

## Use
Check out the `examples/` directory for full workflow instructions. Also included is `examples/data/` which includes 22 samples of gem5 runs of the PARSEC benchmark `ferret`. Directly run analysis of this data by using an example script:

```bash
cd spa-integrations/examples/
python graphing-example.py
```
