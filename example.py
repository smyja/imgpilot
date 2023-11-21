import requests
import base64

def fetch_image_and_save(input_image_path, prompt, api_key, output_file_path):
    # Read the image from file
    with open(input_image_path, 'rb') as image_file:
        binary_data = image_file.read()

    # Encode binary data to Base64
    base64_data = base64.b64encode(binary_data).decode('utf-8')

    # Create FormData
    files = {'init_image': ('output.jpg', binary_data, 'image/jpeg')}
    data = {
        'image_strength': '0.35',
        'init_image_mode': 'IMAGE_STRENGTH',
        'text_prompts[0][text]': prompt,
        'text_prompts[0][weight]': '1',
        'cfg_scale': '7',
        'clip_guidance_preset': 'FAST_BLUE',
        'sampler': 'K_DPM_2_ANCESTRAL',
        'samples': '3',
        'steps': '30',
    }

    # Set Authorization header
    headers = {'Authorization': f'Bearer {api_key}'}

    # Make the request
    response = requests.post(
        'https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image',
        files=files,
        data=data,
        headers=headers
    )

    if response.status_code != 200:
        print(response.text)
        raise Exception(f"Failed to fetch image. Status code: {response.status_code}")

    # Save the image content to a file
    decoded_content = base64.b64decode(response.json()['artifacts'][0]['base64'])
    with open(output_file_path, 'wb') as output_file:
        output_file.write(decoded_content)

# Example usage:
api_key = "sk-DxMTg0eRrS8oBrbHnvnkoB5rHll97NRJjpJasZpYXsRyzrl9"
input_image_path = "output.jpg"  # Replace with the actual path to your image file
prompt = "A dog space commander"
output_file_path = "output_image.jpg"

fetch_image_and_save(input_image_path, prompt, api_key, output_file_path)
