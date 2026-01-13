import subprocess
import io

import numpy as np


def run_command_o(
    command: list[str],
) -> np.ndarray:
    """Run a TISEAN command without input and catch the output as a numpy array

    Args:
        command (list[str]): The tisean command.

    Raises:
        RuntimeError: Outputs stderr of the tisean program if the program does not run successfully.

    Returns:
        np.ndarray: Output of the tisean program.
    """
    # Run subprocess
    proc = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Capture output
    stdout, stderr = proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(f"Subprocess failed: {stderr}")

    # Convert output back to NumPy array
    # Use StringIO again to read it as a file-like object
    output_array = np.loadtxt(io.StringIO(stdout))

    return output_array


def run_command_io(
    command: list[str],
    input_array: np.ndarray,
    verbose: bool = False,
) -> np.ndarray:
    """Run a TISEAN command with input and catch the output as a numpy array

    Args:
        command (list[str]): The tisean command.
        input_array (np.ndarray): The input array of dim <= 2.
        verbose (bool, optional): Whether to print stderr. Defaults to False.

    Raises:
        RuntimeError: Outputs stderr of the tisean program if the program does not run successfully.

    Returns:
        np.ndarray: Output of the tisean program
    """
    # Use a StringIO buffer to hold the text version
    input_buffer = io.StringIO()
    np.savetxt(input_buffer, input_array, fmt="%.6f")  # fmt optional
    input_text = input_buffer.getvalue()

    # Run subprocess
    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Send input and capture output
    stdout, stderr = proc.communicate(input_text)

    if proc.returncode != 0:
        raise RuntimeError(f"Subprocess failed: {stderr}")

    # Convert output back to NumPy array
    # Use StringIO again to read it as a file-like object
    output_array = np.loadtxt(io.StringIO(stdout))

    if verbose:
        print(stderr)

    return output_array
