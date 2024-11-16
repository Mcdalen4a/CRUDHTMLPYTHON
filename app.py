from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json
import os

app = Flask(__name__)


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

DATA_FILE = 'data.json'


def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)


items = load_data()

@app.route('/')
def index():
    return render_template('index.html', items=items)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
     
        image = request.files['image']
        image_filename = None
        if image and image.filename:
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_filename)

     
        new_item = {
            'id': len(items) + 1,
            'name': request.form['name'],
            'description': request.form['description'],
            'image': image_filename  
        }
        items.append(new_item)
        save_data(items)  
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update(item_id):
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        return "Elemento no encontrado", 404

    if request.method == 'POST':
      
        item['name'] = request.form['name']
        item['description'] = request.form['description']

       
        image = request.files['image']
        if image and image.filename:
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_filename)
            item['image'] = image_filename

        save_data(items)  
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    global items
    items = [i for i in items if i['id'] != item_id]
    save_data(items)  
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  
    app.run(debug=True)
