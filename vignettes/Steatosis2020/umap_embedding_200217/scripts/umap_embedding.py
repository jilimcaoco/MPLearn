
import sys
import argparse

import pandas as pd
import joblib
from MPLearn import embedding

DESCRIPTION="""Do the embedding for one dataset with one set of parameters
version 0.0.1

Usage, for example:

    cd MPLearn/vignettes/Steatosis2020/umap_embedding_200217
    python scripts/umap_embedding.py \
        --dataset intermediate_data/cf10k.joblib \
        --embed_dir intermediate_data/cf10k_embedding_pca20_umap2_1_1_euclid \
        --umap_n_neighbors 1 \
        --umap_min_dist 1 
"""

def main(argv):
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(
        "--dataset", type=str, action="store", dest="dataset",
        help="""a pandas dataframe located in .joblib file""")
    parser.add_argument(
        "--tag", type=str, action="store", dest="tag",
        help="""Directory where to store umap embedding and output images""")
    parser.add_argument(
        "--pca_n_components", type=int, action="store", dest="pca_n_components", default=20,
        help="""Dimension of the preliminary PCA embedding""")
    parser.add_argument(
        "--umap_n_neighbors", type=int, action="store", dest="umap_n_neighbors", default=0,
        help="""Number of neighbors when computing UMAP embedding""")
    parser.add_argument(
        "--umap_min_dist", type=float, action="store", dest="umap_min_dist", default=0.0,
        help="""Minimum distance between points in UMAP embedding""")
    parser.add_argument(
        "--umap_init", type=str, action="store", dest="umap_init", default='spectral',
        help="""UMAP initialization. Spectral is prefered, but random is more robust""")
    parser.add_argument(
        "--compute_hdbscan_clusters", type=bool, action="store", dest="compute_hbscan_clusters", default=True,
        help="""Compute HBSCAN clusters and store in the tagged directory""")
    parser.add_argument(
        "--verbose", type=bool, action="store", dest="verbose", default=False,
        help="""Verbose output""")

    arguments = parser.parse_args()

    dataset = joblib.load(arguments.dataset)

    if arguments.verbose:
        print("Computing UMAP embedding clusters ...")    
    dataset_embedding = embedding.fit_embedding(
        dataset=dataset,
        embed_dir="intermediate_data/{}".format(arguments.tag),
        pca_n_components=arguments.pca_n_components,
        umap_init=arguments.umap_init,
        umap_n_neighbors=arguments.umap_n_neighbors,
        umap_min_dist=arguments.umap_min_dist,
        verbose=arguments.verbose)
    embedding.plot_embedding(
        embedding=dataset_embedding,
        plot_width=2000,
        plot_height=2000,
        output_fname="product/figures/{}_embedding.png".format(arguments.tag))

    if arguments.compute_hbscan_clusters:
        if arguments.verbose:
            print("Computing HBSCAN clusters ...")
        clusterer = hdbscan.HDBSCAN(min_cluster_size=3)
        cluster_labels = full_clusterer.fit_predict(embedding)
        joblib.dump(
            value=clusterer,
            filename="intermediate_data/{}/hdbscan_clusterer.joblib".format(arguments.tag))
        joblib.dump(
            value=cluster_labels,
            filename="intermediate_data/{}/hdbscan_clustering.joblib".format(arguments.tag))

if __name__ == "__main__":
    main(sys.argv)
