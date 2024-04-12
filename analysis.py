
def generate_umap_feature_plot(gene):
    # Placeholder function to generate an image
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import os
    import seaborn as sns
    import numpy as np
    import psycopg2

    def make_umap_feature_plot(umap, gene):
        plt.figure(figsize=(8, 6), dpi=300)
        x = umap['UMAP_1'] 
        y = umap['UMAP_2']
        scatter = plt.scatter(x, y, c=umap['value'], cmap='hot', s=6)
        plt.colorbar(scatter, label='Gene Expression Level')
        plt.xlabel('UMAP 1')
        plt.ylabel('UMAP 2')
        plt.title(gene)

    # load in umap embeddings
    umap = pd.read_csv('data/stiff.integrated/umap_embeddings.csv')

    # load in all gene names
    genes = []
    with open('data/stiff.integrated/gene_names.txt', 'r') as file:
        for line in file:
            genes.append(line.strip())

    def access_db(gene):
    #access database
        conn_params = {
        "dbname": 'postgres',
        "user": 'postgres',
        "password": 'FcuSshAgM3HezCARpCR9',
        "host": 'scrnaseq-database-acta.ch2yim6a0f08.us-east-2.rds.amazonaws.com',
        "port": '5432'  # Default PostgreSQL port, change if necessary
        }
        try:
            # Connect to the database
            conn = psycopg2.connect(**conn_params)
            cur = conn.cursor()
            
            query = "SELECT * FROM gene_expression WHERE gene_name = %s;"
            cur.execute(query, (gene,))
            
            rows=cur.fetchall()
            results = [list(row) for row in rows]
            #print(results)
        except psycopg2.Error as e:
            print(f"An error occurred: {e}")
        finally:
            # Clean up, close the cursor and connection
            if cur:
                cur.close()
            if conn:
                conn.close()
        return rows


    if gene in genes:
        rows = access_db(gene)
        umap['gene'] = gene
        umap['value'] = 0
        df = pd.DataFrame(rows, columns=['cells', 'gene', 'value'])
        del rows
        merged_df = umap.merge(df, on='cells', how='left', suffixes=('', '_updated'))
        umap['value'] = merged_df['value_updated'].fillna(merged_df['value'])
        del merged_df
        umap['value'] = [float(x) for x in umap['value']]
        umap['value'] = np.log1p(umap['value'])
        make_umap_feature_plot(umap, gene)
    else:
        return 'GENE DOES NOT EXIST'
    # Ensure the directory for the image exists
    image_dir = 'static/images'
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    umap_path = os.path.join(image_dir, 'stiff-plot.png')
    plt.savefig(umap_path)    
    plt.close()


    # Create a violin plot
    plt.figure(figsize=(5,4),dpi=300)  # Adjust the dpi for on-screen display quality
    custom_palette = {'Tumor': 'pink', 'Immune': 'white', 'Fibroblast': 'brown', 'Endothelial':'yellow'}
    sns.violinplot(x='Idents', hue='Idents', y='value', data=umap, palette=custom_palette, bw_method=0.5, inner='quartile', legend=False)
    plt.title(gene)
    violin_path = os.path.join(image_dir, 'stiff-violin-plot.png')
    plt.savefig(violin_path)    
    plt.close()

    # Create a bar plot
    plt.figure(figsize=(5,4), dpi=300)  # Adjust the dpi for on-screen display quality
    sns.barplot(x='Idents', hue='Idents', y='value', data=umap, palette=custom_palette, edgecolor='black', capsize=0.2, 
                    err_kws={'linewidth': 1, 'color': 'black'}, legend=False)
    plt.title(gene)
    bar_path = os.path.join(image_dir, 'stiff-bar-plot.png')
    plt.savefig(bar_path)    
    plt.close()

    #SOFT STUFF
    umap_path1 = os.path.join(image_dir, 'soft-plot.png')

    violin_path1 = os.path.join(image_dir, 'soft-violin-plot.png')

    bar_path1 = os.path.join(image_dir, 'soft-bar-plot.png')


    return [umap_path, violin_path, bar_path, umap_path1, violin_path1, bar_path1]