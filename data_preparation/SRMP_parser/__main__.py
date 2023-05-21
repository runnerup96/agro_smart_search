import pandas as pd
import yaml
from SRMP import SRMPParser

config = yaml.load(open("SRMP_config.yaml", "rb"), Loader=yaml.Loader)

if __name__ == "__main__":
    parser = SRMPParser(config)
    parser.parse_files()

    result = (
        parser.processed.groupby("market_name")["chemical_name"]
        .apply(list)
        .reset_index()
    )
    result.loc[:, "chemical_name"] = result.chemical_name.apply(
        lambda x: " ".join(pd.unique(x))
    )

    result.to_csv("parsed/SRMP.csv")
