/*
Compilation of queries for exploring drug-target tractability
from the OpenTargets BigQuery dataset

params:

job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter(
                    "target_ids",
                    "STRING",
                    list(targets.values())
                )
            ]
        )
*/

-- `bigquery-public-data.open_targets_platform.colocalisation` 

SELECT
    t.id,
    t.approvedSymbol,
    t.biotype,
    assessment.element.*
FROM `bigquery-public-data.open_targets_platform.target` AS t
CROSS JOIN UNNEST(t.tractability.list) AS assessment
LIMIT 100;

SELECT
    t.id,
    t.approvedSymbol,
    assessment.element.*
FROM `bigquery-public-data.open_targets_platform.target` AS t
CROSS JOIN UNNEST(t.tractability.list) AS assessment
WHERE t.approvedSymbol = 'ADAM10';


-- drug mechanism of action


-- SELECT * 
-- FROM `bigquery-public-data.open_targets_platform.drug_mechanism_of_action`;


/*
We need q query that:
- Looks at each ens_id within dict
- queries to drug_mechanism_of_action table (col X)
- if ENS_ID == THERE -> KEEP ROW
*/


-- target_prioritisation maybe?

SELECT *
FROM `bigquery-public-data.open_targets_platform.target_prioritisation`
LIMIT 50;












