import requests
import os
import shutil

# Ensure directories exist
os.makedirs('media/cars/main', exist_ok=True)
os.makedirs('media/cars/gallery', exist_ok=True)

# Car images mapping
car_images = {
    # Main images
    'mercedes_s_class.jpg': 'https://images.unsplash.com/photo-1553440569-bcc63803a83d?w=800&h=600&fit=crop',
    'bmw_m8.jpg': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&h=600&fit=crop',
    'tesla_model_s.jpg': 'https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&h=600&fit=crop',
    'porsche_911.jpg': 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&h=600&fit=crop',
    'ferrari_roma.jpg': 'https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=800&h=600&fit=crop',
    'lamborghini_huracan.jpg': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop',
    'range_rover.jpg': 'https://images.unsplash.com/photo-1566474601545-57c45ada0a7d?w=800&h=600&fit=crop',
    'bentley_bentayga.jpg': 'https://images.unsplash.com/photo-1621004989330-71fcdc05c513?w=800&h=600&fit=crop',
    'rolls_royce_cullinan.jpg': 'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800&h=600&fit=crop',
    'mclaren_720s.jpg': 'https://images.unsplash.com/photo-1551524165-6b6e5a6166f3?w=800&h=600&fit=crop',
    
    # Gallery images (you can use same or different images)
    'mercedes_s_class_1.jpg': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&h=600&fit=crop',
    'mercedes_s_class_2.jpg': 'https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=800&h=600&fit=crop',
    'mercedes_s_class_3.jpg': 'https://images.unsplash.com/photo-1553440569-bcc63803a83d?w=800&h=600&fit=crop',
}

def download_image(url, filename):
    """Download image from URL"""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            return True
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
    return False

print("Downloading car images...")
for filename, url in car_images.items():
    if 'gallery' in filename:
        path = f'media/cars/gallery/{filename}'
    else:
        path = f'media/cars/main/{filename}'
    
    if download_image(url, path):
        print(f"✓ Downloaded: {filename}")
    else:
        print(f"✗ Failed: {filename}")

print("\n✅ Image download complete!")
print(f"Images saved in: media/cars/")