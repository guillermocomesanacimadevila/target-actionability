import argparse
import polars as pl 
from .targetTractability import TargetTractability
from .utils import compose_target_ens_dictionary

def TargetActionability():
    p = argparse.ArgumentParser()
    p.add_argument("--gcp_project", required=True)
    p.add_argument("--bigquery_dataset", required=False, default='open-targets-prod.platform')
    p.add_argument("--targets", required=True)
    p.add_argument("--reference_dataset", required=True)
    p.add_argument("--ens_col", required=False, default="Ensembl_ID")
    p.add_argument("--symbol_col", required=False, default="Symbol")
    p.add_argument("--synonym_col", required=False, default="Synonyms")
    p.add_argument("--output", required=False, default="target_tractability.csv")
    parser = p.parse_args()

    # tractability using the OpenTargets BigQuery dataset
    df = pl.read_csv(parser.reference_dataset, separator="\t", infer_schema_length=0)

    # read targets .txt
    with open(parser.targets, "r") as file:
        targets = [line.strip() for line in file if line.strip()] # skip empty lines

    targets = compose_target_ens_dictionary(
        targets,
        df,
        parser.ens_col,
        parser.symbol_col,
        parser.synonym_col
    )
    
    trac = TargetTractability(parser.gcp_project, parser.bigquery_dataset)

    # now fetch to BigQuery
    rows = trac.fetch(targets)

    # list[dict] -> polars df -> csv
    out = pl.DataFrame(rows)
    out.write_csv(parser.output)
    print(f"{out.height} rows for {len(targets)} targets -> {parser.output}")
