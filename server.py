from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename

import random
import time
import pandas as pd
import os

from traffic import directTraffic, multi_directTraffic


# Function to delete selected files
def delete_files(selected_files):
    for file in selected_files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.exists(file_path):
            os.remove(file_path)


app = Flask(__name__)
app.secret_key = 'my_secret_key'

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

filename = ''


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'submit_button' in request.form:
            submit_value = request.form['submit_button']

            if submit_value == 'del':
                selected_files = request.form.getlist('file-checkbox')
                delete_files(selected_files)
                
            elif submit_value == 'read':
                selected_files = request.form.getlist('file-checkbox')
                data_file, selected_files = read_uploaded_file(selected_files)
                file_list = os.listdir(app.config['UPLOAD_FOLDER'])
                return render_template('index.html', files=file_list, data_file=data_file, selected_files=selected_files)
                
            elif submit_value == 'run':
                selected_files = request.form.getlist('file-checkbox')
                # Print the selected file names
                # print('Selected files:', selected_files)
                if len(selected_files) == 1 and '.xlsx' in selected_files[0]:
                    file_path = os.path.join(
                        app.config['UPLOAD_FOLDER'], selected_files[0])
                    # Read the Excel file using pandas
                    df = pd.read_excel(file_path)
                    urls = df['Danh sách bài viết'].tolist()
                    number_traffics = df['Random Number'].tolist()
                    
                    try:
                        # for url in df['Danh sách bài viết']:
                        #     directTraffic(url)
                        multi_directTraffic(urls, number_traffics)
                        pass
                    except:
                        print("Error")

    file_list = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=file_list)


@app.route('/upload', methods=['POST'])
def upload():
    global filename
    # Check if the 'file' key is in the request.files
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    print("file", file)

    # If the user does not select a file, the browser submits an empty file
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))

    # Save the file to the upload folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    filename = file.filename

    flash('File uploaded successfully', 'success')
    return redirect(url_for('index'))


def read_uploaded_file(selected_files):
    if len(selected_files) == 1 and '.xlsx' in selected_files[0]:
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], selected_files[0])
        # Read the Excel file using pandas
        df = pd.read_excel(file_path)
        urls = df['Danh sách bài viết'].tolist()
        

        random_numbers = []
        for i in df.iloc[:, 1]:
            min_value, max_value = map(int, i.split(','))
            random_number = random.randint(min_value, max_value)
            random_numbers.append(random_number)

        df['Random Number'] = random_numbers
        # Ghi DataFrame đã cập nhật vào tệp Excel
        df.to_excel(file_path, index=False)
        # Lấy nội dung cột 'Danh sách bài viết' và 'Random Number'
        urls = df['Danh sách bài viết'].tolist()
        random_numbers = df['Random Number'].tolist()
        
        data_file = list(zip(urls, random_numbers))
    
    return data_file, selected_files


if __name__ == '__main__':
    app.run(debug=True)
