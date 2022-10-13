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
            file_name = f"{uf}_{role}_{candidate_id}_info.json"
            file_p = Path(f"./data/info/{file_name}")
            if file_p.exists:
                try:
                    with open(f"./data/info/{file_name}", "r+") as fp:
                        candidate_info = json.load(fp)
                    df_data["candidate_id"].append(candidate_info["id"])
                    df_data["running_role"].append("deputado federal")
                    df_data["candidate_assets"].append(candidate_info["totalDeBens"])
                    df_data["name_ballot"].append(candidate_info["nomeUrna"])
                    df_data["number"].append(candidate_info["numero"])
                    df_data["full_name"].append(candidate_info["nomeCompleto"])
                    df_data["sex"].append(candidate_info["descricaoSexo"])
                    df_data["dob"].append(candidate_info["dataDeNascimento"])
                    df_data["marital_status"].append(candidate_info["descricaoEstadoCivil"])
                    df_data["race"].append(candidate_info["descricaoCorRaca"])
                    df_data["nationality"].append(candidate_info["nacionalidade"])
                    df_data["education"].append(candidate_info["grauInstrucao"])
                    df_data["occupation"].append(candidate_info["ocupacao"])
                    df_data["campaign_expenses1T"].append(candidate_info["gastoCampanha1T"])
                    df_data["birth_uf"].append(candidate_info["sgUfNascimento"])
                    df_data["birth_town"].append(candidate_info["nomeMunicipioNascimento"])
                    df_data["place_candidate"].append(candidate_info["localCandidatura"])
                    df_data["uf_candidate"].append(candidate_info["ufCandidatura"])
                    df_data["photo_url"].append(candidate_info["fotoUrl"])
                    df_data["election_outcome"].append(candidate_info["descricaoTotalizacao"])
                    df_data["coalition"].append(candidate_info["nomeColigacao"])
                    df_data["party_number"].append(candidate_info["partido"]["numero"])
                    df_data["party_code"].append(candidate_info["partido"]["sigla"])
                    df_data["party_name"].append(candidate_info["partido"]["nome"])
                    df_data["titulo_eleitor"].append(candidate_info["tituloEleitor"])
                    candidate_assets = candidate_info["totalDeBens"]
                    total_uf += candidate_assets
                except Exception as e:
                    print(e)
        print(f"Total for {uf} is {total_uf}")
        total_asset += total_uf
    print(f"total_asset = {total_asset}")

# 7_552_211_927.280001

df = pd.DataFrame(df_data)

df.to_csv("./data/deputado_federal_info.csv", index=False)



# get 2018 winners

df_data = defaultdict(list)

for role in get_roles:
    for uf in states_uf:
        total_uf = 0
        with open(BASE_PATH/"data"/ f"{role}_2018" /f"{uf}_{role}.json", "r+") as fp:
            state_data = json.load(fp)
        candidates = state_data["candidatos"]
        for candidate in candidates:
            candidate_id = candidate["id"]
            role_code = roles_codes["deputado_federal"]
            name = candidate["nomeUrna"]
            file_name = f"{uf}_{role}_{candidate_id}_info.json"
            file_p = Path(f"./data/info_2018_winners/{file_name}")
            election_outcome = candidate["descricaoTotalizacao"]
            if election_outcome in ["Eleito por m\u00e9dia","Eleito por QP"]:
                if file_p.exists:
                    try:
                        with open(file_p, "r+") as fp:
                            candidate_info = json.load(fp)
                        df_data["candidate_id"].append(candidate_info["id"])
                        df_data["running_role"].append("deputado federal")
                        df_data["candidate_assets"].append(candidate_info["totalDeBens"])
                        df_data["name_ballot"].append(candidate_info["nomeUrna"])
                        df_data["number"].append(candidate_info["numero"])
                        df_data["full_name"].append(candidate_info["nomeCompleto"])
                        df_data["sex"].append(candidate_info["descricaoSexo"])
                        df_data["dob"].append(candidate_info["dataDeNascimento"])
                        df_data["marital_status"].append(candidate_info["descricaoEstadoCivil"])
                        df_data["race"].append(candidate_info["descricaoCorRaca"])
                        df_data["nationality"].append(candidate_info["nacionalidade"])
                        df_data["education"].append(candidate_info["grauInstrucao"])
                        df_data["occupation"].append(candidate_info["ocupacao"])
                        df_data["campaign_expenses1T"].append(candidate_info["gastoCampanha1T"])
                        df_data["birth_uf"].append(candidate_info["sgUfNascimento"])
                        df_data["birth_town"].append(candidate_info["nomeMunicipioNascimento"])
                        df_data["place_candidate"].append(candidate_info["localCandidatura"])
                        df_data["uf_candidate"].append(candidate_info["ufCandidatura"])
                        df_data["photo_url"].append(candidate_info["fotoUrl"])
                        df_data["election_outcome"].append(candidate_info["descricaoTotalizacao"])
                        df_data["coalition"].append(candidate_info["nomeColigacao"])
                        df_data["party_number"].append(candidate_info["partido"]["numero"])
                        df_data["party_code"].append(candidate_info["partido"]["sigla"])
                        df_data["party_name"].append(candidate_info["partido"]["nome"])
                        df_data["titulo_eleitor"].append(candidate_info["tituloEleitor"])
                        candidate_assets = candidate_info["totalDeBens"]
                        total_uf += candidate_assets
                    except Exception as e:
                        print(e)


df = pd.DataFrame(df_data)

df.to_csv("./data/deputado_federal_info_2018.csv", index=False)

