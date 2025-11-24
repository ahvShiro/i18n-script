import os
import re
import unidecode
from dotenv import load_dotenv

load_dotenv()


ARQUIVO_PROPERTIES = os.getenv('PROPERTIES_FILEPATH')
ENCODING_PROPERTIES = "latin-1"
ENCODING_XHTML = "utf-8"

STOP_WORDS = {'de',  'a',  'o',  'que',  'e',  'do',  'da',  'em',  'um',  'para',  'é',  'com',  'não',  'uma',  'os',  'no',  'se',  'na',  'por',  'mais',  'as',  'dos',  'como',  'mas',  'foi',  'ao',  'ele',  'das',  'tem',  'à',  'seu',  'sua',  'ou',  'ser',  'quando',  'muito',  'há',  'nos',  'já',  'está',  'eu',  'também',  'só',  'pelo',  'pela',  'até',  'isso',  'ela',  'entre',  'era',  'depois',  'sem',  'mesmo',  'aos',  'ter',  'seus',  'quem',  'nas',  'me',  'esse',  'eles',  'estão',  'você',  'tinha',  'foram',  'essa',  'num',  'nem',  'suas',  'meu',  'às',  'minha',  'têm',  'numa',  'pelos',  'elas',  'havia',  'seja',  'qual',  'será',  'nós',  'tenho',  'lhe',  'deles',  'essas',  'esses',  'pelas',  'este',  'fosse',  'dele',  'tu',  'te',  'vocês',  'vos',  'lhes',  'meus',  'minhas',  'teu',  'tua',  'teus',  'tuas',  'nosso',  'nossa',  'nossos',  'nossas',  'dela',  'delas',  'esta',  'estes',  'estas',  'aquele',  'aquela',  'aqueles',  'aquelas',  'isto',  'aquilo',  'estou',  'está',  'estamos',  'estão',  'estive',  'esteve',  'estivemos',  'estiveram',
              'estava',  'estávamos',  'estavam',  'estivera',  'estivéramos',  'esteja',  'estejamos',  'estejam',  'estivesse',  'estivéssemos',  'estivessem',  'estiver',  'estivermos',  'estiverem',  'hei',  'há',  'havemos',  'hão',  'houve',  'houvemos',  'houveram',  'houvera',  'houvéramos',  'haja',  'hajamos',  'hajam',  'houvesse',  'houvéssemos',  'houvessem',  'houver',  'houvermos',  'houverem',  'houverei',  'houverá',  'houveremos',  'houverão',  'houveria',  'houveríamos',  'houveriam',  'sou',  'somos',  'são',  'era',  'éramos',  'eram',  'fui',  'foi',  'fomos',  'foram',  'fora',  'fôramos',  'seja',  'sejamos',  'sejam',  'fosse',  'fôssemos',  'fossem',  'for',  'formos',  'forem',  'serei',  'será',  'seremos',  'serão',  'seria',  'seríamos',  'seriam',  'tenho',  'tem',  'temos',  'tém',  'tinha',  'tínhamos',  'tinham',  'tive',  'teve',  'tivemos',  'tiveram',  'tivera',  'tivéramos',  'tenha',  'tenhamos',  'tenham',  'tivesse',  'tivéssemos',  'tivessem',  'tiver',  'tivermos',  'tiverem',  'terei',  'terá',  'teremos',  'terão',  'teria',  'teríamos',  'teriam'}

generics = {}
reference_value = ""


def load_generics():
    with open(ARQUIVO_PROPERTIES, 'r', encoding=ENCODING_PROPERTIES) as file:

        for i in range(1600):

            line = file.readline().strip()

            if not line or line.startswith('#') or line.startswith("\n"):
                continue

            if '=' in line:
                key, value = line.split('=', 1)
                generics[key.strip()] = value.strip()

        print("Generics Loaded")


def get_property_name(dirty_name: str) -> list[str]:
    list_words = unidecode.unidecode(dirty_name.strip().lower())
    list_words = list_words.split()

    # remove stopwords
    result_list = [word for word in list_words if word not in STOP_WORDS]
    
    # TODO get first and last 2 words for final return
    
    return result_list
    

def format_property_name(listed_name: list[str] ,reference_value: str="") -> str:

    output_name = ""

    if reference_value != "":
        output_name += reference_value
        output_name += "."

    for word in listed_name:
        output_name += word
        if (word != listed_name[-1]):
            output_name += "."

    return output_name



def main():
    list = get_property_name("Gerar contas a pagar de fechamento de folha")
    
    print(format_property_name(list, "usercreate"))


if __name__ == "__main__":

    main()
