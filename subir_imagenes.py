import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

media_root = 'proyecto/media'

for root, dirs, files in os.walk(media_root):
    for filename in files:
        filepath = os.path.join(root, filename)
        public_id = filepath.replace('\\', '/').replace('media/', '')
        print(f"Subiendo {filepath}...")
        cloudinary.uploader.upload(filepath, public_id=public_id, overwrite=True)
        print(f"✅ {filename} subido")

print("¡Todas las imágenes subidas!")