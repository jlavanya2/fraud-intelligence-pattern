def update_case_status(df, txn_id, status):
    df.loc[df["txn_id"] == txn_id, "case_status"] = status
    return df
