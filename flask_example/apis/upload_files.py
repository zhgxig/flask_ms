from flask import Blueprint, request, jsonify, abort, render_template, send_file
from flask_example.db.model import PasteFile, db

upload_files_bp = Blueprint("upload_files", __name__)


@upload_files_bp.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        upload_file = request.files["file"]
        w = request.form.get("w")
        h = request.form.get("h")
        if not upload_file:
            return abort(400)

        if w and h:
            paste_file = PasteFile.rsize(upload_file, w, h)
        else:
            paste_file = PasteFile.create_by_upload_file(upload_file)
        db.session.add(paste_file)
        db.session.commit()

        return jsonify({
            "url_d": paste_file.url_d,
            "url_i": paste_file.url_i,
            "url_s": paste_file.url_s,
            "url_p": paste_file.url_p,
            "file_name": paste_file.file_name,
            "size": humanize_bytes(paste_file.size),
            "time": str(paste_file.upload_time),
            "mime_type": paste_file.mime_type,
            "quoteurl": paste_file.quotrurl
        })

    return render_template("index.html", **locals())


@upload_files_bp.route("/r/<img_hash>")
def rsize(img_hash):
    w = request.args.get("w")
    h = request.args.get("h")
    old_paste = PasteFile.get_by_file_hash(img_hash)
    new_paste = PasteFile.rsize(old_paste, w, h)
    return new_paste.url_i


@upload_files_bp.route("/d/<file_hash>", methods=["GET", "POST"])
def download(file_hash):
    ONE_MONTH = 60 * 60 * 24 * 30

    paste_file = PasteFile.get_by_file_hash(file_hash)
    return send_file(
        open(paste_file.path, "rb"),
        mimetype="application/octet-stream",
        cache_timeout=ONE_MONTH,
        as_attachment=True,
        attachment_filename=paste_file.file_name.encode("utf-8")

    )


@upload_files_bp.route("/p/<file_hash>")
def preview(file_hash):
    paste_file = PasteFile.get_by_file_hash(file_hash)
    return render_template("success.html", p=paste_file)


@upload_files_bp.route("/s/<symlink>")
def s(symlink):
    paste_file = PasteFile.get