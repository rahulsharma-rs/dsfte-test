import pandas as pd
import io
import requests
from flask import Flask, request, flash, redirect, render_template,url_for,send_from_directory
from dsfet import fe_1mol
import os
import uuid


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

        table = result[['SMILES']+result.columns[10:].to_list()][:2].to_html(classes='table table-striped')
        # table
        # filename = str(uuid.uuid4()) + '.csv'
        # table.to_csv(os.path.join(app.root_path, 'download', filename))

        return render_template('morgan.html')
  else:
        return render_template('morgan.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(os.path.join(app.root_path, 'download'), filename)        






if __name__ == '__main__':
    app.run(debug=True)
