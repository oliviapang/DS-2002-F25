# ...existing code...
import os
import json
import pandas as pd

def _load_lookup_data(lookup_dir):
    """
    Load JSON price files from lookup_dir, flatten them and extract the highest
    market price per card_id.

    Returns a DataFrame with one row per card_id (highest market value kept).
    """
    all_lookup_df = []

    #required_cols = ['card_id', 'set_id', 'name', 'card_market_value']

    for fname in os.listdir(lookup_dir):
        if not fname.lower().endswith('.json'):
            continue

        filepath = os.path.join(lookup_dir, fname)
        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception:
            # Skip unreadable / invalid JSON files
            continue

        if 'data' not in data or not isinstance(data['data'], (list, dict)):
            continue

        df = pd.json_normalize(data['data'])

        # Compute card_market_value, preferring holofoil.market then normal.market then 0.0
        holo_col = 'tcgplayer.prices.holofoil.market'
        normal_col = 'tcgplayer.prices.normal.market'

        # Use get to avoid KeyError if column missing; create series of NaNs if absent
        holo_series = df[holo_col] if holo_col in df.columns else pd.Series([pd.NA] * len(df), index=df.index)
        normal_series = df[normal_col] if normal_col in df.columns else pd.Series([pd.NA] * len(df), index=df.index)

        df['card_market_value'] = holo_series.fillna(normal_series).fillna(0.0)
        df['card_market_value'] = pd.to_numeric(df['card_market_value'], errors='coerce').fillna(0.0)

        # Standardize column names
        df = df.rename(columns={'id': 'card_id', 'set.id': 'set_id'})

        # Ensure required columns exist (missing will be NaN)
        out_df = df.reindex(columns=required_cols).copy()

        all_lookup_df.append(out_df)

    if not all_lookup_df:
        # Return empty DataFrame with required columns
        return pd.DataFrame(columns=required_cols)

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)

    # Sort by market value (highest first) and drop duplicates keeping the highest value per card_id
    if 'card_market_value' in lookup_df.columns:
        lookup_df = lookup_df.sort_values(by='card_market_value', ascending=False)

    lookup_df = lookup_df.drop_duplicates(subset=['card_id'], keep='first').reset_index(drop=True)

    return lookup_df

# ...existing code...
import os
import json
import pandas as pd

def _load_lookup_data(lookup_dir):
    """
    Load JSON price files from lookup_dir, flatten them and extract the highest
    market price per card_id.

    Returns a DataFrame with one row per card_id (highest market value kept).
    """
    all_lookup_df = []

    required_cols = ['card_id', 'set_id', 'name', 'card_market_value']

    for fname in os.listdir(lookup_dir):
        if not fname.lower().endswith('.json'):
            continue

        filepath = os.path.join(lookup_dir, fname)
        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception:
            # Skip unreadable / invalid JSON files
            continue

        if 'data' not in data or not isinstance(data['data'], (list, dict)):
            continue

        df = pd.json_normalize(data['data'])

        # Compute card_market_value, preferring holofoil.market then normal.market then 0.0
        holo_col = 'tcgplayer.prices.holofoil.market'
        normal_col = 'tcgplayer.prices.normal.market'

        # Use get to avoid KeyError if column missing; create series of NaNs if absent
        holo_series = df[holo_col] if holo_col in df.columns else pd.Series([pd.NA] * len(df), index=df.index)
        normal_series = df[normal_col] if normal_col in df.columns else pd.Series([pd.NA] * len(df), index=df.index)

        df['card_market_value'] = holo_series.fillna(normal_series).fillna(0.0)
        df['card_market_value'] = pd.to_numeric(df['card_market_value'], errors='coerce').fillna(0.0)

        # Standardize column names
        df = df.rename(columns={'id': 'card_id', 'set.id': 'set_id'})

        # Ensure required columns exist (missing will be NaN)
        out_df = df.reindex(columns=required_cols).copy()

        all_lookup_df.append(out_df)

    if not all_lookup_df:
        # Return empty DataFrame with required columns
        return pd.DataFrame(columns=required_cols)

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)

    # Sort by market value (highest first) and drop duplicates keeping the highest value per card_id
    if 'card_market_value' in lookup_df.columns:
        lookup_df = lookup_df.sort_values(by='card_market_value', ascending=False)

    lookup_df = lookup_df.drop_duplicates(subset=['card_id'], keep='first').reset_index(drop=True)

    return lookup_df

