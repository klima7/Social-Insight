from frontend import create_app
import db
import uploads


app = create_app()


@app.cli.command(help="Clean database and remove uploaded files")
def clean():
    db.clean_db()
    uploads.remove_all_packs()
    print("Database cleaned and uploaded files removed")





