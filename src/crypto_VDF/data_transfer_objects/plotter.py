import enum
from pathlib import Path

import pandas as pd
import pydantic


class GetPaths(pydantic.BaseModel):
    dir_path: Path
    plot_file_name: Path
    measurements_file_name: Path
    macrostate_file_name: Path


class CollectVDFData(pydantic.BaseModel):
    measurements: pd.DataFrame
    means: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True


class InputType(enum.Enum):
    RANDOM_INPUT = 'random_input'
    FIX_INPUT = 'fix_input'


class VDFName(enum.Enum):
    PIETRZAK = 'pietrzak'
    WESOLOWSKI = 'wesolowski'
