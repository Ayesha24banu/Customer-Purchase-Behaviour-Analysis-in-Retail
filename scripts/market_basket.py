import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.frequent_patterns import apriori, association_rules
import logging

# --- Market Basket Analysis using Apriori Algorithm ---
def perform_market_basket_analysis(df: pd.DataFrame, country: str = None, min_support: float = 0.02, min_confidence: float = 0.3, min_lift: float = 1.0, top_rules: int = 10) -> pd.DataFrame:
    """
    Perform Market Basket Analysis using Apriori algorithm and generate Association Rules.

    Parameters:
        df (pd.DataFrame): Cleaned transactional data.
        country (str): Optional. Filter data by country. If None, use full dataset.
        min_support (float): Minimum support value.
        min_confidence (float): Minimum confidence value.
        min_lift (float): Minimum lift value.
        top_rules (int): Number of top rules to return.

    Returns:
        pd.DataFrame: Top N association rules.
    """
    try:
        print(" Starting Market Basket Analysis...")
        logging.info("Market Basket Analysis started")

        # Step 1: Filter by country if provided
        if country:
            df = df[df['Country'] == country]
            print(f" Country Filter Applied: {country}")
            logging.info(f"Filtered data for country: {country}")
        else:
            print(" No country specified — using full dataset.")
            logging.info("No country filter applied, using entire dataset")

        # Step 2: Convert to basket format (1 row per Invoice, columns = products, Values → 0/1)
        print("Creating basket matrix (Invoice x Products)...")
        basket = (df.groupby(['Invoice', 'Description'])['Quantity']
                    .sum().unstack().reset_index().fillna(0)
                    .set_index('Invoice'))

        # Step 3: Convert quantities to 1/0 (Binary Encoding — 1 if item was purchased, 0 otherwise)
        print("Converting quantities to binary (1=Purchased, 0=Not Purchased)...")
        basket_encoded = (basket > 0).astype(int)
        print('basket_encoded:', basket_encoded)

        # Step 4: Apply Apriori Algorithm 
        # Find frequent itemsets
        print(f"Applying Apriori with min_support={min_support}...")
        frequent_itemsets = apriori(basket_encoded, min_support=min_support, use_colnames=True)
       
        print(f"Frequent Itemsets Found: {len(frequent_itemsets)} with support >= {min_support}")
        logging.info(f"Frequent Itemsets Found: {len(frequent_itemsets)} with support >= {min_support}")
        print(frequent_itemsets)

        
        # Step 5: Generate association rules
        print("🔗 Generating Association Rules...")
        rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)
        rules = rules[rules['confidence'] >= min_confidence]

        print(f"Rules Generated: {len(rules)} (Confidence ≥ {min_confidence}, Lift ≥ {min_lift})")
        logging.info(f"Generated {len(rules)} rules with min confidence={min_confidence} and lift={min_lift}")
        print(rules)
        
        # Step 6: Sort by lift and confidence & Display Top Rules
        top_rules_df = rules.sort_values(['lift', 'confidence'], ascending=False)
        top_rules_df.reset_index(drop=True, inplace=True)

        # Add Rule Number Column for reference
        top_rules_df['Rule No.'] = top_rules_df.index + 1
        
        print("\n Top Association Rules:")
        for idx, row in top_rules_df.iterrows():
            print(f"{idx+1}. antecedents: {set(row['antecedents'])} ➡ consequents: {set(row['consequents'])} | Support: {row['support']:.3f}, Confidence: {row['confidence']:.2f}, Lift: {row['lift']:.2f}")
            logging.info(f"Rule {idx+1}: {set(row['antecedents'])} => {set(row['consequents'])} | \
                      Support: {row['support']:.2f}, Confidence: {row['confidence']:.2f}, Lift: {row['lift']:.2f}")
        
        # Save to CSV
        top_rules_df.to_csv( r"../outputs/data/final_association_rules.csv", index=False)
        print(f"\n Market Basket Rules saved to ../outputs/data/final_association_rules.csv")
        logging.info(f"Association rules saved to: ../outputs/data/final_association_rules.csv")

        # Step 7: Visualize Scatter Plot: Support vs Confidence vs Lift
        print("\n Plotting: Lift vs Confidence Scatter Plot...")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=top_rules_df, x='support', y='confidence',
                        size='lift', hue='lift', palette='viridis', sizes=(40, 300),legend=True)

        # Label each point with Rule No.
        for i, row in top_rules_df.iterrows():
            plt.text(row['support'], row['confidence'], str(row['Rule No.']),
                     horizontalalignment='center', verticalalignment='center',
                     fontsize=8, weight='bold', color='black', bbox=dict(boxstyle="circle", facecolor='white', alpha=0.6))

        plt.title('Top Association Rules: Lift vs Confidence (Bubble size = Lift) \nRule No. indicates each association rule', fontsize=14, fontweight='bold')
        plt.xlabel('Support: (Frequency in Transactions)')
        plt.ylabel('Confidence: (Likelihood of Next Purchase)')
        plt.grid(True)
        plt.tight_layout()
        plt.legend(title='Lift (Strength of association)')
        plt.savefig(r'../outputs/figures/mba_fig/top_association_rules.png')
        plt.show()
        plt.close()

        # --- Step 9: Bar Plot (Lift Values) ---
        print(" Plotting: Bar Plot (Top Rules by Lift)...")
        plt.figure(figsize=(10, 6))
        sns.barplot(data=top_rules_df, y='lift', x='Rule No.', palette='coolwarm')

        # Add labels with strength interpretation
        for i, row in top_rules_df.iterrows():
            strength = "Weak" if row['lift'] < 3 else "Moderate" if row['lift'] < 6 else "Strong"
            plt.text(i, row['lift'] + 0.2, f"{row['lift']:.2f}\n({strength})", ha='center', fontsize=8)

        plt.title(" Top Association Rules by Lift \n(Lift > 1: Positive Association, >10: Very Strong)" , fontsize=14, fontweight='bold')
        plt.xlabel("Rule Number: Indicates each association rule")
        plt.ylabel("Lift\n(How many times more likely B is bought when A is bought)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(r'../outputs/figures/mba_fig/top_rules_by_lift.png')
        plt.show()
        plt.close()

        print("\n Market Basket Analysis completed and plotted.")
        return top_rules_df

    except Exception as e:
        logging.error(f" Market Basket Analysis failed: {e}")
        print(f" Error occurred during Market Basket Analysis: {e}")
        raise