from flask import Flask, render_template
import pandas as pd
import simplejson as json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def data():
    SHEET_ID = '1cTDvhpsvd0YwQGj0IfgY_tkS1wKsazo0kh5DRx4e_7k'
    SHEET_NAME = 'Sheet1'
    sheet_link = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
    df = pd.read_csv(sheet_link, on_bad_lines='skip')
    df = df.rename(columns={
        "L": "Language",
        "C": "Class",
        "Term": "Term",
        "Definition": "Definition",
        "Similar terms": "Similar_Terms",
        "Context (example)": "Context/Example",
        "Ambiguity": "Ambiguity",
    })
    for column in ["Language", "Class"]:
        df[column] = df[column].fillna(method='ffill')

    for column in ["Term", "Definition", "Similar_Terms", "Context/Example", "Ambiguity"]:
        df[column] = df[column].fillna("")
    

    entries = df.to_dict('records')
    entries_ = [
        {
        "Language": "ENGLISH",
        "Class": "nation",
        "Term": "nigger/es",
        "Definition": "",
        "Similar_Terms": "",
        "Context/Example": "",
        "Ambiguity": ""
    }
    ]

    return {'data': entries}



    