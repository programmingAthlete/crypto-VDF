import enum
import shutil
import unittest
from pathlib import Path

import orjson

from crypto_VDF.data_transfer_objects.plotter import GetPaths
from crypto_VDF.plotter.grapher import Grapher
from crypto_VDF.utils.utils import create_path_to_data_folder_v2


class MockInputTypeEnum(enum.Enum):
    InputTypeMock = 'input_type'


class MockVDFNameEnum(enum.Enum):
    VDFNameMock = 'vdf_name'


class TestGrapher(unittest.TestCase):

    def test_get_paths(self):
        number_of_delays = 10
        iterations = 10
        input_type = MockInputTypeEnum.InputTypeMock
        vdf_name = MockVDFNameEnum.VDFNameMock
        delay_sub_dir = f"2_to_power_{number_of_delays}"

        resp = Grapher.get_paths(delay_sub_dir=delay_sub_dir, iterations=iterations, input_type=input_type,
                                 vdf_name=vdf_name)

        self.assertTrue(isinstance(resp, GetPaths))
        from_project_root_dir_name = '/'.join(resp.dir_path.parts[-5:])
        self.assertEqual(from_project_root_dir_name, f'crypto-VDF/data/{vdf_name.value}/{input_type.value}/{delay_sub_dir}')
        self.assertTrue(from_project_root_dir_name in str(resp.macrostate_file_name))
        self.assertTrue(from_project_root_dir_name in str(resp.measurements_file_name))
        self.assertEqual(resp.macrostate_file_name.name, f'macrostate_repeated_{iterations}_times.csv')
        self.assertEqual(resp.measurements_file_name.name, f'repeated_{iterations}_times.csv')

        path_to_data = create_path_to_data_folder_v2()
        p = path_to_data / vdf_name.value
        shutil.rmtree(str(p))
