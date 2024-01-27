from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from crypto_VDF.data_transfer_objects.plotter import GetPaths, VDFName, InputType
from crypto_VDF.utils.utils import create_path_to_data_folder_v2
import pandas as pd


class Grapher:

    def __init__(self, number_of_delays: int, number_ot_iterations: int):
        self.number_of_delays = number_of_delays
        self.number_ot_iterations = number_ot_iterations

    def plot_data(self, data, title, fname: str, show: bool = False):
        delays_list = np.asarray(data['delay'])
        yTimeEval = np.asarray(data[f'eval time means for {self.number_ot_iterations} iterations (s)'])
        yTimeVerif = np.asarray(data[f"verify time means for {self.number_ot_iterations} iterations (s)"])

        plt.figure(figsize=(15, 12))
        plt.plot(delays_list, yTimeEval, 'r--', label="Eval func complexity (mean)")
        plt.plot(delays_list, yTimeVerif, 'b-', label="Verify func complexity (mean) ")
        plt.plot([], [], ' ', label="Security parameter = 256")

        plt.title(title)
        plt.xlabel("Delays")
        plt.ylabel("Time taken (seconds)")
        plt.legend()
        plt.savefig(str(fname) + ".png")
        print("\nfigure saved successfully!\n")
        return plt

    @staticmethod
    def get_paths(delay_sub_dir: str, iterations: int, input_type: InputType, vdf_name: VDFName) -> GetPaths:
        data_path = create_path_to_data_folder_v2()
        vdf_path = data_path / str(vdf_name.value)
        input_path = vdf_path / str(input_type.value)
        input_type_path = vdf_path / str(input_type.value)

        # create the directories for data
        vdf_path.mkdir(exist_ok=True)
        input_path.mkdir(exist_ok=True)
        # _2_to_power_{number_of_delays}
        sub_dir = input_type_path / delay_sub_dir
        sub_dir.mkdir(exist_ok=True)

        input_file_name = f"repeated_{iterations}_times.csv"
        macrostate_input_file = f"macrostate_repeated_{iterations}_times.csv"
        file_path = sub_dir / input_file_name
        macrostate_file_path = sub_dir / macrostate_input_file
        figure_name = f"data_mean_over_{iterations}_iterations"
        figure_path = sub_dir / figure_name
        return GetPaths(dir_path=sub_dir, plot_file_name=figure_path, measurements_file_name=file_path,
                        macrostate_file_name=macrostate_file_path)

    @staticmethod
    def store_data(filename: Path, data: pd.DataFrame) -> None:
        data.to_csv(str(filename))
