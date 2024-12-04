from pathlib import Path
from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode

def configure_converter(use_accurate_table_mode: bool = False) -> DocumentConverter:
    """
    Configura el convertidor de Docling con opciones personalizadas.

    Args:
        use_accurate_table_mode (bool): Si se debe usar el modo TableFormer más preciso.

    Returns:
        DocumentConverter: Instancia configurada del convertidor.
    """
    pipeline_options = PdfPipelineOptions(do_table_structure = True)
    
    if use_accurate_table_mode:
        pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
    
    return DocumentConverter()

def pdf_to_markdown(pdf_path: str, max_pages: int = None, max_file_size: int = None) -> str:
    """
    Convierte un archivo PDF a Markdown.

    Args:
        pdf_path (str): Ruta al archivo PDF.
        max_pages (int, optional): Número máximo de páginas a procesar.
        max_file_size (int, optional): Tamaño máximo del archivo en bytes.

    Returns:
        str: Contenido del PDF en formato Markdown.
    """
    try:
        # Configura el convertidor
        converter = configure_converter(use_accurate_table_mode=True)
        
        # Procesa el PDF
        result = converter.convert(pdf_path, max_num_pages = max_pages, max_file_size = max_file_size)
        return result.document.export_to_markdown()
    
    except AttributeError as e:
        raise RuntimeError(f"Error al convertir el PDF: {e}")
    
    except Exception as e:
        raise RuntimeError(f"Se produjo un error inesperado: {e}")

if __name__ == "__main__":

    pdf_file_path = "data/pdf/Sample.pdf"
    
    if not Path(pdf_file_path).is_file():
        print(f"El archivo '{pdf_file_path}' no existe. Por favor, verifica la ruta.")
    else:
        try:
            markdown_content = pdf_to_markdown(pdf_file_path, max_pages = 100, max_file_size = 20 * 1024 * 1024)
            output_file = "data/markdown/markdown.md"
            
            with open(output_file, "w", encoding="utf-8") as md_file:
                md_file.write(markdown_content)
            print(f"El contenido del PDF se guardó en '{output_file}'.")

        except RuntimeError as error:
            print(error)
