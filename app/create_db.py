#!/usr/bin/env python

import os
from app.models import *
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from sqlalchemy import create_engine
import pandas as pd
from app.config import Config

db = SQLAlchemy()

# Run this script to create app.db with the scivocab words in it.

def create_word_tables():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
    basedir = os.path.abspath(os.path.dirname(__file__))
    df = pd.read_csv(f"{basedir}/static/scivocab/sv_bv1_input.csv")
    current_app = create_app()
    current_app.config.from_object(Config)
    current_app.app_context().push()
    db.drop_all()
    db.create_all()
    for row in df.itertuples():
        word = Word(
            id=row.target, breadth_id=row.breadth_id, strand=Strand(id = row.strand)
        )
        db.session.merge(word)
        breadth_task_image = BreadthTaskImage(
            target=row.target,
            filename=row.file,
            image_type=BreadthTaskImageType(id = row.img_type),
            position = int(row.file.split("_")[2][1])
        )
        db.session.merge(breadth_task_image)
    db.session.commit()


if __name__ == "__main__":
    create_word_tables()
