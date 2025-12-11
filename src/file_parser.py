from dotenv import load_dotenv
import os

load_dotenv()

# Caminho dos arquivos utilizados pelo programa
ARQUIVO_PROPERTIES = os.getenv('PROPERTIES_FILEPATH')


# Codificação dos documentos da iCode
ENCODING_PROPERTIES = "latin-1"
ENCODING_XHTML = "utf-8"

# Palavras a serem ignoradas nas propriedades

generics = {}

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
