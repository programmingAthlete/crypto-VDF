from crypto_VDF.plotter.grapher import Grapher

from crypto_VDF.data_transfer_objects.dto import PublicParams
from crypto_VDF.data_transfer_objects.plotter import CollectVDFData, InputType, VDFName
from crypto_VDF.utils.logger import get_logger, set_level
from crypto_VDF.verifiable_delay_functions.pietrzak import PietrzakVDF
from crypto_VDF.utils.number_theory import NumberTheory
from time import time as t
from time import strftime, gmtime
from crypto_VDF.utils.utils import arrange_powers_of_2
import numpy as np
import pandas as pd

_log = get_logger(__name__)


class PietrzakGrapher(Grapher):

    def __init__(self, number_of_delays: int, number_ot_iterations: int, security_parameter: int,
                 input_type: InputType = InputType.RANDOM_INPUT):
        self.delays = np.array(arrange_powers_of_2(1, number_of_delays))
        self.security_parameter = security_parameter
        self.paths = self.get_paths(delay_sub_dir=f"2_to_power_{number_of_delays}", iterations=number_ot_iterations,
                                    input_type=input_type, vdf_name=VDFName.PIETRZAK)
        super().__init__(number_of_delays=number_of_delays, number_ot_iterations=number_ot_iterations)

    @classmethod
    def run_vdf_random(cls, pp: PublicParams):
        x = NumberTheory.generate_quadratic_residue(pp.modulus)
        return cls.run_vdf(pp=pp, input_pram=x)

    @staticmethod
    def run_vdf(pp: PublicParams, input_pram: int):
        print()
        _log.debug(f"[RUN-VDF] Delay {pp.delay}")
        _log.debug(f"[RUN-VDF] Starting the evaluation function with x = {input_pram}")
        t_out_start = t()
        evaluation = PietrzakVDF.eval(public_params=pp, input_param=input_pram, _hide=True)
        t_out_end = t() - t_out_start
        _log.debug(f"[RUN-VDF] Finished the evaluation function with y = {evaluation.output}"
                   f" in {t_out_end} seconds")
        _log.debug(f"[RUN-VDF] Starting the verification function with (x,y) ="
                   f" ({input_pram},{evaluation.output})")

        t_verif_start = t()
        verification = PietrzakVDF.verify(public_params=pp, input_param=input_pram, output_param=evaluation.output,
                                          proof=evaluation.proof, _hide=True)
        t_verif_end = t() - t_verif_start
        _log.debug(f"[RUN-VDF] Finished the verification function with verification: {verification} in {t_verif_end} "
                   f"seconds")

        assert verification is True
        return t_out_end, t_verif_end, input_pram, pp.delay

    def run_vdf_random_with_delay(self, delay):
        return self.run_vdf_random(PietrzakVDF.setup(security_param=self.security_parameter, delay=delay))

    def generate_pietrzak_complexity_data(self, fix_input=False) -> pd.DataFrame:

        delays_list = np.array(arrange_powers_of_2(1, self.number_of_delays))
        _log.info(f"[PIETRAK-GENERATE-DATA] Delays {delays_list}")
        _log.info(f"[PIETRAK-GENERATE-DATA] Delay repeat {self.number_ot_iterations}")

        if fix_input:

            primes = PietrzakVDF.generate_rsa_primes(self.security_parameter)
            modulus = primes.q.base_10 * primes.p.base_10
            x = NumberTheory.generate_quadratic_residue(modulus=modulus)
            results = [
                self.run_vdf(pp := PietrzakVDF.setup(security_param=self.security_parameter, delay=i), input_pram=x) for
                idx, i in
                enumerate(delays_list) for _ in range(self.number_ot_iterations)]
            time_eval_macro, time_verif_macro, macrostate_counted_delays, macrostate_inputs = zip(*results)

        else:
            results = [self.run_vdf_random(pp := PietrzakVDF.setup(security_param=self.security_parameter, delay=i)) for
                       idx, i in
                       enumerate(delays_list) for _ in range(self.number_ot_iterations)]
            time_eval_macro, time_verif_macro, macrostate_counted_delays, macrostate_inputs = zip(*results)

        _log.info("[PIETRAK-GENERATE-DATA] VDF ran successfully for all delays and repetitions")

        data = {"delay": macrostate_inputs, "eval time (s)": time_eval_macro,
                "verify time (s)": time_verif_macro, "input": macrostate_counted_delays}
        dt = pd.DataFrame(data)
        _log.info("[PIETRAK-GENERATE-DATA] Data Generated")
        return dt

    def get_macrostate(self, data: pd.DataFrame) -> pd.DataFrame:
        eval_time_means, eval_time_std, verify_time_means, verify_time_std = zip(*[
            (data.loc[data['delay'] == delay]['eval time (s)'].sum() / self.number_ot_iterations,
             data.loc[data['delay'] == delay]['eval time (s)'].std(),
             data.loc[data['delay'] == delay]['verify time (s)'].sum() / self.number_ot_iterations,
             data.loc[data['delay'] == delay]['verify time (s)'].std()
             )
            for delay in self.delays])
        d = data['input'].unique()
        if len(d) != len(self.delays):
            d = [0 for _ in range(len(self.delays))]

        return pd.DataFrame(
            {"delay": self.delays,
             f"eval time means for {self.number_ot_iterations} iterations (s)": eval_time_means,
             f"eval time std for {self.number_ot_iterations} iterations (s)": eval_time_std,
             f"verify time means for {self.number_ot_iterations} iterations (s)": verify_time_means,
             f"verify time std for {self.number_ot_iterations} iterations (s)": verify_time_std,
             "input": d})

    @set_level(logger=_log)
    def collect_pietrzak_complexity_data(self, fix_input: bool = False, _verbose: bool = False,
                                         store_measurements: bool = True) -> CollectVDFData:
        data = self.generate_pietrzak_complexity_data(fix_input=fix_input)

        input_data = self.get_macrostate(data=data)
        if store_measurements:
            Grapher.store_data(filename=self.paths.measurements_file_name, data=data)
            _log.info(f"[COLLECT-VDF-DATA] Stored measurements in file {self.paths.measurements_file_name}")
            Grapher.store_data(filename=self.paths.macrostate_file_name, data=input_data)
            _log.info(f"[COLLECT-VDF-DATA] Stored mean measurements in file {self.paths.macrostate_file_name}")

        return CollectVDFData(means=input_data, measurements=data)


if __name__ == '__main__':
    s = t()
    # grapher = PietrzakGrapher(number_of_delays=20, number_ot_iterations=10)
    grapher = PietrzakGrapher(number_of_delays=2, number_ot_iterations=2, security_param=10)
    result = grapher.collect_pietrzak_complexity_data()
    print(f"the operation took {t() - s} seconds or {strftime('%H:%M:%S', gmtime(t() - s))}")
    print(result)
