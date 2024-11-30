import cv2
import os
import shutil
import time

# Caminhos das pastas
input_folder = 'imgGrande'
location_folder = 'localizacao'
output_folder = 'capturas'  # Pasta onde as imagens renomeadas serão salvas

# Assegura a criação das pastas
os.makedirs(input_folder, exist_ok=True)
os.makedirs(location_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Define o tamanho desejado para a imagem
new_width = 300
new_height = 170

# Função para renomear, redimensionar e mover imagens
def rename_and_move_images():
    # Obtém a lista de arquivos de localização e imagens
    location_files = sorted(os.listdir(location_folder))
    image_files = sorted(os.listdir(input_folder))

    for image_file in image_files:
        if image_file.lower().endswith((".jpg", ".jpeg", ".png")):
            if location_files:
                # Caminho do primeiro arquivo de localização disponível
                location_file = location_files[0]
                location_path = os.path.join(location_folder, location_file)

                # Verifica se o arquivo de localização existe antes de prosseguir
                if not os.path.exists(location_path):
                    print(f"Arquivo de localização não encontrado: {location_path}")
                    location_files.pop(0)  # Remove da lista, mas continua o loop
                    continue

                # Novo nome baseado no nome do arquivo de localização
                new_image_name = location_file.replace('.txt', '') + os.path.splitext(image_file)[1]

                # Caminhos de origem e destino para a imagem
                src_image_path = os.path.join(input_folder, image_file)
                dst_image_path = os.path.join(output_folder, new_image_name)

                # Carrega e redimensiona a imagem
                image = cv2.imread(src_image_path)
                if image is None:
                    print(f"Erro ao carregar a imagem: {src_image_path}")
                    continue

                resized_image = cv2.resize(image, (new_width, new_height))
                cv2.imwrite(dst_image_path, resized_image)
                print(f"Imagem {image_file} renomeada para {new_image_name}, redimensionada e movida para {output_folder}")

                # Exclui o arquivo de texto de localização após o uso
                try:
                    os.remove(location_path)
                    print(f"Arquivo de localização {location_file} excluído após uso")
                except FileNotFoundError:
                    print(f"Erro: O arquivo de localização {location_path} não foi encontrado para exclusão.")

                # Remove o arquivo original da pasta de entrada
                os.remove(src_image_path)
            else:
                print("Não há mais arquivos de localização disponíveis.")
                break

# Loop para monitorar a pasta 'imgGrande'
print("Monitorando a pasta 'imgGrande' para renomear imagens. Pressione Ctrl+C para encerrar.")
try:
    while True:
        rename_and_move_images()
        time.sleep(1)  # Pausa de 1 segundo antes de verificar novamente
except KeyboardInterrupt:
    print("\nMonitoramento encerrado.")