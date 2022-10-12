import json
from pathlib import Path
from collections import defaultdict

import pandas as pd

BASE_PATH = Path(".").resolve()

states = {
            "AC": "Acre",
            "AL": "Alagoas",
            "AP": "Amapá",
            "AM": "Amazonas",
            "BA": "Bahia",
            "CE": "Ceará",
            "DF": "Distrito Federal",
            "ES": "Espirito Santo",
            "GO": "Goiás",
            "MA": "Maranhão",
            "MS": "Mato Grosso do Sul",
            "MT": "Mato Grosso",
            "MG": "Minas Gerais",
            "PA": "Pará",
            "PB": "Paraíba",
            "PR": "Paraná",
            "PE": "Pernambuco",
            "PI": "Piauí",
            "RJ": "Rio de Janeiro",
            "RS": "Rio Grande do Sul",
            "RO": "Rondônia",
            "RR": "Roraima",
            "SC": "Santa Catarina",
            "SP": "São Paulo",
            "SE": "Sergipe",
            "TO": "Tocantins",
            }

roles_codes = { 'governador': 3, 
                'vice_governador': 4, 
                'senador': 5, 
                'deputado_federal': 6, 
                'deputado_estadual': 7, 
                'suplente_1': 9, 
                'suplente_2': 10}

# open role file for state

states_uf = [s for s in states.keys()]
get_roles = ["deputado_federal"]


total_asset = 0

df_data = defaultdict(list)

for role in get_roles:
    for uf in states_uf:
        total_uf = 0
        with open(BASE_PATH/"data"/ role /f"{uf}_{role}.json", "r+") as fp:
            state_data = json.load(fp)
        candidates = state_data["candidatos"]
        for candidate in candidates:
            candidate_id = candidate["id"]
            role_code = roles_codes["deputado_federal"]
            name = candidate["nomeUrna"]
            file_name = f"{uf}_{role}_{candidate_id}.json"
            file_p = Path(f"./data/funds/{file_name}")
            if file_p.exists:
                try:
                    with open(file_p, "r+") as fp:
                        candidate_info = json.load(fp)
                    consolidated = candidate_info.get("dadosConsolidados")
                    if consolidated:
                        df_data["all_received"].append(consolidated.get("totalRecebido",0))
                        df_data["party_contribution"].append(consolidated.get("graphVrReceitaFin",0))
                        df_data["other_contribution"].append(consolidated.get("graphVrReceitaFinOutros",0))
                        df_data["special_fund_contribution"].append(consolidated.get("graphVrReceitaFinFefc",0))
                        df_data["candidate_id"].append(candidate_id)
                except Exception as e:
                    print(e)


df = pd.DataFrame(df_data)

df.to_csv("./data/deputado_federal_funds.csv", index=False)

print(df.head())
print(df["special_fund_contribution"].sum())
print(df["party_contribution"].sum())
print(df["other_contribution"].sum())



