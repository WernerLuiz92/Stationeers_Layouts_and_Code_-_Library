import os
import shutil
import xml.etree.ElementTree as ET
import time

def process_folders(main_folder):
    # Verifica se o caminho é um diretório válido
    if not os.path.isdir(main_folder):
        print(f'O caminho {main_folder} não é um diretório válido.')
        return
    
    # Percorre todas as subpastas dentro da pasta principal
    for folder_name in os.listdir(main_folder):
        folder_path = os.path.join(main_folder, folder_name)
        
        # Verifica se é um diretório
        if not os.path.isdir(folder_path):
            continue
        
        # Lista todos os arquivos na pasta atual
        files = os.listdir(folder_path)
        
        # Verifica se há um único arquivo .ic10
        ic10_files = [file for file in files if file.endswith('.ic10')]
        if len(ic10_files) == 1:
            ic10_file = ic10_files[0]
            ic10_path = os.path.join(folder_path, ic10_file)
            
            # Cria o conteúdo para o arquivo instruction.xml
            xml_content = create_instruction_xml(folder_name, ic10_path)
            
            # Salva o conteúdo no arquivo instruction.xml
            xml_path = os.path.join(folder_path, 'instruction.xml')
            save_to_file(xml_content, xml_path)
            
            print(f'Criado arquivo instruction.xml para pasta {folder_name}')
        
        # Verifica se há um único arquivo instruction.xml
        xml_files = [file for file in files if file == 'instruction.xml']
        if len(xml_files) == 1:
            xml_path = os.path.join(folder_path, 'instruction.xml')
            ic10_file = folder_name + '.ic10'
            ic10_path = os.path.join(folder_path, ic10_file)
            
            # Carrega o conteúdo da tag <Instructions> do XML
            xml_instructions = load_instructions_from_xml(xml_path)
            
            # Salva o conteúdo no arquivo .ic10 se necessário
            save_to_file(xml_instructions, ic10_path)
            
            print(f'Criado arquivo .ic10 a partir de instruction.xml para pasta {folder_name}')
        
        # Verifica se ambos os arquivos existem
        if len(ic10_files) == 1 and len(xml_files) == 1:
            ic10_path = os.path.join(folder_path, ic10_files[0])
            xml_path = os.path.join(folder_path, xml_files[0])
            
            # Compara os conteúdos
            ic10_content = load_file_content(ic10_path)
            xml_instructions = load_instructions_from_xml(xml_path)
            
            if ic10_content.strip() != xml_instructions.strip():
                print(f'Conteúdo de {ic10_files[0]} difere de instruction.xml para pasta {folder_name}')
            else:
                print(f'Conteúdo de {ic10_files[0]} é igual ao de instruction.xml para pasta {folder_name}')

def create_instruction_xml(folder_name, ic10_path):
    # Obtém o conteúdo do arquivo .ic10
    ic10_content = load_file_content(ic10_path)
    
    # Cria o XML
    root = ET.Element('InstructionData')
    root.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    
    ET.SubElement(root, 'DateTime').text = str(int(time.time() * 1000000))
    ET.SubElement(root, 'GameVersion').text = '0.2.5025.22811'
    ET.SubElement(root, 'Title').text = folder_name
    ET.SubElement(root, 'Description').text = ''
    ET.SubElement(root, 'Author').text = 'D4RK GH0ST'
    ET.SubElement(root, 'WorkshopFileHandle').text = '0'
    instructions_elem = ET.SubElement(root, 'Instructions')
    instructions_elem.text = ic10_content
    
    xml_content = ET.tostring(root, encoding='utf-8', method='xml')
    return xml_content.decode('utf-8')

def load_instructions_from_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    instructions_elem = root.find('Instructions')
    if instructions_elem is not None:
        return instructions_elem.text.strip()
    return ''

def load_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def save_to_file(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Exemplo de uso:
main_folder = './scripts'
process_folders(main_folder)
