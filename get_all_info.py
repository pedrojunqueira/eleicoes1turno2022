import json
import requests
from pathlib import Path

BASE_URL = "https://divulgacandcontas.tse.jus.br/divulga/rest/v1/candidatura/buscar/2022/{state}/2040602022/candidato/{candidate_id}"

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

payload={}
headers = {
  'authority': 'divulgacandcontas.tse.jus.br',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8,pt-BR;q=0.7,pt;q=0.6',
  'cookie': '__utma=260825096.221692522.1664858718.1664858718.1665092300.2; __utmz=260825096.1665092300.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _d8a23=308a378b82e71487; TS01efa917=0103a0ceaeb39dac43d3498c7c06bd77da1d161ed236c2e33d7872f08a1b3137bb75ef270a00f3f7b76960d21afe3474b6b8481cd0671d326cca3e86e2c7f7c7ed97b05494',
  'referer': 'https://divulgacandcontas.tse.jus.br/',
  'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
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

for role in get_roles:
	for uf in states_uf:
		with open(BASE_PATH/"data"/ role /f"{uf}_{role}.json", "r+") as fp:
			state_data = json.load(fp)
			candidates = state_data["candidatos"]
			for candidate in candidates:
				try:
					candidate_id = candidate["id"]
					role_code = roles_codes["deputado_federal"]
					name = candidate["nomeUrna"]
					print(f"fetching {name} id: {candidate_id} {uf}")
					api_url = BASE_URL.format(state=uf,candidate_id=candidate_id)
					file_name = f"{uf}_{role}_{candidate_id}_info.json"
					response = requests.get(api_url, headers=headers)
					with open(f"./data/info/{file_name}", "w+") as fp:
						json.dump(response.json(), fp)
				except Exception as e:
					print(e)
            



