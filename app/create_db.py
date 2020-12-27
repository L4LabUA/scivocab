#!/usr/bin/env python

"""The create_db script creates an SQLite3 database that contains the tables
and data required for the app."""

import os
import sys
from app.models import Word, Strand, BreadthTaskImage, BreadthTaskImageType
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
from sqlalchemy import create_engine
import pandas as pd
from app.config import Config
import click
from pathlib import Path


def create_word_tables():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
    basedir = os.path.abspath(os.path.dirname(__file__))
    df = pd.read_csv(f"{basedir}/static/scivocab/sv_bv1_input.csv")
    current_app = create_app()
    current_app.config.from_object(Config)
    current_app.app_context().push()
    db.init_app(current_app)
    db_filepath = current_app.config["SQLITE3_DB_PATH"]

    if Path(db_filepath).exists():
        # Warn the user about the consequences of running the script and ask
        # them 
        if not click.confirm(
            "This script will delete the existing database "
            f"({db_filepath}) and create a fresh one. "
            "Are you sure you want to continue?",
            default=False,
        ):
            print("Database creation canceled. Exiting now.")
            sys.exit(0)

    db.drop_all()
    db.create_all()
    for row in df.itertuples():
        word = Word(
            id=row.target,
            breadth_id=row.breadth_id,
            strand=Strand(id=row.strand),
        )
        db.session.merge(word)
        breadth_task_image = BreadthTaskImage(
            target=row.target,
            filename=row.file,
            image_type=BreadthTaskImageType(id=row.img_type),
            position=int(row.file.split("_")[2][1]),
        )
        db.session.merge(breadth_task_image)
    db.session.commit()


if __name__ == "__main__":
    create_word_tables()