def _load_inventory_data(inventory_dir):
    """
    Load CSV inventory files from inventory_dir, concatenate them and create a
    unified 'card_id' key by combining set_id and card_number (format: "{set_id}-{card_number}").
    """
    inventory_data = []

    for fname in os.listdir(inventory_dir):
        if not fname.lower().endswith('.csv'):
            continue

        filepath = os.path.join(inventory_dir, fname)
        try:
            df = pd.read_csv(filepath)
        except Exception:
            # Skip unreadable / invalid CSV files
            continue

        inventory_data.append(df)

    if not inventory_data:
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_data, ignore_index=True)

    # Create unified card_id key
    inventory_df['card_id'] = inventory_df['set_id'].astype(str) + '-' + inventory_df['card_number'].astype(str)

    return inventory_df

# ...existing code...
import os
import json
import sys
import pandas as pd

def _load_lookup_data(lookup_dir):
    """
    Load JSON price files from lookup_dir, flatten them and extract the highest
    market price per card_id.

    Returns a DataFrame with one row per card_id (highest market value kept).
    """
    all_lookup_df = []

    required_cols = ['card_id', 'set_id', 'name', 'card_market_value']

    for fname in os.listdir(lookup_dir):
        if not fname.lower().endswith('.json'):
            continue

        filepath = os.path.join(lookup_dir, fname)
        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception:
            # Skip unreadable / invalid JSON files
            continue

        if 'data' not in data or not isinstance(data['data'], (list, dict)):
            continue

        df = pd.json_normalize(data['data'])

        # Compute card_market_value, preferring holofoil.market then normal.market then 0.0
        holo_col = 'tcgplayer.prices.holofoil.market'
        normal_col = 'tcgplayer.prices.normal.market'

        holo_series = df[holo_col] if holo_col in df.columns else pd.Series([pd.NA] * len(df), index=df.index)
        normal_series = df[normal_col] if normal_col in df.columns else pd.Series([pd.NA] * len(df), index=df.index)

        df['card_market_value'] = holo_series.fillna(normal_series).fillna(0.0)
        df['card_market_value'] = pd.to_numeric(df['card_market_value'], errors='coerce').fillna(0.0)

        # Standardize column names
        df = df.rename(columns={'id': 'card_id', 'set.id': 'set_id'})

        # Ensure required columns exist (missing will be NaN)
        out_df = df.reindex(columns=required_cols).copy()

        all_lookup_df.append(out_df)

    if not all_lookup_df:
        # Return empty DataFrame with required columns
        return pd.DataFrame(columns=required_cols)

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)

    # Sort by market value (highest first) and drop duplicates keeping the highest value per card_id
    if 'card_market_value' in lookup_df.columns:
        lookup_df = lookup_df.sort_values(by='card_market_value', ascending=False)

    lookup_df = lookup_df.drop_duplicates(subset=['card_id'], keep='first').reset_index(drop=True)

    return lookup_df


def _load_inventory_data(inventory_dir):
    """
    Load CSV inventory files from inventory_dir, concatenate them and create a
    unified 'card_id' key by combining set_id and card_number (format: "{set_id}-{card_number}").
    """
    inventory_data = []

    for fname in os.listdir(inventory_dir):
        if not fname.lower().endswith('.csv'):
            continue

        filepath = os.path.join(inventory_dir, fname)
        try:
            df = pd.read_csv(filepath)
        except Exception:
            # Skip unreadable / invalid CSV files
            continue

        inventory_data.append(df)

    if not inventory_data:
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_data, ignore_index=True)

    # Create unified card_id key
    inventory_df['card_id'] = inventory_df['set_id'].astype(str) + '-' + inventory_df['card_number'].astype(str)

    return inventory_df


