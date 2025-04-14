from flask import Flask, render_template, request, send_file  
from rembg import remove  
from PIL import Image  
import os

app = Flask(__name__)

# Configure upload folder  
UPLOAD_FOLDER = 'static/uploads'  
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure Flask-Dropzone  
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True  
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'  
app.config['DROPZONE_MAX_FILE_SIZE'] = 3  
app.config['DROPZONE_MAX_FILES'] = 1

@app.route('/', methods=['GET', 'POST'])  
def index():  
    if request.method == 'POST':  
        if 'file' not in request.files:  
            return 'No file uploaded'  
          
        file = request.files['file']  
        if file.filename == '':  
            return 'No file selected'

        # Save original image  
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input.png')  
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png')  
        file.save(input_path)

        # Remove background  
        input_image = Image.open(input_path)  
        output_image = remove(input_image)  
        output_image.save(output_path)

        return send_file(output_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':  
    app.run(debug=True)  