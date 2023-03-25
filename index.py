from flask import Flask, render_template, send_file, request
import pandas as pd

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
    print(df)
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

    df["Language"] = df["Language"].apply(lambda x: x.capitalize())

    for column in ["Term", "Definition", "Similar_Terms", "Context/Example", "Ambiguity"]:
        df[column] = df[column].fillna("")
    
    terms = df["Term"].apply(lambda x: x.split('\n')[0])

    df["Twitter Examples Path"] = "Twitter Examples/" + df["Language"] + "/" + terms + ".csv"
    print(df["Twitter Examples Path"])

    entries = df.to_dict('records')
    print(entries)

    return {'data': entries}


@app.route('/download_csv/') # this is a job for GET, not POST
def plot_csv():
    args = request.args
    file_path = args.get('file_path')
    return send_file(
        file_path,
        mimetype='text/csv',
        download_name=file_path.split('/')[-1],
        as_attachment=True
    )



    