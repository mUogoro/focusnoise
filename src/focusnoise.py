"""Play continuous colored noise through the default audio output."""

import click
import numpy as np
import sounddevice as sd


SAMPLE_RATE = 44100
BLOCK_SIZE = 4096


def pink_noise(size, state):
    """Generate pink noise with a stateful multi-pole filter."""
    white = np.random.uniform(-1.0, 1.0, size)
    output = np.empty(size, dtype=np.float32)
    b0, b1, b2, b3, b4, b5, b6 = state

    for i, sample in enumerate(white):
        b0 = 0.99886 * b0 + sample * 0.0555179
        b1 = 0.99332 * b1 + sample * 0.0750759
        b2 = 0.96900 * b2 + sample * 0.1538520
        b3 = 0.86650 * b3 + sample * 0.3104856
        b4 = 0.55000 * b4 + sample * 0.5329522
        b5 = -0.7616 * b5 - sample * 0.0168980
        output[i] = (b0 + b1 + b2 + b3 + b4 + b5 + b6 + sample * 0.5362) * 0.11
        b6 = sample * 0.115926

    state[:] = [b0, b1, b2, b3, b4, b5, b6]
    return output


def brown_noise(size, state):
    """Generate brown noise using a leaky integrator."""
    white = np.random.uniform(-1.0, 1.0, size)
    output = np.empty(size, dtype=np.float32)
    value = state[0]

    for i, sample in enumerate(white):
        value = (value + 0.02 * sample) / 1.02
        output[i] = value * 3.5

    state[0] = value
    return output


def blue_noise(size, state):
    """Generate blue noise by differentiating white noise."""
    white = np.random.uniform(-1.0, 1.0, size)
    samples = np.concatenate(([state[0]], white))
    state[0] = samples[-1]
    return np.diff(samples).astype(np.float32) * 0.6


def violet_noise(size, state):
    """Generate violet noise by twice differentiating white noise."""
    white = np.random.uniform(-1.0, 1.0, size)
    samples = np.concatenate(([state[0], state[1]], white))
    state[:] = samples[-2:].tolist()
    return np.diff(samples, n=2).astype(np.float32) * 0.35


def green_noise(size, state):
    """Generate band-limited noise focused on the mid frequencies."""
    white = np.random.uniform(-1.0, 1.0, size)
    output = np.empty(size, dtype=np.float32)
    previous_input, highpass_value, lowpass_value = state
    highpass_alpha = SAMPLE_RATE / (SAMPLE_RATE + 2.0 * np.pi * 180.0)
    lowpass_alpha = 1.0 - np.exp(-2.0 * np.pi * 1800.0 / SAMPLE_RATE)

    for i, sample in enumerate(white):
        highpass_value = highpass_alpha * (highpass_value + sample - previous_input)
        previous_input = sample
        lowpass_value += lowpass_alpha * (highpass_value - lowpass_value)
        output[i] = lowpass_value * 2.0

    state[:] = [previous_input, highpass_value, lowpass_value]
    return output


@click.command()
@click.argument("noise", type=click.Choice(("pink", "brown", "blue", "green", "violet")))
@click.option(
    "--volume",
    type=click.IntRange(min=0, max=100),
    default=100,
    show_default=True,
    help="Output volume as a percentage (0-100).",
)
def main(noise, volume):
    """Play noise to help mask distractions."""
    generators = {
        "pink": (pink_noise, 7),
        "brown": (brown_noise, 1),
        "blue": (blue_noise, 1),
        "green": (green_noise, 3),
        "violet": (violet_noise, 2),
    }
    generator, state_size = generators[noise]
    state = [0.0] * state_size

    try:
        with sd.OutputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32") as stream:
            while True:
                block = generator(BLOCK_SIZE, state) * (volume / 100.0)
                stream.write(block)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
