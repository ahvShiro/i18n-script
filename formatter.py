import os
import unidecode
import re
from dotenv import load_dotenv

load_dotenv()

# Valor que será concatenado no começo de cada propriedade. Ex.: "teste.*"
REFERENCE_VALUE = os.getenv('REFERENCE_VALUE')

# Quantas palavras o programa selecionará no o começo ou final da propriedade aparada
# Ex.: Se start = 3 e end = 2, "Atenção. Não serão adicionados horários repetidos para
# o mesmo dia na lista!" resulta em "atencao.nao.serao.dia.lista"
PROPERTY_CROP_QUANTITY_WORDS_START = int(os.getenv('PROPERTY_CROP_QUANTITY_WORDS_START'))
PROPERTY_CROP_QUANTITY_WORDS_END = int(os.getenv('PROPERTY_CROP_QUANTITY_WORDS_END'))

STOP_WORDS = {'de',  'a',  'o',  'que',  'e',  'do',  'da',  'em',  'um',  'para',  'é',  'com',  'não',  'uma',  'os',  'no',  'se',  'na',  'por',  'mais',  'as',  'dos',  'como',  'mas',  'foi',  'ao',  'ele',  'das',  'tem',  'à',  'seu',  'sua',  'ou',  'ser',  'quando',  'muito',  'há',  'nos',  'já',  'está',  'eu',  'também',  'só',  'pelo',  'pela',  'até',  'isso',  'ela',  'entre',  'era',  'depois',  'sem',  'mesmo',  'aos',  'ter',  'seus',  'quem',  'nas',  'me',  'esse',  'eles',  'estão',  'você',  'tinha',  'foram',  'essa',  'num',  'nem',  'suas',  'meu',  'às',  'minha',  'têm',  'numa',  'pelos',  'elas',  'havia',  'seja',  'qual',  'será',  'nós',  'tenho',  'lhe',  'deles',  'essas',  'esses',  'pelas',  'este',  'fosse',  'dele',  'tu',  'te',  'vocês',  'vos',  'lhes',  'meus',  'minhas',  'teu',  'tua',  'teus',  'tuas',  'nosso',  'nossa',  'nossos',  'nossas',  'dela',  'delas',  'esta',  'estes',  'estas',  'aquele',  'aquela',  'aqueles',  'aquelas',  'isto',  'aquilo',  'estou',  'está',  'estamos',  'estão',  'estive',  'esteve',  'estivemos',  'estiveram',
              'estava',  'estávamos',  'estavam',  'estivera',  'estivéramos',  'esteja',  'estejamos',  'estejam',  'estivesse',  'estivéssemos',  'estivessem',  'estiver',  'estivermos',  'estiverem',  'hei',  'há',  'havemos',  'hão',  'houve',  'houvemos',  'houveram',  'houvera',  'houvéramos',  'haja',  'hajamos',  'hajam',  'houvesse',  'houvéssemos',  'houvessem',  'houver',  'houvermos',  'houverem',  'houverei',  'houverá',  'houveremos',  'houverão',  'houveria',  'houveríamos',  'houveriam',  'sou',  'somos',  'são',  'era',  'éramos',  'eram',  'fui',  'foi',  'fomos',  'foram',  'fora',  'fôramos',  'seja',  'sejamos',  'sejam',  'fosse',  'fôssemos',  'fossem',  'for',  'formos',  'forem',  'serei',  'será',  'seremos',  'serão',  'seria',  'seríamos',  'seriam',  'tenho',  'tem',  'temos',  'tém',  'tinha',  'tínhamos',  'tinham',  'tive',  'teve',  'tivemos',  'tiveram',  'tivera',  'tivéramos',  'tenha',  'tenhamos',  'tenham',  'tivesse',  'tivéssemos',  'tivessem',  'tiver',  'tivermos',  'tiverem',  'terei',  'terá',  'teremos',  'terão',  'teria',  'teríamos',  'teriam'}

reference_value = REFERENCE_VALUE


def crop_word_list_start_end(word_list: list[str], qt_start: int, qt_end: int) -> list[str]:
    return word_list[:qt_start] + word_list[qt_end * -1:]


def crop_word_list_first_words(word_list: list[str], qt_start: int, qt_end: int) -> list[str]:
    return word_list[:qt_start + qt_end]


def get_property_name(dirty_name: str) -> list[str]:
    list_words = unidecode.unidecode(dirty_name.strip().lower())
    list_words = re.sub(r'[^A-Za-z0-9\s]+', '', list_words)
    list_words = list_words.split()

    # remove stopwords
    result_list = [word for word in list_words if word not in STOP_WORDS]

    if len(list_words) > 7:
        result_list = crop_word_list_start_end(
            result_list, PROPERTY_CROP_QUANTITY_WORDS_START, PROPERTY_CROP_QUANTITY_WORDS_END)

    return result_list


def format_property_name(listed_name: list[str]) -> str:

    output_name = ""

    # Se tiver valor de referencia, concatena no começo
    if reference_value != "":
        output_name += reference_value
        output_name += "."

    # Caso seja requiredMessage
    if (("obrigatorio" in listed_name) or ("necessario" in listed_name)) and reference_value != "excecao":
        joined_fieldname = ".".join(listed_name[1:-1])
        return output_name + joined_fieldname + ".requiredMessage"

    # Caso seja emptyMessage
    elif "nenhum" in listed_name and "encontrado" in listed_name:
        joined_fieldname = ".".join(listed_name[1:-1])
        return output_name + joined_fieldname + ".emptyMessage"

    # Caso não seja nenhum caso acima, concatena tudo à output_name
    for word in listed_name:
        output_name += word

        if (word != listed_name[-1]):
            output_name += "."

    return output_name
