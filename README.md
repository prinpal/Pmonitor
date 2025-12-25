# pmonitor

A process system resource usage monitor.

## Installation

Install pmonitor with uv (recommended), pip, or pipx:

```shell
# With uv.
uv tool install pmonitor@latest  # Install pmonitor globally.

# With pip.
pip install pmonitor

# With pipx.
pipx install pmonitor
```

## Usage

Launch pmonitor to monitor the specified process; the default monitoring interval is 1 seconds.

```shell
# As a command line tool.
pmonitor 12345

# As a installed package.
python -m pmonitor 12345 1.5
```

pmonitor will continuously record the process's system resource usage and save the data to a CSV file at fixed intervals.

Visualize the recorded data:

```shell
from pmonitor.utils import visualize_data

visualize_data("20251225_202020_953721bb.csv")
```

The charts intuitively display how process resource usage changes over time.
