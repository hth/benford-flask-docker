from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for
from werkzeug import utils

import csv
import os
import tempfile

import matplotlib.pyplot as plt
import numpy as np

# Location has to be in config file
UPLOAD_FOLDER = '/tmp/upload'

# Supported file extensions
ALLOWED_EXTENSIONS = {'txt', 'csv', 'xls'}

# 16 megabytes
MAX_CONTENT_LENGTH = 16 * 1000 * 1000

benfordLaw_page = Blueprint('benfordLaw_page', __name__, template_folder='templates')
csv.register_dialect('piper', delimiter='\t', quoting=csv.QUOTE_NONE)


@benfordLaw_page.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('error.html', userFriendlyErrorMessage="Missing file part")

        f = request.files['file']
        try:
            if f.filename == '':
                return render_template('error.html', userFriendlyErrorMessage="No file selected")
            # if len(f.read()) == 0:
            #     return render_template('error.html', userFriendlyErrorMessage="Blank file uploaded")
            if f and allowed_file_type(f.filename):
                name = utils.secure_filename(f.filename)
                filepath = os.path.join(UPLOAD_FOLDER, randomize_file_name(name))
                f.save(filepath)

                benford_array = [0] * 9
                incorrect_format = ''
                with open(filepath, newline='\n') as csvfile:
                    data = csv.reader(csvfile, delimiter='\t')
                    for row in data:
                        try:
                            if len(row) == 3 and row[2].isnumeric():
                                benford_array[int(row[2][0]) - 1] = benford_array[int(row[2][0]) - 1] + 1
                            else:
                                # Before correction
                                # Benford: [5735, 3540, 2341, 1847, 1559, 1370, 1166, 1042, 903]
                                # After Correction
                                # Benford: [5738, 3540, 2342, 1847, 1559, 1370, 1166, 1043, 904]
                                corrected = list_to_string(row).rpartition(' ')[2]
                                if corrected.isnumeric():
                                    benford_array[int(corrected[0]) - 1] = benford_array[int(corrected[0]) - 1] + 1
                                else:
                                    incorrect_format = incorrect_format + ',' + list_to_string(row)
                        except:
                            print("Error line ".join(row) + " " + filepath)
                            continue

                image_location = replace_extension(filepath, 'png')
                graph_bar(image_location, benford_array)
                # Send to another page
                # return render_template("uploadSuccess.html",
                #                        name=f.filename,
                #                        array=benford_array,
                #                        image=image_location.split('/')[3],
                #                        errors=incorrect_format)
                redirected = redirect(
                    url_for('index',
                            name=f.filename,
                            array=benford_array,
                            image=image_location.split('/')[3],
                            errors=incorrect_format),
                    code=302)
                return redirected
            else:
                return render_template('error.html',
                                       userFriendlyErrorMessage="No file uploaded or file not supported. Upload file types " + supported_file_extensions())
        finally:
            f.close()


@benfordLaw_page.route('/loadImage/<image>', methods=['GET'])
def download(image):
    return send_from_directory(UPLOAD_FOLDER, image)


def allowed_file_type(name):
    return '.' in name and \
        name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def randomize_file_name(name):
    return name.split(".")[0] + "_" + tempfile.NamedTemporaryFile().name.removeprefix("/tmp/") + "." + name.split(".")[1]


def replace_extension(name, extension):
    split_name = name.split('.')
    return split_name[0] + "." + extension


def supported_file_extensions():
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in ALLOWED_EXTENSIONS:
        str1 += ele + ", "

    # return string
    str1 = str1.removesuffix(",")
    return str1


def list_to_string(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

    # return string
    return str1


def graph_bar(s, benford_array):
    # Create dataset
    bars = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
    x_pos = np.arange(len(bars))

    # Create bars
    plt.bar(x_pos, benford_array)

    # Create names on the x-axis
    plt.xticks(x_pos, bars)

    # Save image
    plt.savefig(s)
    plt.close()

