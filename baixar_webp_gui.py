import os
import requests
from PIL import Image
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox

def save_webpage_as_webp(url, output_path):
    """
    Baixa a página web especificada pelo URL e salva como uma imagem WebP.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se houve algum erro na requisição

        soup = BeautifulSoup(response.text, 'html.parser')

        # Convertendo o conteúdo da página para uma imagem PNG
        with open('temp_page.png', 'wb') as f:
            f.write(response.content)

        # Convertendo PNG para WebP
        with Image.open('temp_page.png') as img:
            img.save(output_path, 'webp')
        print(f"Página salva como: {output_path}")

    except Exception as e:
        print(f"Erro ao processar a URL {url}: {e}")

def extract_links_from_text_files(directory):
    """
    Extrai todos os links de arquivos de texto no diretório especificado.
    """
    links = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                links.extend(file.read().splitlines())
    return links

def main(text_files_directory, output_directory):
    # Criando o diretório de saída, se não existir
    os.makedirs(output_directory, exist_ok=True)

    # Extraindo links dos arquivos de texto
    links = extract_links_from_text_files(text_files_directory)
    
    # Baixando cada página e salvando como WebP
    for i, link in enumerate(links):
        output_path = os.path.join(output_directory, f'page_{i + 1}.webp')
        save_webpage_as_webp(link, output_path)

    print("Download e conversão concluídos!")

def select_text_files_directory():
    directory = filedialog.askdirectory()
    text_files_directory_entry.delete(0, tk.END)
    text_files_directory_entry.insert(0, directory)

def select_output_directory():
    directory = filedialog.askdirectory()
    output_directory_entry.delete(0, tk.END)
    output_directory_entry.insert(0, directory)

def start_conversion():
    text_files_directory = text_files_directory_entry.get()
    output_directory = output_directory_entry.get()

    if not text_files_directory or not output_directory:
        messagebox.showerror("Erro", "Por favor, selecione ambos os diretórios.")
        return

    main(text_files_directory, output_directory)
    messagebox.showinfo("Concluído", "Download e conversão concluídos!")

# Interface Gráfica
root = tk.Tk()
root.title("Web Page to WebP Converter")

tk.Label(root, text="Diretório dos Arquivos de Texto:").grid(row=0, column=0, padx=10, pady=5)
text_files_directory_entry = tk.Entry(root, width=50)
text_files_directory_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Selecionar", command=select_text_files_directory).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Diretório de Saída:").grid(row=1, column=0, padx=10, pady=5)
output_directory_entry = tk.Entry(root, width=50)
output_directory_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Selecionar", command=select_output_directory).grid(row=1, column=2, padx=10, pady=5)

tk.Button(root, text="Iniciar Conversão", command=start_conversion).grid(row=2, column=0, columnspan=3, pady=20)

root.mainloop()
