from flask import Flask, render_template, request
import pandas as pd
from dsfet import fe_1mol
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        df1 = df[['SMILES']]
        Train, Test, feature_sequences, feature_to_token_map = fe_1mol.oneMolFeatureExtraction(trainSMILES=df1, testSMILES=None,ngram_list=[1,2,3,4,5,6,7,8])

        table = Train[['SMILES']+Train.columns[4:].to_list()][:2].to_html(classes='table table-striped')

        return render_template('index.html', table=table)
    else:
        return render_template('index.html')

@app.route('/morgan', methods=['GET', 'POST'])
def morganFP():
    if request.method == 'POST':
        file = request.files['file']
        df = pd.read_csv(file)
        df1 = df[['SMILES']]
        result= fe_1mol.morganFingerPrint(df, nBits=1024)

        table = result[['SMILES']+result.columns[10:].to_list()][:2].to_html(classes='table table-striped')

        return render_template('index.html', table=table)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)