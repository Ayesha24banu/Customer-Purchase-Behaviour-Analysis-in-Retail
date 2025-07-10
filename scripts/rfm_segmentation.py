import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# --- Customer Segmentation using RFM & KMeans ---
def perform_rfm_clustering(df: pd.DataFrame, plot: bool = True) -> pd.DataFrame:
    """
    Perform RFM segmentation and clustering using KMeans.

    Args:
        df (pd.DataFrame): Cleaned retail transaction data with InvoiceDate, Invoice, TotalPrice.
        plot (bool): If True, display visualizations and save figures.

    Returns:
        pd.DataFrame: RFM table with Cluster and AOV columns.
    """
    try:
        logging.info(" Starting RFM Segmentation...")

        # 1️. Snapshot date: 1 day after last transaction ( reference point to calculate Recency)
        snapshot = df['InvoiceDate'].max() + pd.Timedelta(days=1)

        # 2️. Aggregate RFM values/metrics: Why only Recency, Frequency, Monetary?
        # Because they reflect customer behavior in a business-relevant way:
        rfm = df.groupby('CustomerID').agg({
            'InvoiceDate': lambda x: (snapshot - x.max()).days,  # Recency: Indicates how recently a customer purchased (days since last purchase)
            'Invoice': 'nunique',                                 # Frequency: Indicates how often they purchase (total unique invoices)
            'TotalPrice': 'sum'                                   # Monetary: Indicates how much they spend (total revenue)
        }).rename(columns={'InvoiceDate': 'Recency', 'Invoice': 'Frequency', 'TotalPrice': 'Monetary'})
        print("RFM calculated successfully")

        print("\n RFM Table (raw):")
        print(rfm.head())

        # Handle extreme outliers using IQR (Interquartile Range) method to improve clustering accuracy for RFM (optional, but good practice for clustering)
        # This removes customers whose R, F, or M are unusually high/low and may distort cluster
        for col in ['Recency', 'Frequency', 'Monetary']:
            Q1 = rfm[col].quantile(0.25)    # 25th percentile (lower quartile) 
            Q3 = rfm[col].quantile(0.75)    # 75th percentile (upper quartile)
            IQR = Q3 - Q1
            rfm = rfm[~((rfm[col] < (Q1 - 1.5 * IQR)) | (rfm[col] > (Q3 + 1.5 * IQR)))]

        # 3️. Standardize RFM features. 
        # Because KMeans_alg is distance-based, and features on different scales bias clustering. so,standardizing ensures equal weight
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm)

        # 4️. Evaluate optimal number of clusters using Elbow and Silhouette method to find best k
        distortions = []        # Inertia: Total within-cluster sum of squares
        silhouette_scores = []  # Silhouette: Measures how well clusters are separated
        K = range(2, 10)

        for k in K:
            model = KMeans(n_clusters=k, random_state=42)
            model.fit(rfm_scaled)
            distortions.append(model.inertia_)
            sil_score = silhouette_score(rfm_scaled, model.labels_)
            silhouette_scores.append(sil_score)
            print(f"\n Silhouette Score for k = {k}: {sil_score:.3f}")

        if plot:
            # Plot Elbow & Silhouette Scores
            # Inertia always decreases as k increases (more specialized clusters)
            # Look for 'elbow' where it stops decreasing rapidly.
            # Silhouette Score: how well-separated the clusters are
            #   1.0 = tight clusters, far apart
            #   0.0 = overlapping
            #  -1.0 = incorrect clustering
            plt.figure(figsize=(10, 5))
            plt.plot(K, distortions, 'bo-', label='Inertia (Elbow)')
            plt.plot(K, silhouette_scores, 'ro-', label='Silhouette Score')
            plt.xlabel('Number of Clusters (k)')
            plt.ylabel('Score')
            plt.title('Elbow & Silhouette Analysis for KMeans', fontsize=14, fontweight='bold')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(r'../outputs/figures/rfm_fig/rfm_Elbow_Silhouette_analysis.png')
            plt.show()
            plt.close()

        # 5️. Final KMeans clustering (set optimal_k = 4 manually)
        optimal_k = 4
        kmeans_model = KMeans(n_clusters=optimal_k, random_state=42)
        rfm['Cluster'] = kmeans_model.fit_predict(rfm_scaled)

        print("\n RFM Table with Clusters:")
        print(rfm.head())

        # 6️. Average Order Value(AOV) = Monetary / Frequency
        rfm['AOV'] = (rfm['Monetary'] / rfm['Frequency']).round(2)

        # 7️. Convert scaled cluster centers back to original RFM scale
        # This helps visualize the average R, F, M per cluster using real-world units
        centers_scaled = kmeans_model.cluster_centers_
        centers_original = pd.DataFrame(
            scaler.inverse_transform(centers_scaled),
            columns=['Recency', 'Frequency', 'Monetary']
        )
        centers_original['Cluster'] = centers_original.index # Label the centers for plotting

        # 8️. Add descriptive segment labels for business understanding
        segment_labels = {
            0: 'Loyal Customers',            # Low Recency, High Frequency, High Monetary
            1: 'Inactive/At-Risk Customers', # High Recency, Low Frequency, Low Monetary
            2: 'Frequent Low-Spenders',      # Low Recency, High Frequency, Low Monetary
            3: 'Recent Big Spenders'         # Low Recency, Low Frequency, High Monetary
        }
        # Assign labels to each customer
        rfm['Segment'] = rfm['Cluster'].map(segment_labels)

        if plot:
            # Heatmap: Mean RFM & AOV by cluster
            #What's the average behavior per cluster?
            # This helps profile each cluster (e.g. high spenders, inactive, loyal customers)
            cluster_summary = rfm.groupby('Cluster')[['Recency', 'Frequency', 'Monetary', 'AOV']].mean().round(1)
            plt.figure(figsize=(8, 5))
            sns.heatmap(cluster_summary, annot=True, cmap='YlGnBu', fmt='.1f')
            plt.title(' Average RFM & AOV Metrics per Cluster', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig(r'../outputs/figures/rfm_fig/rfm_cluster_summary.png')
            plt.show()
            plt.close()

            #SCATTERPLOT: RFM Cluster Segmentation (3 Views)
            plt.figure(figsize=(20, 7))

            # SUBSCATTERPLOT 1: Why plot Recency vs Monetary?
            # Helps identify high-value customers who recently purchased
            plt.subplot(1, 3, 1)
            sns.scatterplot(data=rfm, x='Recency', y='Monetary', hue='Cluster', palette='Set2', s=60)
            plt.scatter(centers_original['Recency'], centers_original['Monetary'],
                        c='black', marker='X', s=200, label='Centroids')
            plt.title('Recency vs Monetary', fontsize=14, fontweight='bold')
            plt.xlabel('Recency (Days since last purchase)')
            plt.ylabel('Monetary £ (Total Spend)')
            plt.grid(True)
            plt.legend(title='Cluster')

            # SUBSCATTERPLOT 2: Why plot Frequency vs Monetary?
            # Identifies frequent and high-spending customers (loyal high-value)
            plt.subplot(1, 3, 2)
            sns.scatterplot(data=rfm, x='Frequency', y='Monetary', hue='Cluster', palette='Set2', s=60)
            plt.scatter(centers_original['Frequency'], centers_original['Monetary'],
                        c='black', marker='X', s=200, label='Centroids')
            plt.title('Frequency vs Monetary', fontsize=14, fontweight='bold')
            plt.xlabel('Frequency (No. of Purchases)')
            plt.ylabel('Monetary £ (Total Spend)')
            plt.grid(True)
            plt.legend(title='Cluster')

            # SUBSCATTERPLOT 3: Why add Recency vs Frequency?
            # Useful to see if recent customers are also frequent buyers
            plt.subplot(1, 3, 3)
            sns.scatterplot(data=rfm, x='Recency', y='Frequency', hue='Cluster', palette='Set2', s=60)
            plt.scatter(centers_original['Recency'], centers_original['Frequency'],
                        c='black', marker='X', s=200, label='Centroids')
            plt.title('Recency vs Frequency', fontsize=14, fontweight='bold')
            plt.xlabel('Recency (Recent Days of purchases)')
            plt.ylabel('Frequency (No. of Purchases)')
            plt.grid(True)
            plt.legend(title='Cluster')

            plt.tight_layout()
            plt.suptitle(' RFM Cluster Segmentation (3 Views)', fontsize=16, fontweight='bold', y=1.05)
            plt.savefig(r'../outputs/figures/rfm_fig/rfm_cluster_views.png')
            plt.show()
            plt.close()
            
        logging.info(" RFM clustering and segmentation completed successfully.")
        return rfm

    except Exception as e:
        logging.error(f" RFM clustering failed: {e}")
        raise