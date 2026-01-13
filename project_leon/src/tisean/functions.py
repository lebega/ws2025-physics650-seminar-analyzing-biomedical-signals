import numpy as np

from tisean.wrapper import run_command_o, run_command_io


def henon(
    steps: int,
    a: float = 1.4,
    b: float = 0.3,
    x0: float = 0.0,
    y0: float = 0.0,
    transients: int = 10000,
) -> np.ndarray:
    """Generate 'steps' steps of the Henon map.

    Args:
        steps (int): Number of steps to generate.
        a (float, optional): Henon parameter 'a'. Defaults to 1.4.
        b (float, optional): Henon parameter 'b'. Defaults to 0.3.
        x0 (float, optional): Henon initial x-value. Defaults to 0.0.
        y0 (float, optional): Henon initial y-value. Defaults to 0.0.
        transients (int, optional): Number of initial steps to drop. Defaults to 10000.

    Returns:
        np.ndarray: Henon steps (transients) to (transients+steps).
    """
    command = [
        "henon",
        "-l",
        f"{steps}",
        "-A",
        f"{a}",
        "-B",
        f"{b}",
        "-X",
        f"{x0}",
        "-Y",
        f"{y0}",
        "-x",
        f"{transients}",
    ]
    output = run_command_o(command)

    return output


def addnoise(
    data: np.ndarray, lvl: float = 0.05, rel: bool = True, uniform: bool = False
) -> np.ndarray:
    """Add noise to a one dimensional timeseries.

    Args:
        data (np.ndarray): The data to be noised.
        lvl (float, optional): The noise level. Defaults to 0.05.
        rel (bool, optional): Whether to use relative noise.
            If True, noise level is relative to the data's standard deviation.
            If False, noise level is absolute. Defaults to True.
        uniform (bool, optional): Whether to use a uniform noise distribution.
            If True, noise is distributed uniformly.
            If False, produces Gaussian noise. Defaults to False.

    Returns:
        np.ndarray: Input data with added noise.
    """
    # ensure array compatibility
    _check_array(data)

    # run command
    command = ["addnoise", "-v" if rel else "-r", f"{lvl}"]
    if uniform:
        command.append("-u")
    output = run_command_io(command, data)

    return output


def delay(data: np.ndarray, m: int = 2, tau: int = 1) -> np.ndarray:
    """Create delay vectors from a one dimensional timeseries

    Args:
        data (np.ndarray): The data from which to create delay vectors.
        m (int, optional): The embedding dimension. Defaults to 2.
        tau (int, optional): The time step (delay). Defaults to 1.

    Returns:
        np.ndarray: Array of delay vectors of shape (len(data), m).
    """
    # ensure array compatibility
    _check_array(data)

    # run command
    command = ["delay", "-m", f"{m}", "-d", f"{tau}"]
    output = run_command_io(command, data)

    return output


def lazy(
    data: np.ndarray,
    iterations: int = 3,
    m: int = 2,
    eps: float = 0.1,
    rel: bool = True,
) -> np.ndarray:
    """Performs the simple (zero-order) noise reduction algorithm.

    Performs the noise reduction algorithm proposed by Schreiber 1993.

    Args:
        data (np.ndarray): One dimensional noisy timeseries.
        iterations (int, optional): Number of iterations. Defaults to 3.
        m (int, optional): Embedding dimension. Defaults to 2.
        eps (float, optional): Size if the initial epsilon neighbourhoods. Defaults to 0.1.
        rel (bool, optional): Whether epsilon is relative to the data's stddev. Defaults to True.

    Returns:
        np.ndarray: Noise reduced timeseries.

    References:
        Schreiber, Thomas (1993). “Extremely simple nonlinear noise-reduction method”.
        In: Physical Review E 47.4, p. 2401.
    """
    # ensure array compatibility
    _check_array(data)

    # run command
    command = [
        "lazy",
        "-m",
        f"{m}",
        "-v" if rel else "-r",
        f" {eps}",
        "-i",
        f"{iterations}",
    ]
    output = run_command_io(command, data)

    return output


def ghkss(
    data: np.ndarray,
    iterations: int = 5,
    m: int = 5,
    tau: int = 1,
    Q: int = 2,
    K: int = 30,
    verbose: bool = False,
) -> np.ndarray:
    """Performs the projective (first-order) noise reduction algorithm.

    Performs the noise reduction algorithm proposed by Grassberger et al. 1993.

    Args:
        data (np.ndarray): One dimensional noisy timeseries.
        iterations (int, optional): Number of iterations. Defaults to 5.
        m (int, optional): Embedding dimension. Defaults to 5.
        tau (int, optional): Embedding delay. Defaults to 1.
        Q (int, optional): Assumed attractor dimension. Defaults to 2.
        K (int, optional): Size of initial neighbourhood (N of neighbours). Defaults to 30.
        verbose (bool, optional): Whether to print the stderr output. Defaults to False.

    Returns:
        np.ndarray: Noise reduced timeseries.

    References:
        Grassberger, Peter et al. (1993). “On noise reduction methods for chaotic data”.
        In: Chaos: An Interdisciplinary Journal of Nonlinear Science 3.2, pp. 127–141.
    """
    # ensure array compatibility
    _check_array(data)

    # run command
    command = [
        "ghkss",
        "-m",
        f"1,{m}",
        "-d",
        f"{tau}",
        "-q",
        f"{Q}",
        "-k",
        f"{K}",
        "-i",
        f"{iterations}",
        "-V",
        "2",
    ]
    output = run_command_io(command, data, verbose=verbose)

    return output


def _check_array(data: np.ndarray, allowed_dimension: int | list[int] = 1) -> None:
    """Checks whether the given array can be passed to TISEAN safely.

    Raises an error of the array is of the wrong format.

    Args:
        data (np.ndarray): The array to be checked.
        allowed_dimension (int | list[int], optional): Allowed array dimension(s). Defaults to 1.
    """
    if not (
        isinstance(allowed_dimension, int) or isinstance(allowed_dimension, list[int])
    ):
        raise TypeError(
            f"The allowed dimension must be an integer or list of integer, not {type(allowed_dimension)}!"
        )

    if not isinstance(data, np.ndarray):
        raise TypeError("The input array must be a NumPy array!")
    if isinstance(allowed_dimension, int):
        if not data.ndim == allowed_dimension:
            raise ValueError(
                f"The input array's must be {allowed_dimension}-dimensional! The given array is of shape {data.shape}."
            )
    else:
        if data.ndim not in allowed_dimension:
            raise ValueError(
                f"The input array's dimension must be in {allowed_dimension}! The given array is of shape {data.shape}."
            )
    if not np.issubdtype(data.dtype, np.number):
        raise TypeError("The input array must contain only numeric values!")
