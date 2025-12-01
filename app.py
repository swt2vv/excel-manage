import flask 
import azure.storage.blob
from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for
from azure.storage.blob import BlobServiceClient
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import pandas as pd
import io
from io import StringIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt



AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
EXCEL_CONTAINER = "excel-container"
bsc = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
cc  = bsc.get_container_client(EXCEL_CONTAINER)


app = Flask(__name__)


@app.route("/api/v1/health")
def health():
    return {"status": "ok"}

@app.post("/api/v1/upload")
def upload():
    f = request.files["file"]

    if f.filename == "":
        return jsonify(ok=False, error="empty filename"), 400


    filename = secure_filename(f.filename)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    blob_name = f"{timestamp}-{filename}"    
    
    try:    
        blob_client = cc.get_blob_client(blob_name)
        blob_client.upload_blob(f, overwrite=True)
        blob_url = f"{cc.url}/{blob_name}"
        return redirect("/gallery")

    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500 


@app.post("/delete/<path:filename>")
def delete_file(filename):
    try:
        blob_client = cc.get_blob_client(filename)
        blob_client.delete_blob()
        return redirect("/gallery")
    except Exception as e:
        return f"Delete error: {e}", 500


@app.get("/api/v1/gallery")
def gallery():
    try:
        urls = []
        for b in cc.list_blobs():
            urls.append(f"{cc.url}/{b.name}")
        urls.sort(reverse=True)
        return jsonify(ok=True, gallery=urls)
    except Exception as exc:
        print("error:", exc)
        return jsonify(ok=False, error=str(exc)), 500
        


@app.route("/chart/<path:filename>")
def chart(filename):
    try:
        blob_client = cc.get_blob_client(filename)
        stream = io.BytesIO(blob_client.download_blob().readall())
        df = pd.read_csv(stream) if filename.lower().endswith(".csv") else pd.read_excel(stream)

        distr_null = df.isnull().sum().value_counts()
        plt.figure(figsize=(10,6))
        distr_null.plot(kind="bar")
        plt.title("Distribution of Null Counts Across Columns")
        plt.xlabel("Number of Nulls in a Column")
        plt.ylabel("Number of Columns")
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        return send_file(img, mimetype="image/png")

    except Exception as e:
        return jsonify(ok=False, error=str(e)), 500


@app.route('/api/v1/summary')
def summary_api():
    filename = request.args.get("file")
    files = [b.name for b in cc.list_blobs()]

    if not filename:
        return render_template("summary.html", files=files)

    blob_client = cc.get_blob_client(filename)
    stream = io.BytesIO(blob_client.download_blob().readall())
    df = pd.read_csv(stream) if filename.lower().endswith(".csv") else pd.read_excel(stream)

    shape = df.shape
    columns = df.columns.tolist()
    col_count = shape[1]
    missing_info = df.isnull().sum().to_dict()
    duplicate_count = int(df.duplicated().sum())

    return render_template(
        "summary.html",
        files=files,
        selected_file=filename,
        shape=shape,
        col_count=col_count,
        columns=columns,
        missing_info=missing_info,
        duplicate_count=duplicate_count
    )

@app.route('/')
def index():
    try:
        files = [b.name for b in cc.list_blobs()]
        files.sort(reverse=True)
        return render_template("gallery.html", files=files, cc=cc)
    except Exception as e:
        return f"Error loading gallery: {e}", 500


@app.route('/gallery')
def gallery_page():
    try:
        files = [b.name for b in cc.list_blobs()]
        # sort newest first if you like
        files.sort(reverse=True)
        return render_template("gallery.html", files=files, cc=cc)
    except Exception as e:
        return f"Error loading gallery: {e}", 500

@app.route('/summary')
def summary_page():
    files = [b.name for b in cc.list_blobs()]
    return render_template("summary.html", files=files)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)