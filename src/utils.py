import warnings

import polars as pl

def compose_target_ens_dictionary(
        targets: list[str],
        reference_df: pl.DataFrame,
        ens_col_pk: str,
        target_col_uk: str,
        synonym_col: str | None = None
    ) -> dict[str, str]:

    """
    take 1 list of targets + 1 dataset with 2 cols
    (1 == ens_id PK + UK for target + synonyms as opt )
    -> {"APOE": "ENSG00000130203", ...}

    matching is case-insensitive; approved symbol (UK) wins over synonyms.
    synonym_col can be a list[str] col or a string col delimited by | , or ;
    """

    if not targets:
        raise ValueError("Targets list is empty!")

    cols = [ens_col_pk, target_col_uk] + ([synonym_col] if synonym_col else [])
    missing = [c for c in cols if c not in reference_df.columns]
    if missing:
        raise ValueError(f"Columns not found in reference_df: {missing}")

    # ens_id cleaned: strip whitespace + version suffix (ENSG00000223972.6 -> ENSG00000223972)
    # empty strings -> null so rows w/o an ens_id get dropped
    ens_expr = (
        pl.col(ens_col_pk).cast(pl.Utf8).str.strip_chars()
        .str.replace(r"\.\d+$", "")
        .replace("", None)
        .alias("ens_id")
    )

    # 1) approved symbol -> ens_id
    approved = (
        reference_df
        .select(
            pl.col(target_col_uk).cast(pl.Utf8).str.strip_chars().str.to_uppercase().alias("key"),
            ens_expr,
        )
        .drop_nulls()
        .unique(subset="key", keep="first")
    )
    approved_map = dict(zip(approved["key"], approved["ens_id"]))

    # 2) synonym -> ens_id (only keep synonyms pointing to a single ens_id)
    synonym_map: dict[str, str] = {}
    if synonym_col:
        syn = reference_df.select(
            pl.col(synonym_col).alias("syn"),
            ens_expr,
        )
        if syn.schema["syn"] != pl.List(pl.Utf8):
            syn = syn.with_columns(
                pl.col("syn").cast(pl.Utf8).str.replace_all(r"[,;]", "|").str.split("|")
            )
        syn = (
            syn
            .explode("syn")
            .with_columns(pl.col("syn").str.strip_chars().str.to_uppercase())
            .filter(pl.col("syn").is_not_null() & (pl.col("syn") != ""))
            .drop_nulls()
            .group_by("syn")
            .agg(pl.col("ens_id").unique())
        )
        for key, ens_ids in syn.iter_rows():
            if len(ens_ids) == 1:
                synonym_map[key] = ens_ids[0]

    # 3) resolve each target
    result: dict[str, str] = {}
    unmatched: list[str] = []
    for target in targets:
        if not isinstance(target, str) or not target.strip():
            raise ValueError("Targets must be non-empty strings!")

        key = target.strip().upper()
        ens_id = approved_map.get(key) or synonym_map.get(key)
        if ens_id is None:
            unmatched.append(target)
        else:
            result[target.strip()] = ens_id

    if unmatched:
        warnings.warn(f"No Ensembl ID found for {len(unmatched)} target(s): {unmatched}")

    return result
