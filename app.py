import pandas as pd
import io
import requests
from flask import Flask, request, flash, redirect, render_template,url_for,send_from_directory
from dsfet import fe_1mol
import os
import uuid
import plotly.express as px
import umap




app = Flask(__name__)
app.secret_key = 'secretkey'

@app.route('/', methods=['GET', 'POST'])
def upload_csv():
    # counter += 1
    if request.method == 'POST':
        
        
        file = request.files['file']
        df = pd.read_csv(file)
        df1 = df[['SMILES']]
        Train, Test, feature_sequences, feature_to_token_map = fe_1mol.oneMolFeatureExtraction(trainSMILES=df1, testSMILES=None,ngram_list=[1,2,3,4,5,6,7,8])

        table = Train[['SMILES']+Train.columns[4:].to_list()][:2].to_html(classes='table table-striped')

        filename = str(uuid.uuid4()) + '.csv'
        Train.to_csv(os.path.join(app.root_path, 'download', filename), index=False)
        # file_url = url_for('download', filename=filename, _external=True)

        return render_template('nlp.html',filename=filename)
    else:
        return render_template('nlp.html')
    
@app.route('/morgan',  methods=['GET', 'POST'])
def morganFP():
  
  if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        df1 = df[['SMILES']]
        result= fe_1mol.morganFingerPrint(df1, nBits=1024)

        table = result[['SMILES']+result.columns[10:].to_list()]
        # .to_html(classes='table table-striped')
      
        filename = str(uuid.uuid4()) + '.csv'
        table.to_csv(os.path.join(app.root_path, 'download', filename))

        return render_template('morgan.html',filename=filename)
  else:
        return render_template('morgan.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'download'), filename)        


# Adding the Graph API

@app.route('/plot', methods=['GET'])
def plot():
    flag = 0
    file = request.files['file']
    df = pd.read_csv(file)
    df1 = df[['SMILES']]
    Train, Test, feature_sequences, feature_to_token_map = fe_1mol.oneMolFeatureExtraction(trainSMILES=df1, testSMILES=None,ngram_list=[1,2,3,4,5,6,7,8])

    data = pd.read_csv('SMILES_data.csv')
    data = data[['DRUG_NAME', 'PUBCHEM_ID', 'SMILES']]

    if 'DRUG_NAME' in Train.columns.to_list():
        y = Train['DRUG_NAME']
        flag = 1
    else:
        y= None
        flag = 0

    reducer = umap.UMAP(n_components=7, min_dist=0.001, )
    cols = ['DRUG_NAME'] + list(Train.columns[len(data.columns)+1:])

    x = Train[Train.columns[len(data.columns)+1:]].copy(deep=True)

    z = reducer.fit_transform(x.values)

    df = pd.DataFrame()
    if flag== 0:
        pass
    else:
        df["y"] = y
    df["comp-1"] = z[:,0]
    df["comp-2"] = z[:,1]

    if flag==0:
        fig = px.scatter(df, x="comp-1", y="comp-2", size_max=10)
    else:
        fig = px.scatter(df, x="comp-1", y="comp-2", size_max=10,color="y")

    fig.update_traces(textposition='top center',marker=dict(size=10,
                                  line=dict(width=2,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))

    fig.update_layout(
        height=800,
        width=800,
        title_text='GBM Cancer Cell line embedding'
    )

    plot_div = plotly.offline.plot(fig, output_type='div')

    return render_template('plot.html', plot_div=plot_div)




if __name__ == '__main__':
    app.run(debug=True)
