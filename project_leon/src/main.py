from os import path

import config
from plots import (
    section_01_plots,
    section_02_plots,
    section_03a_plots,
    section_03b_plots,
    section_04_plots,
)


if __name__ == "__main__":
    config.BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    config.PLOT_DIR = path.join(config.BASE_DIR, "figures", "plots")

    print("Creating plots for section 1...")
    section_01_plots.run()
    print("Creating plots for section 2...")
    section_02_plots.run()
    print("Creating plots for section 3a...")
    section_03a_plots.run()
    print("Creating plots for section 3b...")
    section_03b_plots.run()
    print("Creating plots for section 4...")
    section_04_plots.run()
