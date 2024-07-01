import os
import shutil

def organize_files(folder_path):
    # Verifica se o caminho é um diretório válido
    if not os.path.isdir(folder_path):
        print(f'O caminho {folder_path} não é um diretório válido.')
        return
    
    # Percorre todos os arquivos na pasta
    for filename in os.listdir(folder_path):
        if filename.endswith('.ic10'):
            # Cria o caminho completo para o arquivo
            file_path = os.path.join(folder_path, filename)
            
            # Cria o nome da subpasta (remove a extensão .ic10)
            folder_name = os.path.splitext(filename)[0]
            
            # Cria o caminho completo para a nova subpasta
            new_folder_path = os.path.join(folder_path, folder_name)
            
            # Cria a subpasta se ela ainda não existir
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
            
            # Move o arquivo para dentro da nova subpasta
            shutil.move(file_path, os.path.join(new_folder_path, filename))
            
            print(f'Arquivo {filename} movido para {new_folder_path}')

# Exemplo de uso:
folder_to_process = './scripts'
organize_files(folder_to_process)