def update_portfolio(inventory_dir, lookup_dir, output_file):
    """
    Main ETL: load lookup and inventory, merge, clean, and write final portfolio CSV.
    """
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    # Handle empty inventory
    final_cols = [
        'index', 'card_id', 'set_id', 'card_number',
        'card_market_value', 'set_name',
        'binder_name', 'page_number', 'slot_number'
    ]

    if inventory_df.empty:
        print(f"ERROR: No inventory files found in '{inventory_dir}'. Writing empty portfolio.", file=sys.stderr)
        empty_df = pd.DataFrame(columns=final_cols)
        empty_df.to_csv(output_file, index=False)
        return

    # Merge inventory with lookup (keep all inventory rows)
    lookup_subset = lookup_df.reindex(columns=['card_id', 'card_market_value', 'name'])
    merged = pd.merge(inventory_df, lookup_subset, on='card_id', how='left')

    # Rename 'name' from lookup to 'set_name' for clarity
    if 'name' in merged.columns:
        merged = merged.rename(columns={'name': 'set_name'})
    else:
        merged['set_name'] = pd.NA

    # Final cleaning
    merged['card_market_value'] = pd.to_numeric(merged.get('card_market_value', pd.Series([0.0]*len(merged))), errors='coerce').fillna(0.0)
    merged['set_name'] = merged['set_name'].fillna('NOT_FOUND')

    # Create location index column by concatenating binder_name, page_number, slot_number
    merged['index'] = (
        merged.get('binder_name', pd.Series([''] * len(merged))).astype(str) + '-' +
        merged.get('page_number', pd.Series([''] * len(merged))).astype(str) + '-' +
        merged.get('slot_number', pd.Series([''] * len(merged))).astype(str)
    )

    # Ensure final columns exist (will create with NaN if missing)
    final_df = merged.reindex(columns=final_cols)

    # Write output
    final_df.to_csv(output_file, index=False)
    print(f"Portfolio written to: {output_file}")


def main():
    """Run pipeline against production directories and output."""
    prod_inventory = './card_inventory/'
    prod_lookup = './card_set_lookup/'
    prod_output = 'card_portfolio.csv'
    update_portfolio(prod_inventory, prod_lookup, prod_output)


def test():
    """Run pipeline against test directories and output."""
    test_inventory = './card_inventory_test/'
    test_lookup = './card_set_lookup_test/'
    test_output = 'test_card_portfolio.csv'
    update_portfolio(test_inventory, test_lookup, test_output)


if __name__ == "__main__":
    print("Starting update_portfolio in Test Mode", file=sys.stderr)
    test()

import os
import json
import sys
import pandas as pd

def _load_lookup_data(lookup_dir):
    """
    Load JSON price files from lookup_dir, flatten them and extract the highest
    market price per card_id.

    Returns a DataFrame with one row per card_id (highest market value kept).
    """
    all_lookup_df = []

    required_cols = ['card_id', 'set_id', 'name', 'card_market_value']

    for fname in os.listdir(lookup_dir):
        if not fname.lower().endswith('.json'):
            continue

        filepath = os.path.join(lookup_dir, fname)
        try:
            with open(filepath, 'r', encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception:
            # Skip unreadable / invalid JSON files
            continue

        if 'data' not in data or not isinstance(data['data'], (list, dict)):
            continue

        df = pd.json_normalize(data['data'])

        # Compute card_market_value, preferring holofoil.market then normal.market then 0.0
        holo_col = 'tcgplayer.prices.holofoil.market'
        normal_col = 'tcgplayer.prices.normal.market'

        holo_series = df[holo_col] if holo_col in df.columns else pd.Series([pd.NA] * len(df), index=df.index)
        normal_series = df[normal_col] if normal_col in df.columns else pd.Series([pd.NA] * len(df), index=df.index)

        df['card_market_value'] = holo_series.fillna(normal_series).fillna(0.0)
        df['card_market_value'] = pd.to_numeric(df['card_market_value'], errors='coerce').fillna(0.0)

        # Standardize column names
        df = df.rename(columns={'id': 'card_id', 'set.id': 'set_id'})

        # Ensure required columns exist (missing will be NaN)
        out_df = df.reindex(columns=required_cols).copy()

        all_lookup_df.append(out_df)

    if not all_lookup_df:
        # Return empty DataFrame with required columns
        return pd.DataFrame(columns=required_cols)

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)

    # Sort by market value (highest first) and drop duplicates keeping the highest value per card_id
    if 'card_market_value' in lookup_df.columns:
        lookup_df = lookup_df.sort_values(by='card_market_value', ascending=False)

    lookup_df = lookup_df.drop_duplicates(subset=['card_id'], keep='first').reset_index(drop=True)

    return lookup_df


