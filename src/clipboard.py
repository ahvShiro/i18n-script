import os
from dotenv import load_dotenv
import time
import pyperclip
from formatter import *
import keyboard

load_dotenv()

BUNDLE_VAR = os.getenv('BUNDLE_VAR', 'msg')

def main():
    print("> Pressione Ctrl + C para sair")
    print("> Copie a string a ser traduzida e pressione enter para colar .properties na clipboard: ")
    dict_strings = {}
    

    while True:
        
        if (keyboard.is_pressed("ctrl+c")):
            time.sleep(0.5)
            print("="*50)
            message = pyperclip.paste()
    
            dict_strings = get_property_dict(message, bundle_var = BUNDLE_VAR, is_controller_message = REFERENCE_VALUE.endswith("excecao"))
                    
                # info = {
                #     'message': "",          # A mensagem sem alterações
                #     'property_name': "",    # O nome da propriedade
                #     'string_property': "",  # A string que vai ser passada no arquivo .properties
                #     'string_on_file': "",   # A string que vai ser colada no arquivo .xhtml ou .java
                # }
                
            print("> Texto copiado, cole no .properties")
            pyperclip.copy(dict_strings['string_property'])
            print(dict_strings['string_property'])
            
        if (keyboard.is_pressed("ctrl+v")):
            time.sleep(0.5)
            print("="*50)

            if "excecao" in reference_value:
                print("> Texto copiado, cole no controlador")
                pyperclip.copy(dict_strings['property_name'])

                print(dict_strings['property_name'])

            else:
                print("> Texto copiado, cole no .xhtml")
                pyperclip.copy(dict_strings['string_on_file'])

                print(dict_strings['string_on_file'])
                
            dict_strings = {key: "" for key in dict_strings}
            

def monitor():
    print("--- Monitor de Clipboard Ativo ---")
    print("> Copie qualquer texto e eu gerarei o .properties automaticamente.")
    print("> Pressione Ctrl + C para sair.\n")
    print("> Copie um texto e aperte ENTER para iniciar o script.")
    
    input()

    dict_with_formatted_data = {}
    
    message = pyperclip.paste()
    
    dict_with_formatted_data = get_property_dict(message, bundle_var = BUNDLE_VAR, is_controller_message = REFERENCE_VALUE.endswith("excecao"))
    
    print(dict_with_formatted_data)
        
        # # teste.ola.mundo=Olá mundo
        # pyperclip.copy(dict_with_formatted_data['string_property'])

        # if keyboard.is_pressed("ctrl+v"):
        #     pyperclip.copy(dict_with_formatted_data['string_on_file'])
        #     time.sleep(1)
        
        # dict_with_formatted_data = {key: "" for key in dict_with_formatted_data}



if __name__ == "__main__":
    main()