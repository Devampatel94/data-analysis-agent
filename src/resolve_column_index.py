import re

def resolve_column_indices(query, df):
    """
    Finds phrases like '2nd column' and returns real column names by index.
    """
    # Find all ordinal mentions like '2nd', '3rd'
    matches = re.findall(r'(\d+)(?:st|nd|rd|th)?\s+column', query.lower())
    print(matches)
    col_names = []
    for m in matches:
        idx = int(m) - 1  # 1-based to 0-based
        if 0 <= idx < len(df.columns):
            col_names.append(df.columns[idx])

    return col_names