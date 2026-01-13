BASE_DIR = None
PLOT_DIR = None


def get_base_dir():
    if BASE_DIR is None:
        raise ValueError("BASE_DIR has not been set yet!")
    return BASE_DIR


def get_plot_dir():
    if PLOT_DIR is None:
        raise ValueError("PLOT_DIR has not been set yet!")
    return PLOT_DIR
