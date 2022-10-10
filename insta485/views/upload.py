"""Upload functions."""
import uuid
import pathlib
import flask
import insta485


def file_upload():
    """Upload files."""
    # Unpack flask object
    fileobj = flask.request.files["file"]
    if not fileobj:
        flask.abort(400)
    filename = fileobj.filename
    # Compute base name (filename without directory).  We use a UUID to avoid
    # clashes with existing files, and ensure
    # that the name is compatible with the
    # filesystem.
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"
    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    return uuid_basename


@insta485.app.route('/uploads/<filename>', methods=['GET'])
def image_render(filename):
    """Render images."""
    if "logname" not in flask.session:
        flask.abort(403)
    return flask.send_from_directory(
            insta485.app.config["UPLOAD_FOLDER"], filename)
