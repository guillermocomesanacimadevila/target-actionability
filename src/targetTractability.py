import re

from google.cloud import bigquery


class TargetTractability:

    """ 
    Leverage OpenTarget API to query target tractability from 
    ENS_id to their BigQuery dataset -> pull as csv locally
    """

    def __init__(
            self,
            gcp_project: str,
            bigquery_dataset: str = "open-targets-prod.platform"
    ):
        
        # make sure that if bigquery_dataset arg != same -> error
        if not re.fullmatch(r"[A-Za-z0-9_-]+\.[A-Za-z0-9_]+", bigquery_dataset):
            raise ValueError("Dataset must be 'project.dataset'.")

        self.client = bigquery.Client(project=gcp_project) # client == myself!
        self.table = f"{bigquery_dataset}.target" # table for protein X

    def fetch(
            self,
            targets: dict[str: str]
    ) -> list[dict]:

        """ {"APOE": "ENSG00000130203", ...} """

        if not targets:
            raise ValueError("Targets dictionary is empty!")

        # now loop through dict
        for gene, ens_id in targets.items():
            if not isinstance(gene, str) or not gene.strip():
                raise ValueError("Gene names must be non-empty strings!!!!!")

            if not isinstance(ens_id, str) or not re.fullmatch(r"ENSG[0-9]{11}", ens_id):
                raise ValueError(f"Invalid Ensembl gene ID for {gene}: {ens_id}")

        # SQL query for BigQuery
        query = f"""
SELECT id, approvedSymbol, tractability
FROM `open-targets-prod.platform.targets`
WHERE id IN UNNEST(@target_ids)
        """

        return 

    