import flask
import os
import zipfile


def display_errors_with_flash(form):
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            flask.flash(err, 'error')


def zipdir(src, dest, include_root=False):
    zipf = zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED)

    dir_offset = '..' if include_root else '.'

    for root, dirs, files in os.walk(src):
        for file in files:
            write_src = os.path.join(root, file)
            write_dst = os.path.relpath(os.path.join(root, file), os.path.join(src, dir_offset))
            zipf.write(write_src, write_dst)

    zipf.close()

