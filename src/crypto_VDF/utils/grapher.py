from matplotlib import pyplot as plt
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF
from crypto_VDF.utils.number_theory import NumberTheory
from time import time as t
from time import strftime, gmtime
from crypto_VDF.utils.utils import arrange_powers_of_2, create_path_to_data_folder
import numpy as np
import pandas as pd
import os


class Grapher:

    @staticmethod
    def generate_pietrzak_complexity_data(number_of_delays=10, fname=None, delay_repeat=1, randomize_input=False):
        data = {"delay": np.asarray([]), "eval time (s)": np.asarray([]),
                "verify time (s)": np.asarray([]), "input": np.asarray([])}

        delays_list = np.array(arrange_powers_of_2(1, number_of_delays))
        print("delays: ", delays_list)

        yTimeEval = np.asarray([])
        yTimeVerif = np.asarray([])
        inputs = np.asarray([])
        counted_delays = np.asanyarray([])

        for i in delays_list:

            pp = None
            x = None

            if not randomize_input:
                pp = PietrzakVDF.setup(security_param=256, delay=i)
                x = NumberTheory.generate_quadratic_residue(pp.modulus)

            for repeat_time in range(delay_repeat):
                if randomize_input:
                    pp = PietrzakVDF.setup(security_param=256, delay=i)
                    x = NumberTheory.generate_quadratic_residue(pp.modulus)

                # print(f"output took: {tOutEnd} seconds")

                tOutStart = t()
                evaluation = PietrzakVDF.eval(public_params=pp, input_param=x, _hide=True)
                tOutEnd = t() - tOutStart

                # print(f"proof took: {tProofEnd} seconds")
                yTimeEval = np.append(yTimeEval, tOutEnd)

                tVerifStart = t()

                verification = PietrzakVDF.verify(public_params=pp, input_param=x, output_param=evaluation.output,
                                                  proof=evaluation.proof, _hide=True)
                assert verification is True
                tVerifEnd = t() - tVerifStart
                # print(f"verification took: {tVerifEnd} seconds")
                yTimeVerif = np.append(yTimeVerif, tVerifEnd)

                inputs = np.append(inputs, x)
                counted_delays = np.append(counted_delays, i)

        data["eval time (s)"] = yTimeEval
        data["verify time (s)"] = yTimeVerif
        data["input"] = inputs
        data["delay"] = counted_delays
        dt = pd.DataFrame(data)

        if fname is not None:
            dt.to_csv(fname)
        return dt

    @staticmethod
    def collect_pietrzak_complexity_data(number_of_delays, iterations):
        data_path = create_path_to_data_folder()
        pietrzak_path = os.path.join(data_path, "pietrzak")
        random_input_path = os.path.join(pietrzak_path, "random_input")
        fixed_input_path = os.path.join(pietrzak_path, "fixed_input")

        # create the directories for data
        if not os.path.exists(pietrzak_path):
            os.mkdir(pietrzak_path)
        if not os.path.exists(random_input_path):
            os.mkdir(random_input_path)
        if not os.path.exists(fixed_input_path):
            os.mkdir(fixed_input_path)

        fixed_input_file_name = f"fixed_input_2_to_power_{number_of_delays}_repeated_{iterations}_times.csv"
        fixed_input_file_path = os.path.join(fixed_input_path, fixed_input_file_name)
        fixed_input_figure_name = f"fixed_input_data_mean_over_{iterations}_iterations_and_up_to_2_to_power_of_{number_of_delays}"
        fixed_input_figure_path = os.path.join(fixed_input_path, fixed_input_figure_name)
        fixed_input_data = Grapher.generate_pietrzak_complexity_data(number_of_delays=number_of_delays,
                                                                     fname=fixed_input_file_path,
                                                                     delay_repeat=iterations,
                                                                     randomize_input=False)

        random_input_file_name = f"random_input_2_to_power_{number_of_delays}_repeated_{iterations}_times.csv"
        random_input_file_path = os.path.join(random_input_path, random_input_file_name)
        random_input_figure_name = f"random_input_data_mean_over_{iterations}_iterations_and_up_to_2_to_power_of_{number_of_delays}"
        random_input_figure_path = os.path.join(random_input_path, random_input_figure_name)
        random_input_data = Grapher.generate_pietrzak_complexity_data(number_of_delays=number_of_delays,
                                                                      fname=random_input_file_path,
                                                                      delay_repeat=iterations,
                                                                      randomize_input=True)

        fixed_input_eval_time_means = np.asarray([])
        fixed_input_verify_time_means = np.asarray([])

        random_input_eval_time_means = np.asarray([])
        random_input_verify_time_means = np.asarray([])
        delays_list = np.array(arrange_powers_of_2(1, number_of_delays))

        for delay in delays_list:
            fixed_input_eval_time_means = np.append(fixed_input_eval_time_means,
                                                    fixed_input_data.loc[fixed_input_data['delay'] == delay][
                                                        'eval time (s)'].sum() / iterations)
            fixed_input_verify_time_means = np.append(fixed_input_verify_time_means,
                                                      fixed_input_data.loc[fixed_input_data['delay'] == delay][
                                                          'verify time (s)'].sum() / iterations)

            random_input_eval_time_means = np.append(random_input_eval_time_means,
                                                     random_input_data.loc[random_input_data['delay'] == delay][
                                                         'eval time (s)'].sum() / iterations)
            random_input_verify_time_means = np.append(random_input_verify_time_means,
                                                       random_input_data.loc[random_input_data['delay'] == delay][
                                                           'verify time (s)'].sum() / iterations)

        fixed_input_data = pd.DataFrame(
            {"delay": delays_list, f"eval time means for {iterations} iterations (s)": random_input_eval_time_means,
             f"verify time means for {iterations} iterations (s)": fixed_input_verify_time_means,
             "input": fixed_input_data['input'].unique()})

        random_input_data = pd.DataFrame(
            {"delay": delays_list,
             f"eval time means for {iterations} iterations (s)": random_input_eval_time_means,
             f"verify time means for {iterations} iterations (s)": random_input_verify_time_means})

        title = f"Pietrzak VDF complexity (mean after {iterations} iterations)"

        Grapher.plot_data(
            data=fixed_input_data,
            iterations=iterations,
            title=title,
            fname=fixed_input_figure_path
        )

        Grapher.plot_data(
            data=random_input_data,
            iterations=iterations,
            title=title,
            fname=random_input_figure_path

        )

        return {"fixed_input_data": fixed_input_data, "random_input_data": random_input_data}

    @staticmethod
    def plot_data(data, iterations, title, fname=None):

        delays_list = np.asarray(data['delay'])
        yTimeEval = np.asarray(data[f'eval time means for {iterations} iterations (s)'])
        yTimeVerif = np.asarray(data[f"verify time means for {iterations} iterations (s)"])

        if fname is not None:
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
        else:
            plt.show()


if __name__ == '__main':
    s = t()
    result = Grapher.collect_pietrzak_complexity_data(20, 10)
    print(f"the operation took {t() - s} seconds or {strftime('%H:%M:%S', gmtime(t() - s))}")
    print(result)
    print(result['fixed_input_data'])
    print(result['random_input_data'])
