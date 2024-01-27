import unittest
from unittest import mock

from crypto_VDF.data_transfer_objects.plotter import GetPaths, InputType, VDFName
from crypto_VDF.plotter.grapher import Grapher


class TestGrapher(unittest.TestCase):

    @mock.patch.object(Grapher, 'create_directories', lambda directories: "pass")
    def test_get_paths(self):
        number_of_delays = 10
        iterations = 10
        input_type = InputType.RANDOM_INPUT
        vdf_name = VDFName.PIETRZAK
        delay_sub_dir = f"2_to_power_{number_of_delays}"

        resp = Grapher.get_paths(delay_sub_dir=delay_sub_dir, iterations=iterations, input_type=input_type,
                                 vdf_name=vdf_name)

        self.assertTrue(isinstance(resp, GetPaths))
        from_project_root_dir_name = '/'.join(resp.dir_path.parts[-5:])
        self.assertEqual(from_project_root_dir_name,
                         f'crypto-VDF/data/{vdf_name.value}/{input_type.value}/{delay_sub_dir}')
        self.assertTrue(from_project_root_dir_name in str(resp.macrostate_file_name))
        self.assertTrue(from_project_root_dir_name in str(resp.measurements_file_name))
        self.assertEqual(resp.macrostate_file_name.name, f'macrostate_repeated_{iterations}_times.csv')
        self.assertEqual(resp.measurements_file_name.name, f'repeated_{iterations}_times.csv')
