import os
import base64
import json
from datetime import datetime

def process_car_data(image_data, car_info):
    """
    Process and save car data including image and attributes
    
    Args:
        image_data (str): Base64 encoded image data
        car_info (dict): Dictionary containing car attributes
    
    Returns:
        dict: Dictionary containing the saved data information
    """
    # Create a unique identifier for this submission
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Save image
    image_filename = f"car_image_{timestamp}.jpg"
    image_path = os.path.join(data_dir, image_filename)
    
    # Remove the base64 header if present
    if ',' in image_data:
        image_data = image_data.split(',')[1]
    
    # Decode and save the image
    with open(image_path, 'wb') as f:
        f.write(base64.b64decode(image_data))
    
    # Create car data dictionary
    car_data = {
        'timestamp': timestamp,
        'image_path': image_filename,
        'damage_type': car_info.get('damageType', ''),
        'car_make': car_info.get('carMake', ''),
        'car_model': car_info.get('carModel', ''),
        'year': car_info.get('year', ''),
        'mileage': car_info.get('mileage', '')
    }
    
    # Save car data to JSON file
    data_filename = f"car_data_{timestamp}.json"
    data_path = os.path.join(data_dir, data_filename)
    
    with open(data_path, 'w') as f:
        json.dump(car_data, f, indent=2)
    
    return {
        'status': 'success',
        'message': 'Car data saved successfully',
        'data': car_data
    }