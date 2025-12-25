# psrm

A process system resource usage monitor.

## Installation

Install psrm with uv (recommended), pip, or pipx:

```shell
# With uv.
uv tool install psrm@latest  # Install psrm globally.

# With pip.
pip install psrm

# With pipx.
pipx install psrm
```

## Usage

Launch psrm to monitor the specified process; the default monitoring interval is 1 seconds.

```shell
# As a command line tool.
psrm 12345

# As a installed package.
python -m psrm 12345 1.5
```

psrm will continuously record the process's system resource usage and save the data to a CSV file at fixed intervals.

Visualize the recorded data:

```shell
from psrm.utils import visualize_data

visualize_data("20251225_202020_953721bb.csv")
```

The charts intuitively display how process resource usage changes over time.
