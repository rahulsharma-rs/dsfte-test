import umap
import requests
from flask import Flask, request, render_template, url_for, send_from_directory
from dsfet import fe_1mol
import os
import uuid
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.offline
from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        df1 = df[['DRUG_NAME', 'SMILES']]
        Train, Test, feature_sequences, feature_to_token_map = fe_1mol.oneMolFeatureExtraction(
            trainSMILES=df1, testSMILES=None, ngram_list=[1, 2, 3, 4, 5, 6, 7, 8])

        table = Train[['SMILES']+Train.columns[4:].to_list()
                                                           ][:2].to_html(classes='table table-striped')

        filename = str(uuid.uuid4()) + '.csv'
        Train.to_csv(os.path.join(
            app.root_path, 'download', filename), index=False)

        data = df[['DRUG_NAME', 'SMILES']]
        flag = 0
        if 'DRUG_NAME' in Train.columns.to_list():
            y = Train['DRUG_NAME']
            flag = 1
        else:
            y = None
            flag = 0

        reducer = umap.UMAP(n_components=7, min_dist=0.001, )
        cols = ['DRUG_NAME'] + list(Train.columns[len(data.columns)+1:])

        x = Train[Train.columns[len(data.columns)+3:]].copy(deep=True)

        z = reducer.fit_transform(x.values)


        df = pd.DataFrame()

        if flag == 0:
            pass
        else:
            df["y"] = y
        df["comp-1"] = z[:, 0]
        df["comp-2"] = z[:, 1]

        if flag == 0:
            fig = px.scatter(df, x="comp-1", y="comp-2", size_max=10)
        else:
            fig = px.scatter(df, x="comp-1", y="comp-2", size_max=10, color="y")

        fig.update_traces(textposition='top center', marker=dict(size=10,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))

        fig.update_layout(
        height=600,
        
        width=600,
        title_text='Umap-2D Embedding of Extracted Drug Features')
        fig.update_layout(title_text='Umap-2D Embedding of Extracted Drug Features', title_x=0.5)


        plot_div = plotly.offline.plot(fig, output_type='div')

        return render_template('nlp.html', filename=filename, plot_div=plot_div)
    else:
        return render_template('nlp.html')


    
@app.route('/morgan',  methods=['GET', 'POST'])
def morganFP():
  
  if request.method == 'POST':
        file = request.files['file']
        nBits = int(request.form.get('nBits', 1024))
        df = pd.read_csv(file)
        # data = df[['DRUG_NAME', 'PUBCHEM_ID', 'SMILES']]
        df1 = df[['DRUG_NAME','SMILES']]
        result= fe_1mol.morganFingerPrint(df1, nBits=nBits)
        # Train=result

        table = result[['SMILES']+result.columns[10:].to_list()]
        # .to_html(classes='table table-striped')
      
        filename = str(uuid.uuid4()) + '.csv'
        table.to_csv(os.path.join(app.root_path, 'download', filename))

        # from here the graph code for morgan
       
        data = df[['DRUG_NAME','SMILES']]
        flag = 0
        if 'DRUG_NAME' in result.columns.to_list():
            y = result['DRUG_NAME']
            flag = 1
        else:
            y = None
            flag = 0

        reducer = umap.UMAP(n_components=7, min_dist=0.001, )
        cols = ['DRUG_NAME'] + list(result.columns[len(data.columns)+1:])

        x = result[result.columns[len(data.columns)+1:]].copy(deep=True)

        z = reducer.fit_transform(x.values)


        df = pd.DataFrame()

        if flag == 0:
            pass
        else:
            df["y"] = y
        df["comp-1"] = z[:, 0]
        df["comp-2"] = z[:, 1]

        if flag == 0:
            fig = px.scatter(df, x="comp-1", y="comp-2", size_max=10)
        else:
            fig = px.scatter(df, x="comp-1", y="comp-2", size_max=10, color="y")

        fig.update_traces(textposition='top center', marker=dict(size=10,
                              line=dict(width=2,
                                        color='DarkSlateGrey')),
                  selector=dict(mode='markers'))

        fig.update_layout(
        height=600,
        
        width=600,
        title_text=f'Umap-2D Embedding of Extracted Drug Features for {nBits} bits' )
        fig.update_layout(title_text=f'Umap-2D Embedding of Extracted Drug Features for {nBits} bits', title_x=0.5)


        plot_div = plotly.offline.plot(fig, output_type='div')


        return render_template('morgan.html',filename=filename, plot_div=fig.to_html(full_html=False))
  else:
        return render_template('morgan.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'download'), filename)        





if __name__ == '__main__':
    app.run(debug=True)
