
def generate_umap_feature_plot(gene):
    # Placeholder function to generate an image
    import pandas as pd
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import os
    from seaborn import violinplot, barplot
    from numpy import log1p
    import psycopg2

    def load_umap(condition):
        if condition == 'stiff':
            umap = pd.read_csv('data/stiff.integrated/umap_embeddings.csv')
        else:
            umap = pd.read_csv('data/soft.integrated/umap_embeddings.csv')
        table = ''.join([condition, '_integrated_norm_counts'])
        rows = access_db(table, gene)
        umap['gene'] = gene
        umap['value'] = 0
        df = pd.DataFrame(rows, columns=['cells', 'gene', 'value'])
        del rows
        merged_df = umap.merge(df, on='cells', how='left', suffixes=('', '_updated'))
        umap['value'] = merged_df['value_updated'].fillna(merged_df['value'])
        del merged_df
        umap['value'] = [float(x) for x in umap['value']]
        umap['value'] = log1p(umap['value'])
        return umap

    def access_db(table, gene):
    #access database
        password = os.environ.get('SECRET_AWS_PASSWORD')
        conn_params = {
        "dbname": 'postgres',
        "user": 'postgres',
        "password": password,
        "host": 'scrnaseq-database-acta.ch2yim6a0f08.us-east-2.rds.amazonaws.com',
        "port": '5432'  # Default PostgreSQL port, change if necessary
        }
        try:
            # Connect to the database
            conn = psycopg2.connect(**conn_params)
            cur = conn.cursor()
            
            query = f"SELECT * FROM {table} WHERE gene_name = %s;"
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
    
    def make_umap_feature_plot(condition, gene):
        umap = load_umap(condition)
        plt.figure(figsize=(8, 6), dpi=300)
        x = umap['UMAP_1'] 
        y = umap['UMAP_2']
        scatter = plt.scatter(x, y, c=umap['value'], cmap='hot', s=6)
        plt.colorbar(scatter, label='Gene Expression Level')
        plt.xlabel('UMAP 1')
        plt.ylabel('UMAP 2')
        plt.title(gene)
        # Ensure the directory for the image exists
        image_dir = 'static/images'
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        if condition == 'stiff':
            umap_path = os.path.join(image_dir, 'stiff-plot.png')
        else:
            umap_path = os.path.join(image_dir, 'soft-plot.png')
        plt.savefig(umap_path)    
        plt.close()
        return umap, umap_path
    
    # load in all gene names
    genes = []
    with open('data/stiff.integrated/gene_names.txt', 'r') as file:
        for line in file:
            genes.append(line.strip())

    if gene in genes:
        umap, umap_path = make_umap_feature_plot('stiff', gene)
    else:
        return 'GENE DOES NOT EXIST'
    
    image_dir = 'static/images'

    # Create a violin plot
    plt.figure(figsize=(5,4),dpi=300)  # Adjust the dpi for on-screen display quality
    custom_palette = {'Tumor': 'pink', 'Immune': 'white', 'Fibroblast': 'brown', 'Endothelial':'yellow'}
    violinplot(x='Idents', hue='Idents', y='value', data=umap, palette=custom_palette, bw_method=0.5, inner='quartile', legend=False)
    plt.title(gene)
    plt.ylabel('nlog(1+counts)')
    violin_path = os.path.join(image_dir, 'stiff-violin-plot.png')
    plt.savefig(violin_path)    
    plt.close()

    # Create a bar plot
    plt.figure(figsize=(5,4), dpi=300)  # Adjust the dpi for on-screen display quality
    barplot(x='Idents', hue='Idents', y='value', data=umap, palette=custom_palette, edgecolor='black', capsize=0.2, 
                    err_kws={'linewidth': 1, 'color': 'black'}, legend=False)
    plt.title(gene)
    plt.ylabel('nlog(1+counts)')
    bar_path = os.path.join(image_dir, 'stiff-bar-plot.png')
    plt.savefig(bar_path)    
    plt.close()

    #SOFT STUFF
    # load in all gene names
    genes = []
    with open('data/soft.integrated/gene_names.txt', 'r') as file:
        for line in file:
            genes.append(line.strip())

    if gene in genes:
        umap, umap_path1 = make_umap_feature_plot('soft', gene)
    else:
        return 'GENE DOES NOT EXIST'

    # Create a violin plot
    plt.figure(figsize=(5,4),dpi=300)  # Adjust the dpi for on-screen display quality
    custom_palette = {'Tumor': 'pink', 'Immune': 'white', 'Fibroblast': 'brown', 'Endothelial':'yellow'}
    violinplot(x='Idents', hue='Idents', y='value', data=umap, palette=custom_palette, bw_method=0.5, inner='quartile', legend=False)
    plt.title(gene)
    plt.ylabel('nlog(1+counts)')
    violin_path1 = os.path.join(image_dir, 'soft-violin-plot.png')
    plt.savefig(violin_path1)
    plt.close()

    # Create a bar plot
    plt.figure(figsize=(5,4), dpi=300)  # Adjust the dpi for on-screen display quality
    barplot(x='Idents', hue='Idents', y='value', data=umap, palette=custom_palette, edgecolor='black', capsize=0.2, 
                    err_kws={'linewidth': 1, 'color': 'black'}, legend=False)
    plt.title(gene)
    plt.ylabel('nlog(1+counts)')
    bar_path1 = os.path.join(image_dir, 'soft-bar-plot.png')
    plt.savefig(bar_path1)    
    plt.close()

    return [umap_path, violin_path, bar_path, umap_path1, violin_path1, bar_path1]