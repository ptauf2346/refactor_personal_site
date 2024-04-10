
def generate_umap_feature_plot(gene):
    # Placeholder function to generate an image
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    from IPython.display import Image
    import anndata
    import os
    import seaborn as sns
    import h5py 
    import numpy as np

    def make_umap_feature_plot(umap, adata, gene):
        plt.figure(figsize=(8, 6), dpi=300)
        x = umap['UMAP_1'] 
        y = umap['UMAP_2']
        scatter = plt.scatter(x, y, c=adata[:, gene].X, cmap='hot', vmax=np.median(adata[:,gene].X)*2, s=6)
        plt.colorbar(scatter, label='Gene Expression Level')
        plt.xlabel('UMAP 1')
        plt.ylabel('UMAP 2')
        plt.title(gene)

    #adata = anndata.read_h5ad('data/stiff.integrated/stiff_integrated.h5ad')
    #norm_adata = anndata.read_h5ad('data/stiff.integrated/stiff_integrated_norm.h5ad')
    #sct_norm_adata = anndata.read_h5ad('data/stiff.integrated/stiff_integrated_sct.h5ad')
    dataset_path = 'sparse_matrix'
    # load in umap embeddings
    umap = pd.read_csv('data/stiff.integrated/umap_embeddings.csv')

    # load in all gene names
    genes = []
    with open('data/stiff.integrated/gene_names.txt', 'r') as file:
        for line in file:
            genes.append(line.strip())

    # load in normalized counts
    h5_file = 'data/stiff.integrated/normalized_counts_data.h5'
    with h5py.File(h5_file, 'r') as f:
        data = np.array(f[dataset_path])
        #print(data.shape)
        
    cell_labels = umap['cells']
    gene_labels = genes

    norm_adata = anndata.AnnData(X=data, obs=pd.DataFrame(index=cell_labels), var=pd.DataFrame(index=gene_labels))

    # load in SCT normalized counts and SCT genes
    h5_file = 'data/stiff.integrated/sct_normalized_counts_data.h5'
    with h5py.File(h5_file, 'r') as f:
        data = np.array(f[dataset_path])
        #print(data.shape)
        
    cell_labels = umap['cells']
    sct_genes = []
    with open('data/stiff.integrated/sct_gene_names.txt', 'r') as file:
        for line in file:
            sct_genes.append(line.strip())

    sct_norm_adata = anndata.AnnData(X=data, obs=pd.DataFrame(index=cell_labels), var=pd.DataFrame(index=sct_genes))



    # check to see if gene is in the SCT library
    #if gene in sct_genes:
    #    umap[gene] = sct_norm_adata[:, gene].X.flatten()
    #    make_umap_feature_plot(umap, sct_norm_adata, gene)
    #elif gene in genes:
    #    umap[gene] = norm_adata[:, gene].X.flatten()
    #    make_umap_feature_plot(umap, norm_adata, gene)
    #else:
    #    return 'GENE DOES NOT EXIST'
       # check to see if gene is in the SCT library

    if gene in genes:
        umap[gene] = norm_adata[:, gene].X.flatten()
        make_umap_feature_plot(umap, norm_adata, gene)
    else:
        return 'GENE DOES NOT EXIST'
    

    # Ensure the directory for the image exists
    image_dir = 'static/images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    umap_path = os.path.join(image_dir, 'stiff-plot.png')
    plt.savefig(umap_path)    
    plt.close()

    # Group the DataFrame by 'group_column' and collect the 'value_column' values into lists
    grouped_values = umap.groupby('Idents')[gene].apply(list)

    # Create a violin plot
    plt.figure(figsize=(5,4),dpi=300)  # Adjust the dpi for on-screen display quality
    custom_palette = {'Tumor': 'pink', 'Immune': 'white', 'Fibroblast': 'brown', 'Endothelial':'yellow'}
    sns.violinplot(x='Idents', hue='Idents', y=gene, data=umap, palette=custom_palette, bw_method=0.5, inner='quartile', legend=False)
    plt.title(gene)
    violin_path = os.path.join(image_dir, 'stiff-violin-plot.png')
    plt.savefig(violin_path)    
    plt.close()

    # Create a bar plot
    plt.figure(figsize=(5,4), dpi=300)  # Adjust the dpi for on-screen display quality
    sns.barplot(x='Idents', hue='Idents', y=gene, data=umap, palette=custom_palette, edgecolor='black', capsize=0.2, 
                    err_kws={'linewidth': 1, 'color': 'black'}, legend=False)
    plt.title(gene)
    bar_path = os.path.join(image_dir, 'stiff-bar-plot.png')
    plt.savefig(bar_path)    
    plt.close()



    #NOW DO IT FOR SOFT
    #adata = anndata.read_h5ad('data/soft.integrated/soft_integrated.h5ad')
    #norm_adata = anndata.read_h5ad('data/soft.integrated/soft_integrated_norm.h5ad')
    #sct_norm_adata = anndata.read_h5ad('data/soft.integrated/soft_integrated_sct.h5ad')

    # load in umap embeddings
    umap = pd.read_csv('data/soft.integrated/umap_embeddings.csv')

    # load in all gene names
    genes = []
    with open('data/soft.integrated/gene_names.txt', 'r') as file:
        for line in file:
            genes.append(line.strip())

    # load in normalized counts
    h5_file = 'data/soft.integrated/normalized_counts_data.h5'
    with h5py.File(h5_file, 'r') as f:
        data = np.array(f[dataset_path])
        #print(data.shape)
        
    cell_labels = umap['cells']
    gene_labels = genes

    norm_adata = anndata.AnnData(X=data, obs=pd.DataFrame(index=cell_labels), var=pd.DataFrame(index=gene_labels))

    # load in SCT normalized counts and SCT genes
    h5_file = 'data/soft.integrated/sct_normalized_counts_data.h5'
    with h5py.File(h5_file, 'r') as f:
        data = np.array(f[dataset_path])
        #print(data.shape)
        
    cell_labels = umap['cells']
    sct_genes = []
    with open('data/soft.integrated/sct_gene_names.txt', 'r') as file:
        for line in file:
            sct_genes.append(line.strip())

    sct_norm_adata = anndata.AnnData(X=data, obs=pd.DataFrame(index=cell_labels), var=pd.DataFrame(index=sct_genes))



    # check to see if gene is in the SCT library
    if gene in sct_genes:
        umap[gene] = sct_norm_adata[:, gene].X.flatten()
        make_umap_feature_plot(umap, sct_norm_adata, gene)
    elif gene in genes:
        umap[gene] = norm_adata[:, gene].X.flatten()
        make_umap_feature_plot(umap, norm_adata, gene)
    else:
        return 'GENE DOES NOT EXIST'
        # Ensure the directory for the image exists
    image_dir = 'static/images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    umap_path1 = os.path.join(image_dir, 'soft-plot.png')
    plt.savefig(umap_path1)    
    plt.close()

    # Group the DataFrame by 'group_column' and collect the 'value_column' values into lists
    grouped_values = umap.groupby('Idents')[gene].apply(list)

    # Create a violin plot
    plt.figure(figsize=(5,4),dpi=300)  # Adjust the dpi for on-screen display quality
    custom_palette = {'Tumor': 'pink', 'Immune': 'white', 'Fibroblast': 'brown', 'Endothelial':'yellow'}
    sns.violinplot(x='Idents', hue='Idents', y=gene, data=umap, palette=custom_palette, bw_method=0.5, inner='quartile', legend=False)
    plt.title(gene)
    violin_path1 = os.path.join(image_dir, 'soft-violin-plot.png')
    plt.savefig(violin_path1)    
    plt.close()

    # Create a bar plot
    plt.figure(figsize=(5,4), dpi=300)  # Adjust the dpi for on-screen display quality
    sns.barplot(x='Idents', hue='Idents', y=gene, data=umap, palette=custom_palette, edgecolor='black', capsize=0.2, 
                    err_kws={'linewidth': 1, 'color': 'black'}, legend=False)
    plt.title(gene)
    bar_path1 = os.path.join(image_dir, 'soft-bar-plot.png')
    plt.savefig(bar_path1)    
    plt.close()

    return [umap_path, violin_path, bar_path, umap_path1, violin_path1, bar_path1]