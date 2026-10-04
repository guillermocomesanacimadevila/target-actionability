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