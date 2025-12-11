import os
from dotenv import load_dotenv
import time
import pyperclip
from formatter import *
import keyboard

load_dotenv()

BUNDLE_VAR = os.getenv('BUNDLE_VAR')

def monitor():
    print("--- Monitor de Clipboard Ativo ---")
    print("> Copie qualquer texto e eu gerarei o .properties automaticamente.")
    print("> Pressione Ctrl + C para sair.\n")
    print("> Copie um texto e aperte ENTER para iniciar o script.")
    input()
    
    last_text = ""

    try:
        next_paste_content = None
        while True:
            if next_paste_content is None:
                current_text = pyperclip.paste().strip()
                
                if current_text and current_text != last_text and "=" not in current_text and "#{" not in current_text:
                    
                    property_name = format_property_name(get_property_name(current_text))
                    string_in_property_file = f"{property_name}={current_text}\n"
                    
                    if "excecao" in property_name:
                        next_paste_content = property_name
                        tipo_destino = "CONTROLADOR"
                    else:
                        next_paste_content = f"#{{{BUNDLE_VAR}['{property_name}']}}"
                        tipo_destino = "XHTML"

                    pyperclip.copy(string_in_property_file)
                    last_text = string_in_property_file # Atualiza para não processar de novo

                    print(f"\n[1/2] Gerado .properties: {property_name}")
                    print(f"      -> Pode colar no arquivo .properties agora...")

            else:
                if keyboard.is_pressed('ctrl+v'):
                    
                    time.sleep(0.5) 
                    
                    pyperclip.copy(next_paste_content)
                    
                    print(f"[2/2] Detectado 'Colar'! Clipboard atualizado para {tipo_destino}.")
                    print(f"      -> Conteúdo: {next_paste_content}")
                    print("-" * 50)
                    
                    next_paste_content = None
                    
                    time.sleep(1)

            time.sleep(0.1) 

    except KeyboardInterrupt:
        print("\nEncerrando.")
            
if __name__ == "__main__":
    monitor()