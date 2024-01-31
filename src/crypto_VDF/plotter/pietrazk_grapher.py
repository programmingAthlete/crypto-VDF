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

    def __init__(self, number_of_delays: int, number_ot_iterations: int, security_param: int,
                 input_type: InputType = InputType.RANDOM_INPUT):
        self.delays = np.array(arrange_powers_of_2(1, number_of_delays))
        self.security_param = security_param
        self.paths = self.get_paths(delay_sub_dir=f"2_to_power_{number_of_delays}", iterations=number_ot_iterations,
                                    input_type=input_type, vdf_name=VDFName.PIETRZAK)
        super().__init__(number_of_delays=number_of_delays, number_ot_iterations=number_ot_iterations)

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
    def run_vdf_random_with_delay(cls, delay, security_param):
        return cls.run_vdf_random(PietrzakVDF.setup(security_param=security_param, delay=delay))

    def generate_pietrzak_complexity_data(self, number_of_delays: int = 10, delay_repeat: int = 1,
                                          fix_input=False) -> pd.DataFrame:

        delays_list = np.array(arrange_powers_of_2(1, number_of_delays))
        _log.info(f"[PIETRAK-GENERATE-DATA] Delays {delays_list}")
        _log.info(f"[PIETRAK-GENERATE-DATA] Delay repeat {delay_repeat}")

        if fix_input:

            primes = PietrzakVDF.generate_rsa_primes(self.security_param)
            modulus = primes.q.base_10 * primes.p.base_10
            x = NumberTheory.generate_quadratic_residue(modulus=modulus)
            results = [cls.run_vdf(pp := PietrzakVDF.setup(security_param=self.security_param, delay=i), input_pram=x) for
                       idx, i in
                       enumerate(delays_list) for _ in range(delay_repeat)]
            time_eval_macro, time_verif_macro, macrostate_counted_delays, macrostate_inputs = zip(*results)

        else:
            results = [cls.run_vdf_random(pp := PietrzakVDF.setup(security_param=self.security_param, delay=i)) for idx, i in
                       enumerate(delays_list) for _ in range(delay_repeat)]
            time_eval_macro, time_verif_macro, macrostate_counted_delays, macrostate_inputs = zip(*results)

        _log.info("[PIETRAK-GENERATE-DATA] VDF ran successfully for all delays and repetitions")

        _log.debug(f"[PIETRAK-GENERATE-DATA] Execution times for Eval function: {time_eval_macro}")
        _log.debug(f"[PIETRAK-GENERATE-DATA] Execution times for Verify function: {time_verif_macro}")
        _log.debug(f"[PIETRAK-GENERATE-DATA] All delays for which the VDF has executes: {macrostate_counted_delays}")
        _log.debug(f"[PIETRAK-GENERATE-DATA] Inputs for which the VDF has executes: {macrostate_inputs}")
        data = {"delay": macrostate_inputs, "eval time (s)": time_eval_macro,
                "verify time (s)": time_verif_macro, "input": macrostate_counted_delays}
        dt = pd.DataFrame(data)
        _log.info("[PIETRAK-GENERATE-DATA] Data Generated")
        return dt

    def get_macrostate(self, data: pd.DataFrame) -> pd.DataFrame:
        eval_time_means, verify_time_means = zip(*[
            (data.loc[data['delay'] == delay]['eval time (s)'].sum() / self.number_ot_iterations,
             data.loc[data['delay'] == delay]['verify time (s)'].sum() / self.number_ot_iterations)
            for delay in self.delays])
        d = data['input'].unique()
        if len(d) != len(self.delays):
            d = [0 for _ in range(len(self.delays))]

        return pd.DataFrame(
            {"delay": self.delays, f"eval time means for {self.number_ot_iterations} iterations (s)": eval_time_means,
             f"verify time means for {self.number_ot_iterations} iterations (s)": verify_time_means,
             "input": d})

    @set_level(logger=_log)
    def collect_pietrzak_complexity_data(self, fix_input: bool = False, _verbose: bool = False,
                                         store_measurements: bool = True) -> CollectVDFData:
        data = self.generate_pietrzak_complexity_data(number_of_delays=self.number_of_delays,
                                                      delay_repeat=self.number_ot_iterations,
                                                      fix_input=fix_input)

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
