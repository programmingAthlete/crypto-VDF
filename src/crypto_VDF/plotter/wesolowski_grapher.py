from crypto_VDF.plotter.grapher import Grapher

from crypto_VDF.data_transfer_objects.dto import RsaSetup
from crypto_VDF.data_transfer_objects.plotter import CollectVDFData, InputType, VDFName
from crypto_VDF.utils.logger import get_logger, set_level
from crypto_VDF.verifiable_delay_functions.wesolowski import WesolowskiVDF
from time import time as t
from time import strftime, gmtime
from crypto_VDF.utils.utils import arrange_powers_of_2
import numpy as np
import pandas as pd

_log = get_logger(__name__)


class WesolowskiGrapher(Grapher):

    def __init__(self, number_of_delays: int, number_ot_iterations: int, security_parameter: int,
                 input_type: InputType = InputType.RANDOM_INPUT):
        self.delays = np.array(arrange_powers_of_2(1, number_of_delays))
        self.security_parameter = security_parameter
        self.paths = self.get_paths(delay_sub_dir=f"2_to_power_{number_of_delays}", iterations=number_ot_iterations,
                                    input_type=input_type, vdf_name=VDFName.WESOLOWSKI)
        super().__init__(number_of_delays=number_of_delays, number_ot_iterations=number_ot_iterations)

    def run_vdf_random(self, pp: RsaSetup):
        x = WesolowskiVDF.gen(setup=pp)
        return self.run_vdf(pp=pp, input_pram=x)

    def run_vdf(self, pp: RsaSetup, input_pram: int):
        _log.debug(f"[RUN-VDF] Starting the evaluation function with x = {input_pram}")
        tOutStart = t()
        evaluation = WesolowskiVDF.eval(setup=pp, input_param=input_pram, _hide=True)
        tOutEnd = t() - tOutStart
        _log.debug(f"[RUN-VDF] Finished the evaluation function with (y,pi) = ({evaluation.output},{evaluation.proof})"
                   f" in {tOutEnd} seconds")
        _log.debug(f"[RUN-VDF] Starting the verification function with (x,y,pi) ="
                   f" ({input_pram},{evaluation.output},{evaluation.proof}")
        tVerifStart = t()
        verification = WesolowskiVDF.verify(setup=pp, input_param=input_pram, output_param=evaluation.output,
                                            proof=evaluation.proof, _hide=True)
        tVerifEnd = t() - tVerifStart
        _log.debug(f"[RUN-VDF] Finished the verification function with verification: {verification} in {tVerifEnd} "
                   f"seconds")
        assert verification is True

        return tOutEnd, tVerifEnd, input_pram, pp.delay

    def run_vdf_random_with_delay(self, delay):
        return self.run_vdf_random(WesolowskiVDF.setup(security_param=self.security_parameter, delay=delay))

    def generate_wesolowski_complexity_data(self, fix_input=False) -> pd.DataFrame:

        delays_list = np.array(arrange_powers_of_2(1, self.number_of_delays))
        _log.info(f"[WESOLOWSKI-GENERATE-DATA] Delays {delays_list}")
        _log.info(f"[WESOLOWSKI-GENERATE-DATA] Delay repeat {self.number_ot_iterations}")

        if fix_input:
            rsa_setup = WesolowskiVDF.setup(security_param=self.security_parameter, delay=2)
            x = WesolowskiVDF.gen(setup=rsa_setup)
            results = [
                self.run_vdf(pp := WesolowskiVDF.setup(security_param=self.security_parameter, delay=i), input_pram=x)
                for idx, i in
                enumerate(delays_list) for _ in range(self.number_ot_iterations)]
            time_eval_macro, time_verif_macro, macrostate_counted_delays, macrostate_inputs = zip(*results)

        else:
            results = [self.run_vdf_random(pp := WesolowskiVDF.setup(security_param=self.security_parameter, delay=i)) for idx, i in
                       enumerate(delays_list) for _ in range(self.number_ot_iterations)]
            time_eval_macro, time_verif_macro, macrostate_counted_delays, macrostate_inputs = zip(*results)

        _log.info("[WESOLOWSKI-GENERATE-DATA] VDF ran successfully for all delays and repetitions")

        _log.debug(f"[WESOLOWSKI-GENERATE-DATA] Execution times for Eval function: {time_eval_macro}")
        _log.debug(f"[WESOLOWSKI-GENERATE-DATA] Execution times for Verify function: {time_verif_macro}")
        _log.debug(f"[WESOLOWSKI-GENERATE-DATA] All delays for which the VDF has executes: {macrostate_counted_delays}")
        _log.debug(f"[WESOLOWSKI-GENERATE-DATA] Inputs for which the VDF has executes: {macrostate_inputs}")
        data = {"delay": macrostate_inputs, "eval time (s)": time_eval_macro,
                "verify time (s)": time_verif_macro, "input": macrostate_counted_delays}
        dt = pd.DataFrame(data)
        _log.info("[WESOLOWSKI-GENERATE-DATA] Data Generated")
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
    def collect_wesolowski_complexity_data(self, fix_input: bool = False, _verbose: bool = False,
                                         store_measurements: bool = True) -> CollectVDFData:

        data = self.generate_wesolowski_complexity_data(fix_input=fix_input)
        _log.info("[COLLECT-VDF-DATA] Finished generating the data")
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
    grapher = WesolowskiGrapher(number_of_delays=2, number_ot_iterations=2, security_parameter=10)
    result = grapher.collect_wesolowski_complexity_data()
    print(f"the operation took {t() - s} seconds or {strftime('%H:%M:%S', gmtime(t() - s))}")
    print(result)
