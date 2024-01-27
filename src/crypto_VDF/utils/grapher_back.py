from typing import Dict

from matplotlib import pyplot as plt

from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF
from crypto_VDF.utils.number_theory import NumberTheory
from time import time as t
from time import strftime, gmtime
from crypto_VDF.utils.utils import arrange_powers_of_2, create_path_to_data_folder
import numpy as np
import pandas as pd
import os


class Grapher:
    @classmethod
    def run_vdf_random(cls, pp: PublicParams):
        x = NumberTheory.generate_quadratic_residue(pp.modulus)
        return cls.run_vdf(pp=pp, input_pram=x)

    @staticmethod
    def run_vdf(pp: PublicParams, input_pram: int):
        tOutStart = t()
        evaluation = PietrzakVDF.eval(public_params=pp, input_param=input_pram, _hide=True)
        tOutEnd = t() - tOutStart

        # print(f"proof took: {tProofEnd} seconds")

        tVerifStart = t()

        verification = PietrzakVDF.verify(public_params=pp, input_param=input_pram, output_param=evaluation.output,
                                          proof=evaluation.proof, _hide=True)
        tVerifEnd = t() - tVerifStart
        assert verification is True
        # print(f"verification took: {tVerifEnd} seconds")
        return tOutEnd, tVerifEnd, input_pram, pp.delay

    @classmethod
    def generate_pietrzak_complexity_data(cls, number_of_delays: int = 10, delay_repeat: int = 1,
                                          fix_input=False) -> pd.DataFrame:
        data = {"delay": np.asarray([]), "eval time (s)": np.asarray([]),
                "verify time (s)": np.asarray([]), "input": np.asarray([])}

        delays_list = np.array(arrange_powers_of_2(1, number_of_delays))
        print("delays: ", delays_list)
        print("delay repeat", delay_repeat)

        time_eval_macro = np.array([0 for _ in range(len(delays_list) * delay_repeat)], dtype=np.float64)
        time_verif_macro = np.array([0 for _ in range(len(delays_list) * delay_repeat)], dtype=np.float64)
        macrostate_inputs = [0 for _ in range(len(delays_list) * delay_repeat)]
        macrostate_counted_delays = np.array([0 for _ in range(len(delays_list) * delay_repeat)], dtype=np.float64)

        if fix_input:

            primes = PietrzakVDF.generate_rsa_primes(256)
            modulus = primes.q.base_10 * primes.p.base_10
            x = NumberTheory.generate_quadratic_residue(modulus=modulus)
            results = [cls.run_vdf(pp := PietrzakVDF.setup(security_param=256, delay=i), input_pram=x) for idx, i in
                       enumerate(delays_list) for _ in range(delay_repeat)]
            # time_eval_macro, time_verif_macro, macrostate_counted_delays, macrostate_inputs = zip(*results)
            # results = [cls.run_vdf(pp=pp, input_pram=x) for idx, i in
            #            enumerate(delays_list) for _ in range(delay_repeat)]
            # time_eval_macro, time_verif_macro, macrostate_counted_delays, macrostate_inputs = zip(*results)
            # for i in delays_list:
            #
            #     pp = PietrzakVDF.setup(security_param=256, delay=i)
            #     y_time_eval = np.array([0 for _ in range(delay_repeat)])
            #     y_time_verif = np.array([0 for _ in range(delay_repeat)])
            #     inputs = [0 for _ in range(delay_repeat)]
            #     counted_delays = np.array([0 for _ in range(delay_repeat)])
            #
            #     for repeat_time in range(delay_repeat):
            #         # print(f"output took: {tOutEnd} seconds")
            #         tOutEnd, tVerifEnd, input_pram, pp.delay = cls.run_vdf(pp=pp, input_pram=x)
            #         time_eval_macro[i + repeat_time] = tOutEnd
            #         print(tOutEnd)
            #         time_verif_macro[i + repeat_time] = tVerifEnd
            #         breakpoint()
            #         time_eval_macro[i + repeat_time] = x
            #         macrostate_counted_delays[i + repeat_time] = pp.delay

        else:
            results = [cls.run_vdf_random(pp := PietrzakVDF.setup(security_param=256, delay=i)) for idx, i in
                       enumerate(delays_list) for _ in range(delay_repeat)]
            time_eval_macro, time_verif_macro, macrostate_counted_delays, macrostate_inputs = zip(*results)

            # for idx, i in enumerate(delays_list):
            #     pp = PietrzakVDF.setup(security_param=256, delay=i)
            #     for repeat_time in range(delay_repeat):
            #         tOutEnd, tVerifEnd, input_pram, pp.delay = cls.run_vdf_random(pp=pp)
            #         time_eval_macro[idx * repeat_time] = tOutEnd
            #         time_verif_macro[idx * repeat_time] = tVerifEnd
            #         macrostate_counted_delays[idx * repeat_time] = pp.delay
            #         macrostate_inputs[idx * repeat_time] = input_pram
            #         print(input_pram)

        print(time_eval_macro)
        print(time_verif_macro)

        print(macrostate_counted_delays)
        print(macrostate_inputs)

        print(len(time_eval_macro), len(delays_list) * delay_repeat)
        data["eval time (s)"] = time_eval_macro
        data["verify time (s)"] = time_verif_macro
        data["input"] = macrostate_counted_delays
        data["delay"] = macrostate_inputs
        dt = pd.DataFrame(data)
        return dt

    @classmethod
    def store_data(cls, number_of_delays: int, iterations: int, data: pd.DataFrame, input_type: str) -> str:
        data_path = create_path_to_data_folder()
        pietrzak_path = os.path.join(data_path, "pietrzak")
        input_path = os.path.join(pietrzak_path, input_type)
        input_type_path = os.path.join(pietrzak_path, input_type)

        # create the directories for data
        if not os.path.exists(pietrzak_path):
            os.mkdir(pietrzak_path)
        if not os.path.exists(input_path):
            os.mkdir(input_path)

        input_file_name = f"{input_type}_2_to_power_{number_of_delays}_repeated_{iterations}_times.csv"
        file_path = os.path.join(input_type_path, input_file_name)
        figure_name = f"{input_type}_data_mean_over_{iterations}_iterations_and_up_to_2_to_power_of_{number_of_delays}"
        figure_path = os.path.join(input_type_path, figure_name)
        if figure_name is not None:
            data.to_csv(file_path)
        return figure_path

    @classmethod
    def collect_pietrzak_complexity_data(cls, number_of_delays: int, iterations: int, fix_input: bool = False) -> \
            Dict[str, pd.DataFrame]:
        if fix_input:
            data = Grapher.generate_pietrzak_complexity_data(number_of_delays=number_of_delays,
                                                             delay_repeat=iterations,
                                                             fix_input=True)
            plot_file_name = cls.store_data(number_of_delays=number_of_delays, iterations=iterations,
                                            data=data, input_type='fixed_input')
        else:
            data = Grapher.generate_pietrzak_complexity_data(number_of_delays=number_of_delays,
                                                             delay_repeat=iterations,
                                                             fix_input=False)
            plot_file_name = cls.store_data(number_of_delays=number_of_delays, iterations=iterations,
                                            data=data, input_type="random_input")

        eval_time_means = np.asarray([])
        verify_time_means = np.asarray([])
        delays_list = np.array(arrange_powers_of_2(1, number_of_delays))

        for delay in delays_list:
            eval_time_means = np.append(eval_time_means,
                                        data.loc[data['delay'] == delay][
                                            'eval time (s)'].sum() / iterations)
            verify_time_means = np.append(verify_time_means,
                                          data.loc[data['delay'] == delay][
                                              'verify time (s)'].sum() / iterations)

        d = data['input'].unique()
        if len(d) != len(delays_list):
            d = [0 for _ in range(len(delays_list))]
        input_data = pd.DataFrame(
            {"delay": delays_list, f"eval time means for {iterations} iterations (s)": eval_time_means,
             f"verify time means for {iterations} iterations (s)": verify_time_means,
             "input": d})

        title = f"Pietrzak VDF complexity (mean after {iterations} iterations)"

        Grapher.plot_data(
            data=input_data,
            iterations=iterations,
            title=title,
            fname=plot_file_name
        )

        return {"plotted_data": input_data}

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


if __name__ == '__main__':
    s = t()
    result = Grapher.collect_pietrzak_complexity_data(20, 10)
    print(f"the operation took {t() - s} seconds or {strftime('%H:%M:%S', gmtime(t() - s))}")
    print(result)
