import os
import sys
import pandas as pd

def generate_summary(portfolio_file):
    
    if not os.path.exists(portfolio_file):
        print(f"ERROR: Portfolio file not found: {portfolio_file}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)

    if df.empty:
        print(f"No data in portfolio file: {portfolio_file}", file=sys.stderr)
        return

    # Ensure numeric values for calculations
    df['card_market_value'] = pd.to_numeric(df.get('card_market_value', pd.Series([0.0]*len(df))), errors='coerce').fillna(0.0)

    total_portfolio_value = df['card_market_value'].sum()

    # Find most valuable card row
    most_idx = df['card_market_value'].idxmax()
    most_valuable_card = df.loc[most_idx]

    card_name = most_valuable_card.get('set_name') or most_valuable_card.get('name') or ''
    card_id = most_valuable_card.get('card_id', '')
    card_value = most_valuable_card['card_market_value']

    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print(f"Most Valuable Card: {card_name} (ID: {card_id}) - ${card_value:,.2f}")


def main():
    prod_portfolio = 'card_portfolio.csv'
    generate_summary(prod_portfolio)


def test():
    test_portfolio = 'test_card_portfolio.csv'
    generate_summary(test_portfolio)


if __name__ == "__main__":
    print("Starting generate_summary in Test Mode", file=sys.stderr)
    test()