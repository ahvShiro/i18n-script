import os
import re
import unidecode
from dotenv import load_dotenv
import pyperclip

load_dotenv()

# Valor que será concatenado no começo de cada propriedade. Ex.: "teste.*"
REFERENCE_VALUE = os.getenv('REFERENCE_VALUE')

# Caminho dos arquivos utilizados pelo programa
ARQUIVO_PROPERTIES = os.getenv('PROPERTIES_FILEPATH')

# Quantas palavras o programa selecionará no o começo ou final da propriedade aparada
# Ex.: Se start = 3 e end = 2, "Atenção. Não serão adicionados horários repetidos para 
# o mesmo dia na lista!" resulta em "atencao.nao.serao.dia.lista"
PROPERTY_CROP_QUANTITY_WORDS_START = int(os.getenv('PROPERTY_CROP_QUANTITY_WORDS_START'))
PROPERTY_CROP_QUANTITY_WORDS_END = int(os.getenv('PROPERTY_CROP_QUANTITY_WORDS_END'))

# Codificação dos documentos da iCode
ENCODING_PROPERTIES = "latin-1"
ENCODING_XHTML = "utf-8"

# Palavras a serem ignoradas nas propriedades
STOP_WORDS = {'de',  'a',  'o',  'que',  'e',  'do',  'da',  'em',  'um',  'para',  'é',  'com',  'não',  'uma',  'os',  'no',  'se',  'na',  'por',  'mais',  'as',  'dos',  'como',  'mas',  'foi',  'ao',  'ele',  'das',  'tem',  'à',  'seu',  'sua',  'ou',  'ser',  'quando',  'muito',  'há',  'nos',  'já',  'está',  'eu',  'também',  'só',  'pelo',  'pela',  'até',  'isso',  'ela',  'entre',  'era',  'depois',  'sem',  'mesmo',  'aos',  'ter',  'seus',  'quem',  'nas',  'me',  'esse',  'eles',  'estão',  'você',  'tinha',  'foram',  'essa',  'num',  'nem',  'suas',  'meu',  'às',  'minha',  'têm',  'numa',  'pelos',  'elas',  'havia',  'seja',  'qual',  'será',  'nós',  'tenho',  'lhe',  'deles',  'essas',  'esses',  'pelas',  'este',  'fosse',  'dele',  'tu',  'te',  'vocês',  'vos',  'lhes',  'meus',  'minhas',  'teu',  'tua',  'teus',  'tuas',  'nosso',  'nossa',  'nossos',  'nossas',  'dela',  'delas',  'esta',  'estes',  'estas',  'aquele',  'aquela',  'aqueles',  'aquelas',  'isto',  'aquilo',  'estou',  'está',  'estamos',  'estão',  'estive',  'esteve',  'estivemos',  'estiveram',
              'estava',  'estávamos',  'estavam',  'estivera',  'estivéramos',  'esteja',  'estejamos',  'estejam',  'estivesse',  'estivéssemos',  'estivessem',  'estiver',  'estivermos',  'estiverem',  'hei',  'há',  'havemos',  'hão',  'houve',  'houvemos',  'houveram',  'houvera',  'houvéramos',  'haja',  'hajamos',  'hajam',  'houvesse',  'houvéssemos',  'houvessem',  'houver',  'houvermos',  'houverem',  'houverei',  'houverá',  'houveremos',  'houverão',  'houveria',  'houveríamos',  'houveriam',  'sou',  'somos',  'são',  'era',  'éramos',  'eram',  'fui',  'foi',  'fomos',  'foram',  'fora',  'fôramos',  'seja',  'sejamos',  'sejam',  'fosse',  'fôssemos',  'fossem',  'for',  'formos',  'forem',  'serei',  'será',  'seremos',  'serão',  'seria',  'seríamos',  'seriam',  'tenho',  'tem',  'temos',  'tém',  'tinha',  'tínhamos',  'tinham',  'tive',  'teve',  'tivemos',  'tiveram',  'tivera',  'tivéramos',  'tenha',  'tenhamos',  'tenham',  'tivesse',  'tivéssemos',  'tivessem',  'tiver',  'tivermos',  'tiverem',  'terei',  'terá',  'teremos',  'terão',  'teria',  'teríamos',  'teriam'}

generics = {}
reference_value = REFERENCE_VALUE


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

def crop_word_list(word_list: list[str], qt_start: int, qt_end: int) -> list[str]:
    return word_list[:qt_start] + word_list[qt_end * -1:]


def get_property_name(dirty_name: str) -> list[str]:
    list_words = unidecode.unidecode(dirty_name.strip().lower())
    list_words = re.sub(r'[^A-Za-z0-9\s]+', '', list_words)
    list_words = list_words.split()
    
    # remove stopwords
    result_list = [word for word in list_words if word not in STOP_WORDS]
    
    if len(list_words) > 6:
        result_list = crop_word_list(result_list, PROPERTY_CROP_QUANTITY_WORDS_START, PROPERTY_CROP_QUANTITY_WORDS_END)
    
    return result_list
    

def format_property_name(listed_name: list[str]) -> str:

    output_name = ""
    
    # Se tiver valor de referencia, concatena no começo
    if reference_value != "":
        output_name += reference_value
        output_name += "."

    # Caso seja requiredMessage
    if "obrigatorio" in listed_name:
        joined_fieldname = ".".join(listed_name[1:-1])
        return output_name + joined_fieldname + ".requiredMessage"
         
    
    # Caso não seja nenhum caso acima, concatena tudo à output_name
    for word in listed_name:
        output_name += word
        
        if (word != listed_name[-1]):
            output_name += "."

    return output_name

get_reference_value = ()
def main():
    print("> Pressione Ctrl + C para sair")
    
    while True:
        
        print("> Copie a string a ser traduzida e pressione enter para colar .properties na clipboard: ")
        input()
        
        copy = pyperclip.paste()
        
        formatted_property_name = get_property_name(copy)
        property_rotulo=  format_property_name(formatted_property_name) + "=" + copy + "\n"
        property_xhtml = "#{msg['" + format_property_name(formatted_property_name) + "']}"
        property_controller= format_property_name(formatted_property_name)
        
        print("> Texto copiado, cole no .properties")
        pyperclip.copy(property_rotulo)
        
        print(property_rotulo)
        
        print("> Pressione enter para colar a mensagem no clipboard: ")
        input()

        if "excecao" in reference_value:
            print("> Texto copiado, cole no controlador")
            pyperclip.copy(property_controller)

            print(property_controller)

        else:
            print("> Texto copiado, cole no .xhtml")
            pyperclip.copy(property_xhtml)

            print(property_xhtml)
        
        print("="*50)


if __name__ == "__main__":

    main()
