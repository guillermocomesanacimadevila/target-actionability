/*
Compilation of all queries used for the 
OpenTargets BigQuery dataset for target tractability
*/

SELECT id, approvedSymbol, tractability
FROM 'open-targets-prod.platform.target'
WHERE id IN UNNEST(@target_ids)