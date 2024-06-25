from flask import Flask, request, render_template, redirect, url_for, redirect
import pandas as pd
import numpy as np
import openpyxl
import sqlite3
import base64
from io import BytesIO, StringIO
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploaded', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist("files")
    message = ""
    for file in uploaded_files:
        if file:
            # TODO Replace this with actual data processing
            file_stream = BytesIO(file.read()) # Convert file into BytesIO object
            file_stream.seek(0) # return pointer to first character
            df = import_data(file.filename, file_stream)
            return graph_df(df)
            # Read files
            # Merge all dfs (should be provided to us)
            # Update message if any errors
    if message == "":
        message = "Files Uploaded Successfully!"
    return render_template("uploaded.html", message=message)

def import_data(filename, file_stream):
    if filename.endswith('.json'):
        return pd.read_json(file_stream)
    elif filename.endswith('.csv'):
        return pd.read_csv(file_stream)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(file_stream)
    elif filename.endswith('.db'):
        conn = sqlite3.connect(file_stream)
        query = "SELECT name FROM sqlite_master WHERE type = 'table';"
        table_names = pd.read_sql_query(query, conn)['name'].tolist()
        if len(table_names) != 1:
            raise ValueError(f"Expected one table, found {len(table_names)}: {table_names}")
        else:
            query = f"SELECT * FROM {table_names[0]}"
            df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    else:
        raise NameError("Cannot read file.  Can only support .json, .csv, .xlsx, and .db extensions.")

def graph_df(df):
    fig = plt.Figure()
    ax = fig.add_subplot()
    ax.bar(df['Age'], df['Salary'])
    ax.title.set_text('Age vs Salary')
    ax.set_xlabel('Age')
    ax.set_ylabel('Salary')
    return show_fig(fig)

@app.route("/test_plots", methods=['GET'])
def test_plots():
    fig = plt.Figure()
    ax=fig.subplots(2, 2)
    x = np.arange(-100, 100)
    y = np.arange(0, 200)
    ax[0][0].title.set_text("Line Graph")
    ax[0][0].plot(y, x)
    ax[0][1].title.set_text("Bar Graph")
    ax[0][1].bar(y, x)
    ax[1][0].title.set_text("Pie Chart")
    ax[1][0].pie([42, 58], labels=['A', 'B'])
    ax[1][1].title.set_text("Scatter Chart")
    ax[1][1].scatter(np.random.randint(0, 42, len(x)), x)
    fig.tight_layout()
    return show_fig(fig)

def show_fig(fig):
    # Generate the figure **without using pyplot**.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"


if __name__ == '__main__':
    app.run(debug=True)
