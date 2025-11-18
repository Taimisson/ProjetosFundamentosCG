"""
Caso de uso para aplicar filtros em imagens.
"""
from domain.entities.image import Image
from domain.interfaces.image_processor import ImageProcessorInterface
from domain.interfaces.image_repository import ImageRepositoryInterface


class ApplyFilterUseCase:
    """Caso de uso para aplicar filtros em imagens."""
    
    def __init__(self, image_repository: ImageRepositoryInterface):
        """
        Inicializa o caso de uso.
        
        Args:
            image_repository: Repositório para carregar/salvar imagens
        """
        self.image_repository = image_repository
    
    def execute(
        self, 
        input_path: str, 
        processor: ImageProcessorInterface,
        output_path: str = None
    ) -> Image:
        """
        Executa o caso de uso de aplicar filtro.
        
        Args:
            input_path: Caminho da imagem de entrada
            processor: Processador de imagem a ser aplicado
            output_path: Caminho opcional para salvar o resultado
            
        Returns:
            Imagem processada
        """
        # Carrega a imagem
        image = self.image_repository.load(input_path)
        
        # Aplica o processador
        processed_image = processor.process(image)
        
        # Salva se caminho foi fornecido
        if output_path:
            self.image_repository.save(processed_image, output_path)
        
        return processed_image
