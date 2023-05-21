import datetime
from pathlib import Path
from typing import Dict, List

import pandas as pd


class SRMPParser:
    """State Register of Medicinal Plants"""

    def __init__(self, config: Dict[str, any]):
        """
        Initialize the SRMPParser instance.

        Args:
            config (Dict[str, any]): Configuration parameters for the parser.
                - file_names (List[str]): List of file names to parse.
                - col_mapping (List[List[int]]): List of column mappings for each file.
                - col_names (List[str]): List of column names.
                - header_row (int): Header row index in the Excel file.

        """
        self.config = config
        self.processed = pd.DataFrame(columns=self.config["col_names"][2:])

    def parse_files(self) -> None:
        """
        Parse the files using the provided configurations.

        Reads each file, applies filters, and appends the processed data to the `self.processed` DataFrame.

        """
        for file, mapping in zip(self.config["file_names"], self.config["col_mapping"]):
            root = Path(self.config["root_data_path"])
            dataset = pd.read_excel(
                root / file, usecols=mapping, header=self.config["header_row"]
            )
            dataset.columns = self.config["col_names"]
            dataset.reset_index(drop=True, inplace=True)
            dataset = self._filter_by_date(dataset)

            # Dropna by market_name
            dataset = dataset[dataset.market_name.notna()]
            # Drop empty chemical_names
            dataset = dataset[dataset.chemical_name.replace("~", None).notna()]
            self.processed = pd.concat(
                [self.processed, dataset[self.config["col_names"][2:]]],
                ignore_index=True,
            )

        self.processed.reset_index(drop=True, inplace=True)

    def _filter_by_date(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Filter the dataset by date.

        Args:
            dataset (pd.DataFrame): Dataset to be filtered.

        Returns:
            pd.DataFrame: Filtered dataset based on date conditions.

        """
        filter_col = self.config["col_names"][:2]
        dataset[filter_col] = dataset[filter_col].apply(
            pd.to_datetime, errors="coerce", format="%d.%m.%Y"
        )

        today = pd.to_datetime(datetime.date.today())
        dataset = dataset[
            ((dataset.completion_data > today) | dataset.completion_data.isnull())
            & ((dataset.cancellation_date > today) | dataset.cancellation_date.isnull())
        ]
        return dataset
