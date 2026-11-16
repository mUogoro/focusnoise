# FocusNoise

> Disclaimer: This script was vibe-coded using gpt-6-luna.

Very simple Python script that help you focusing on noisy environments by playing different types of noise on your computer speaker.

## Installation

Install FocusNoise from the project directory:

```bash
python -m pip install .
```

## Launching

Choose the noise type (`pink` or `brown`):

```bash
focusnoise pink
```

Or:

```bash
focusnoise brown
```

Set the output volume with `--volume` as an integer percentage from 0 to 100 (default: 100):

```bash
focusnoise pink --volume 40
```

Noise plays continuously until you stop the script with **Ctrl+C**.
