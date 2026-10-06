/*
Compilation of all queries used for the 
OpenTargets BigQuery dataset for target tractability
*/

SELECT id, approvedSymbol, tractability
FROM 'open-targets-prod.platform.target'
WHERE id IN UNNEST(@target_ids)

-- flatten tractability col (.list) to standard table 
SELECT
    t.id,
    t.approvedSymbol,
    t.biotype,
    assessment.element.*
FROM `bigquery-public-data.open_targets_platform.target` AS t
CROSS JOIN UNNEST(t.tractability.list) AS assessment
WHERE t.id IN UNNEST(@target_ids); -- ens_id

-- query an individual target
SELECT
    t.id,
    t.approvedSymbol,
    t.biotype,
    assessment.element.*
FROM `bigquery-public-data.open_targets_platform.target` AS t
CROSS JOIN UNNEST(t.tractability.list) AS assessment
WHERE t.approvedSymbol = 'FCRL1';