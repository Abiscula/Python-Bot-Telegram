import requests

class BuscaCEP:
    def __init__(self, cep):
        self.cep = self.treat_input(cep)
        self.unicode = '\n\n' + ('\U00002796' * 20) + '\n\n '
        
    def treat_input(self, cep):
        if type(cep) == str:
            return cep.strip().replace('-', '')
        
    def validate_zip_code(self):
        if len(self.cep) != 8:
            return f'{self.unicode}     Quantidade de digitos inválida. O CEP deve conter 8 caracteres! {self.unicode}'
        else:
            return f'{self.unicode}     Buscando... {self.unicode}'
    
    def via_cep_request(self):
        r = requests.get(f'https://viacep.com.br/ws/{self.cep}/json/')
        resp = r.json()
        if (r.status_code != 200) or ('erro' in resp):
            return f'{self.unicode}     {self.cep} CEP inválido {self.unicode}'
        else:
            return f""" {self.unicode}
            \U0001F539  CEP: {resp['cep']}\n
            \U0001F539  Rua: {resp['logradouro']}\n
            \U0001F539  Bairro: {resp['bairro']}\n
            \U0001F539  Cidade: {resp['localidade']}\n
            \U0001F539  Estado: {resp['uf']}
{self.unicode}"""
            
    