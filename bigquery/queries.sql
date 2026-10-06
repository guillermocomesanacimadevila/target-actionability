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

-- select colnames from table X
SELECT column_name
FROM `bigquery-public-data.open_targets_platform.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'target'
ORDER BY ordinal_position;


-- proteinIds within .target
SELECT
  t.id,
  t.approvedSymbol,
  ARRAY(
    SELECT p.element.id
    FROM UNNEST(t.proteinIds.list) AS p
    WHERE p.element.source = "uniprot_swissprot"
  ) AS uniprot_swissprot,
  ARRAY(SELECT DISTINCT p.element.source FROM UNNEST(t.proteinIds.list) AS p) AS sources_present
FROM `bigquery-public-data.open_targets_platform.target` AS t
WHERE t.approvedSymbol IN ("APOE", "TREM2", "CD33", "ACE", "ANKRD54", "SPRYD4")
ORDER BY t.approvedSymbol;
