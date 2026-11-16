# FocusNoise

> Disclaimer: This script was vibe-coded using gpt-6-luna.

A very simple Python script that helps you focus in noisy environments by playing different types of noise through your computer speakers.

## Dependencies

FocusNoise uses the following Python packages:

- Click
- NumPy
- sounddevice

These dependencies are installed automatically when you install FocusNoise.

## Installation

Install FocusNoise from the project directory:

```bash
python -m pip install .
```

## Launching

Choose the noise type (`pink`, `brown`, `blue`, `green`, or `violet`):

```bash
focusnoise pink
```

Other supported types:

```bash
focusnoise brown
focusnoise blue
focusnoise green
focusnoise violet
```

Green noise is implemented as band-limited noise focused on the mid frequencies.

Set the output volume with `--volume` as an integer percentage from 0 to 100 (default: 100):

```bash
focusnoise pink --volume 40
```

Noise plays continuously until you stop the script with **Ctrl+C**.
