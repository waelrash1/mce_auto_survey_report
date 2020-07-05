import os

from flask import Flask, request, abort, jsonify, send_from_directory

UPLOAD_DIRECTORY = "./output/pdfs/"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

api = Flask(__name__)


@api.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@api.route('/download/<filename>')
def download_file(filename):
    PDF_DIRECTORY = "./output/pdfs"
    suffix = ".pdf"
    print(filename)
    if filename.lower().endswith(".pdf"):
        path = os.path.join(PDF_DIRECTORY, filename)
    else:
        path = os.path.join(PDF_DIRECTORY, filename + suffix)
        filename = os.path.join(filename + suffix)
    print(filename)
    try:
        return send_from_directory(UPLOAD_DIRECTORY, filename, as_attachment=True)
    except:
        return path + " REPORT IS NOT READY YET...IT TAKES A WHILE TO BE GENERATED"


@api.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@api.route("/files/<filename>", methods=["GET"])
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201


if __name__ == "__main__":
    ##  lsof -ti:8002 | xargs kill
    api.run(port=8000)