def _load_inventory_data(inventory_dir):
    """
    Load CSV inventory files from inventory_dir, concatenate them and create a
    unified 'card_id' key by combining set_id and card_number (format: "{set_id}-{card_number}").
    """
    inventory_data = []

    for fname in os.listdir(inventory_dir):
        if not fname.lower().endswith('.csv'):
            continue

        filepath = os.path.join(inventory_dir, fname)
        try:
            df = pd.read_csv(filepath)
        except Exception:
            # Skip unreadable / invalid CSV files
            continue

        inventory_data.append(df)

    if not inventory_data:
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_data, ignore_index=True)

    # Create unified card_id key
    inventory_df['card_id'] = inventory_df['set_id'].astype(str) + '-' + inventory_df['card_number'].astype(str)

    return inventory_df


def update_portfolio(inventory_dir, lookup_dir, output_file):
    """
    Main ETL: load lookup and inventory, merge, clean, and write final portfolio CSV.
    """
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    # Handle empty inventory
    final_cols = [
        'index', 'card_id', 'set_id', 'card_number',
        'card_market_value', 'set_name',
        'binder_name', 'page_number', 'slot_number'
    ]

    if inventory_df.empty:
        print(f"ERROR: No inventory files found in '{inventory_dir}'. Writing empty portfolio.", file=sys.stderr)
        empty_df = pd.DataFrame(columns=final_cols)
        empty_df.to_csv(output_file, index=False)
        return

    # Merge inventory with lookup (keep all inventory rows)
    lookup_subset = lookup_df.reindex(columns=['card_id', 'card_market_value', 'name'])
    merged = pd.merge(inventory_df, lookup_subset, on='card_id', how='left')

    # Rename 'name' from lookup to 'set_name' for clarity
    if 'name' in merged.columns:
        merged = merged.rename(columns={'name': 'set_name'})
    else:
        merged['set_name'] = pd.NA

    # Final cleaning
    merged['card_market_value'] = pd.to_numeric(merged.get('card_market_value', pd.Series([0.0]*len(merged))), errors='coerce').fillna(0.0)
    merged['set_name'] = merged['set_name'].fillna('NOT_FOUND')

    # Create location index column by concatenating binder_name, page_number, slot_number
    merged['index'] = (
        merged.get('binder_name', pd.Series([''] * len(merged))).astype(str) + '-' +
        merged.get('page_number', pd.Series([''] * len(merged))).astype(str) + '-' +
        merged.get('slot_number', pd.Series([''] * len(merged))).astype(str)
    )

    # Ensure final columns exist (will create with NaN if missing)
    final_df = merged.reindex(columns=final_cols)

    # Write output
    final_df.to_csv(output_file, index=False)
    print(f"Portfolio written to: {output_file}")


def main():
    """Run pipeline against production directories and output."""
    prod_inventory = './card_inventory/'
    prod_lookup = './card_set_lookup/'
    prod_output = 'card_portfolio.csv'
    update_portfolio(prod_inventory, prod_lookup, prod_output)


def test():
    """Run pipeline against test directories and output."""
    test_inventory = './card_inventory_test/'
    test_lookup = './card_set_lookup_test/'
    test_output = 'test_card_portfolio.csv'
    update_portfolio(test_inventory, test_lookup, test_output)


if __name__ == "__main__":
    print("Starting update_portfolio in Test Mode", file=sys.stderr)
    test()