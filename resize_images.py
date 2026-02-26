#!/usr/bin/env python3
"""
Script para redimensionar imágenes de la carpeta 'imagenes/'
Las imágenes se ajustarán a 390x260px manteniendo su proporción
y se guardarán optimizadas en la misma carpeta.

Uso:
  python3 resize_images.py
"""

import os
from PIL import Image
import sys

# Tamaño objetivo que coincide con las tarjetas del sitio
TARGET_WIDTH = 390
TARGET_HEIGHT = 260

# Carpeta donde están las imágenes
IMAGES_DIR = "imagenes"

def resize_and_optimize(image_path):
    """Redimensiona una imagen para que encaje perfectamente en las tarjetas."""
    try:
        img = Image.open(image_path)
        
        # Mostrar info original
        original_size = img.size
        print(f"  Original: {original_size[0]}x{original_size[1]}px")
        
        # Calcular la proporción (aspect ratio)
        aspect_ratio = img.width / img.height
        target_ratio = TARGET_WIDTH / TARGET_HEIGHT
        
        # Redimensionar manteniendo proporción
        if aspect_ratio > target_ratio:
            # Imagen más ancha: limitar por alto
            new_height = TARGET_HEIGHT
            new_width = int(new_height * aspect_ratio)
        else:
            # Imagen más alta: limitar por ancho
            new_width = TARGET_WIDTH
            new_height = int(new_width / aspect_ratio)
        
        # Redimensionar
        img_resized = img.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )
        
        # Crear imagen final con fondo del sitio (crema)
        background = Image.new(
            'RGB',
            (TARGET_WIDTH, TARGET_HEIGHT),
            color=(245, 237, 224)  # --cream color
        )
        
        # Centrar la imagen redimensionada en el fondo
        offset_x = (TARGET_WIDTH - new_width) // 2
        offset_y = (TARGET_HEIGHT - new_height) // 2
        background.paste(img_resized, (offset_x, offset_y))
        
        # Guardar optimizada (JPEG con buena calidad)
        background.save(
            image_path,
            'JPEG',
            quality=85,
            optimize=True
        )
        
        file_size = os.path.getsize(image_path) / 1024  # KB
        print(f"  ✅ Redimensionada a: {TARGET_WIDTH}x{TARGET_HEIGHT}px ({file_size:.1f} KB)")
        
        return True
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def main():
    if not os.path.exists(IMAGES_DIR):
        print(f"❌ La carpeta '{IMAGES_DIR}' no existe.")
        print("   Crea la carpeta y coloca tus imágenes allí.")
        sys.exit(1)
    
    # Extensiones de imagen a procesar
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    # Buscar imágenes
    images = [
        f for f in os.listdir(IMAGES_DIR)
        if os.path.splitext(f)[1].lower() in image_extensions
    ]
    
    if not images:
        print(f"⚠️  No hay imágenes en la carpeta '{IMAGES_DIR}'")
        sys.exit(0)
    
    print(f"\n🖼️  Redimensionando {len(images)} imagen(es)...\n")
    
    success_count = 0
    for filename in images:
        filepath = os.path.join(IMAGES_DIR, filename)
        print(f"→ {filename}")
        if resize_and_optimize(filepath):
            success_count += 1
    
    print(f"\n✅ Completado: {success_count}/{len(images)} imágenes redimensionadas")
    print(f"   Tamaño de todas las imágenes: {TARGET_WIDTH}x{TARGET_HEIGHT}px")
    print("   Las fotos ahora encajan perfectamente en las tarjetas del menú.\n")

if __name__ == "__main__":
    main()
