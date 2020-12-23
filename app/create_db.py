import os
from app.models import Concept, BreadthTaskImage
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from sqlalchemy import create_engine
import pandas as pd
from app.config import Config

db = SQLAlchemy()

# Run this script to create app.db with the scivocab words in it.


def create_or_update_tables():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=False)
    basedir = os.path.abspath(os.path.dirname(__file__))
    df = pd.read_csv(f"{basedir}/static/scivocab/sv_bv1_input.csv")
    current_app = create_app()
    current_app.config.from_object(Config)
    current_app.app_context().push()
    for row in df.itertuples():
        concept = Concept(
            id=row.target, breadth_task_id=row.task_id, strand=str(row.strand)
        )
        db.session.merge(concept)
        db.session.commit()
        breadth_task_image = BreadthTaskImage(
            target=row.target,
            filename=row.file,
            image_type=row.img_type,
        )
        db.session.add(breadth_task_image)
        db.session.commit()



if __name__ == "__main__":
    create_or_update_tables()
