from pathlib import Path
from typing import List

import numpy as np
import matplotlib.pyplot as plt

from crypto_VDF.data_transfer_objects.plotter import GetPaths, VDFName, InputType
from crypto_VDF.utils.utils import create_path_to_data_folder_v2
import pandas as pd


class Grapher:

    def __init__(self, number_of_delays: int, number_ot_iterations: int):
        self.number_of_delays = number_of_delays
        self.number_ot_iterations = number_ot_iterations

    def plot_data(self, data, title, fname: str):
        delays_list = np.asarray(data['delay'])
        y_time_eval = np.asarray(data[f'eval time means for {self.number_ot_iterations} iterations (s)'])
        y_time_verif = np.asarray(data[f"verify time means for {self.number_ot_iterations} iterations (s)"])
        fig, (ax1, ax2) = plt.subplots(2)
        fig.suptitle(title)
        ax1.set_title("Eval and Verify")
        ax1.plot(delays_list, y_time_eval, 'r--', label="Eval func complexity (mean)")
        ax1.plot(delays_list, y_time_verif, 'b-', label="Verify func complexity (mean)")
        ax1.set_ylabel('Execution Time')
        ax1.legend()
        ax1.grid()
        ax2.set_title("Verify function")
        ax2.plot(delays_list, y_time_verif, 'b-', label="Verify func complexity (mean) ")
        ax2.set_ylabel('Execution Time')
        ax2.legend()
        ax2.grid()

        plt.tight_layout()

        # plt.figure(figsize=(15, 12))
        # plt.plot(delays_list, y_time_eval, 'r--', label="Eval func complexity (mean)")
        # plt.plot(delays_list, y_time_verif, 'b-', label="Verify func complexity (mean) ")
        # plt.plot([], [], ' ', label="Security parameter = 256")

        #ax1.xlabel("Delays")
        #ax1.ylabel("Time taken (seconds)")
        plt.savefig(str(fname) + ".png")
        print("\nfigure saved successfully!\n")
        return plt

    @staticmethod
    def create_directories(directories: List[Path]) -> None:
        for directory in directories:
            directory.mkdir(exist_ok=True)

    @classmethod
    def get_paths(cls, delay_sub_dir: str, iterations: int, input_type: InputType, vdf_name: VDFName) -> GetPaths:
        data_path = create_path_to_data_folder_v2()
        vdf_path = data_path / str(vdf_name.value)
        input_path = vdf_path / str(input_type.value)
        input_type_path = vdf_path / str(input_type.value)
        sub_dir = input_type_path / delay_sub_dir

        # create the directories for data
        cls.create_directories([vdf_path, input_path, sub_dir])

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
