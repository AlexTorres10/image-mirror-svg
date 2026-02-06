#!/usr/bin/env python3
"""
Image Mirror to SVG Converter
Programa para espelhar imagens horizontalmente e salvar como SVG
Para uso com ScanCut
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os
import base64
from io import BytesIO


class ImageMirrorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Espelhar Imagem para SVG - ScanCut")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        
        # Variáveis
        self.image_path = None
        self.original_image = None
        
        # Configurar interface
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Espelhar Imagem para ScanCut",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Instruções
        instructions = ttk.Label(
            main_frame,
            text="Selecione uma imagem para espelhar horizontalmente\ne converter para SVG",
            justify=tk.CENTER
        )
        instructions.pack(pady=(0, 20))
        
        # Botão selecionar imagem
        self.select_button = ttk.Button(
            main_frame,
            text="📁 Selecionar Imagem",
            command=self.select_image,
            width=30
        )
        self.select_button.pack(pady=10)
        
        # Label para mostrar arquivo selecionado
        self.file_label = ttk.Label(
            main_frame,
            text="Nenhum arquivo selecionado",
            foreground="gray",
            wraplength=450
        )
        self.file_label.pack(pady=10)
        
        # Frame para preview
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        self.preview_label = ttk.Label(preview_frame, text="")
        self.preview_label.pack()
        
        # Botão processar
        self.process_button = ttk.Button(
            main_frame,
            text="✨ Espelhar e Salvar como SVG",
            command=self.process_image,
            state=tk.DISABLED,
            width=30
        )
        self.process_button.pack(pady=10)
        
        # Status
        self.status_label = ttk.Label(
            main_frame,
            text="",
            foreground="blue"
        )
        self.status_label.pack(pady=5)
        
    def select_image(self):
        """Selecionar arquivo de imagem"""
        filetypes = (
            ('Imagens', '*.png *.jpg *.jpeg *.bmp *.gif'),
            ('Todos os arquivos', '*.*')
        )
        
        filename = filedialog.askopenfilename(
            title="Selecionar imagem",
            filetypes=filetypes
        )
        
        if filename:
            self.image_path = filename
            self.file_label.config(
                text=f"Arquivo: {os.path.basename(filename)}",
                foreground="black"
            )
            self.process_button.config(state=tk.NORMAL)
            self.status_label.config(text="")
            
            # Carregar e mostrar preview
            self.show_preview()
    
    def show_preview(self):
        """Mostrar preview da imagem original"""
        try:
            img = Image.open(self.image_path)
            self.original_image = img.copy()
            
            # Redimensionar para preview (máximo 200x200)
            img.thumbnail((200, 200), Image.Resampling.LANCZOS)
            
            # Converter para PhotoImage
            from PIL import ImageTk
            photo = ImageTk.PhotoImage(img)
            
            self.preview_label.config(image=photo)
            self.preview_label.image = photo  # Manter referência
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar imagem:\n{str(e)}")
    
    def process_image(self):
        """Processar imagem: espelhar e salvar como SVG"""
        if not self.image_path:
            return
        
        try:
            self.status_label.config(text="Processando...", foreground="blue")
            self.root.update()
            
            # Abrir e espelhar imagem
            img = Image.open(self.image_path)
            mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            
            # Converter para base64
            buffered = BytesIO()
            mirrored_img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Criar SVG
            width, height = mirrored_img.size
            svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}" 
     height="{height}" 
     viewBox="0 0 {width} {height}">
    <image 
        width="{width}" 
        height="{height}" 
        xlink:href="data:image/png;base64,{img_base64}"/>
</svg>'''
            
            # Gerar nome do arquivo de saída
            base_dir = os.path.dirname(self.image_path)
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]
            output_path = os.path.join(base_dir, f"{base_name}_espelhado.svg")
            
            # Se o arquivo já existe, adicionar número
            counter = 1
            while os.path.exists(output_path):
                output_path = os.path.join(base_dir, f"{base_name}_espelhado_{counter}.svg")
                counter += 1
            
            # Salvar SVG
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            # Sucesso
            self.status_label.config(
                text=f"✓ Salvo com sucesso!\n{os.path.basename(output_path)}",
                foreground="green"
            )
            
            messagebox.showinfo(
                "Sucesso!",
                f"Imagem espelhada salva como:\n\n{output_path}\n\n"
                f"O arquivo SVG está pronto para usar no ScanCut!"
            )
            
        except Exception as e:
            self.status_label.config(text="✗ Erro ao processar", foreground="red")
            messagebox.showerror("Erro", f"Erro ao processar imagem:\n{str(e)}")


def main():
    root = tk.Tk()
    app = ImageMirrorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()