import os
import pandas as pd

from sqlalchemy import create_engine, Column, Integer, SmallInteger, JSON
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"postgresql://postgres:postgres@localhost:5432/{DB_NAME}")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Entreprise(Base):
    """Les données concernant une entreprise (identifieé par son SIREN)"""

    __tablename__ = "siren_info"
    __table_args__ = {"schema": "rne"}
    siren = Column(Integer, primary_key=True)
    annee = Column(SmallInteger)
    result = Column(JSON)

entreprises = session.query(Entreprise).limit(1)

data = []
for e in entreprises:
    data_obj = {
        "siren": e.result["siren"][0],
        "dateCreation": e.result["formality"]["content"]["natureCreation"]["dateCreation"][0],
        "societeEtrangere": e.result["formality"]["content"]["natureCreation"]["societeEtrangere"][0],
        "formeJuridique": e.result["formality"]["content"]["natureCreation"]["formeJuridique"][0],
        "etablieEnFrance": e.result["formality"]["content"]["natureCreation"]["etablieEnFrance"][0],
        "commune": e.result["formality"]["content"]["personneMorale"]["adresseEntreprise"]["adresse"]["commune"][0],
        "codePostal": e.result["formality"]["content"]["personneMorale"]["adresseEntreprise"]["adresse"]["codePostal"][0],
    }

    pouvoirs = e.result["formality"]["content"]["personneMorale"]["composition"]["pouvoirs"]

    for i, p in enumerate(pouvoirs, 1):
        data_obj[f"pouvoir_{i}_libelleRoleEntreprise"] = p["libelleRoleEntreprise"][0]
        if "individu" in p:
            data_obj[f"pouvoir_{i}_nom"] = p["individu"]["descriptionPersonne"]["nom"][0]
            data_obj[f"pouvoir_{i}_prenoms"] = p["individu"]["descriptionPersonne"]["prenoms"][0][0]
            # data_obj[f"pouvoir_{i}_nationalite"] = p["individu"]["descriptionPersonne"]["nationalite"][0]

    data.append(data_obj)
    print(data)
