#Codigo4 que trata as imagens:

import cv2
import os
import time
import base64
import requests
import shutil

# Caminhos das pastas
input_folder = 'imgGrande'
output_folder = 'capturas'  # Agora as imagens redimensionadas serão salvas na pasta 'capturas'

# Criar as pastas se elas não existirem
os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Definir tamanho desejado para a imagem
new_width = 300
new_height = 170

# Configuração da API
api_key = "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"  # Substitua pela sua chave da API
api_endpoint = "https://api.openai.com/v1/chat/completions"
capturas_path = "capturas"  # Pasta onde as imagens redimensionadas serão salvas
enviadas_path = "enviadas"  # Pasta para mover as imagens processadas
output_folders = {
    "Buraco": "buracos",
    "Mato Alto": "mato_alto",
    "Bueiro Aberto": "bueiros_abertos",
    "Sem Problemas": "ok",
    "garrafa": "garrafa",
    "copo": "copo",
    "celular": "celular"
}

# Certifique-se de que todas as pastas existem
os.makedirs(enviadas_path, exist_ok=True)
for folder in output_folders.values():
    os.makedirs(folder, exist_ok=True)

# Função para codificar a imagem em base64
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Erro: Caminho da imagem {image_path} não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao codificar a imagem {image_path}: {e}")
        return None

# Função para processar imagens na pasta
def process_images():
    for image_name in os.listdir(capturas_path):
        image_path = os.path.join(capturas_path, image_name)

        # Verifica se o arquivo é uma imagem válida
        if not os.path.isfile(image_path) or not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        # Codifica a imagem
        base64_image = encode_image(image_path)

        if base64_image:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Quero que você analise a imagem e me responda se você encontra alguma dessas coisas na imagem, me responda com apenas algum desses itens: Buraco, Mato Alto, Bueiro Aberto, Sem Problemas, garrafa, copo, celular"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            try:
                # Envio da solicitação para a API
                response = requests.post(api_endpoint, headers=headers, json=payload)
                if response.status_code == 200:
                    # Extrai apenas o conteúdo de 'content' da resposta
                    data = response.json()
                    if "choices" in data and data["choices"]:
                        content = data["choices"][0].get("message", {}).get("content", "Conteúdo não encontrado.").strip()
                        print(f"Resposta para {image_name}: {content}")

                        # Determina a pasta de destino com base na resposta
                        destination_folder = output_folders.get(content, enviadas_path)
                        shutil.move(image_path, os.path.join(destination_folder, image_name))
                        print(f"Imagem {image_name} movida para a pasta '{destination_folder}'.")
                    else:
                        print(f"Nenhuma resposta encontrada para {image_name}.")
                else:
                    print(f"Erro na API para {image_name}: {response.status_code} - {response.text}")

            except requests.RequestException as e:
                print(f"Erro na solicitação para {image_name}: {e}")
        else:
            print(f"Falha ao processar {image_name}.")

# Loop contínuo para redimensionar e processar imagens
print("Monitorando a pasta 'imgGrande' para redimensionar imagens e a pasta 'capturas' para processá-las. Pressione Ctrl+C para encerrar.")
try:
    while True:
        # Redimensionar imagens da pasta 'imgGrande' e mover para 'capturas'
        for image_name in os.listdir(input_folder):
            if image_name.lower().endswith((".jpg", ".jpeg", ".png")):  # Checando se o arquivo é uma imagem
                input_path = os.path.join(input_folder, image_name)
                output_path = os.path.join(output_folder, image_name)

                # Ler imagem
                img = cv2.imread(input_path)
                if img is None:
                    print(f"Não foi possível ler a imagem de {input_path}")
                    continue

                # Redimensionar imagem
                resized_img = cv2.resize(img, (new_width, new_height))

                # Salvar imagem redimensionada
                cv2.imwrite(output_path, resized_img)
                print(f'Imagem {image_name} redimensionada e movida para {output_path}')

                # Remover a imagem original após processamento
                os.remove(input_path)
                print(f'Imagem original {image_name} removida de {input_folder}')

        # Processar imagens na pasta 'capturas'
        process_images()
        time.sleep(1)  # Pausa de 1 segundo antes de verificar novamente
except KeyboardInterrupt:
    print("\nMonitoramento encerrado.")