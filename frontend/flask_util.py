import flask


def display_errors_with_flash(form):
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            flask.flash(err, 'error')


