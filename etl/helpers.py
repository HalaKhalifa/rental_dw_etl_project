import pandas as pd

def clean_merge(left_df, right_df, on=None, left_on=None, right_on=None, suffixes=('_left', '_right')):
    """Drop 'last_update' and safely merge two DataFrames."""
    for col in ['last_update']:
        left_df = left_df.drop(columns=[col], errors='ignore')
        right_df = right_df.drop(columns=[col], errors='ignore')

    merged_df = pd.merge(
        left_df,
        right_df,
        how='inner',
        on=on,
        left_on=left_on,
        right_on=right_on,
        suffixes=suffixes
    )
    print(f"Merged on '{on or (left_on + ' ~ ' + right_on)}', result cols: {merged_df.columns.tolist()}")
    return merged_df

def safe_full_name(row, person):
    invalid = {"", " ", "null", "none", "nan"}
    first = row.get("first_name")
    last = row.get("last_name")

    if pd.isna(first) or str(first).strip().lower() in invalid:
        first = "Unknown"
    if pd.isna(last) or str(last).strip().lower() in invalid:
        last = person

    return f"{first} {last}"
