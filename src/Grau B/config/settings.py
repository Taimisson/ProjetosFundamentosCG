# Configurações do Projeto

# Caminhos
IMAGE_INPUT_PATH = "assets/images/input"
IMAGE_OUTPUT_PATH = "assets/images/output"

# Formatos suportados
SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]

# Configurações de filtros
FILTER_CONFIGS = {
    "mean_3x3": {"kernel_size": (3, 3)},
    "mean_5x5": {"kernel_size": (5, 5)},
    "gaussian": {"kernel_size": (5, 5), "sigma": 1.0},
    "laplacian": {"kernel_size": 3},
    "sobel": {"kernel_size": 3}
}

# Configurações de elementos estruturantes
MORPHOLOGY_CONFIGS = {
    "kernel_size": (5, 5),
    "kernel_shape": "rect"  # rect, ellipse, cross
}

# Configurações de limiarização
THRESHOLD_CONFIGS = {
    "binary_threshold": 127,
    "adaptive_block_size": 11,
    "adaptive_c": 2
}
