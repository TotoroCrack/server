from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# DataFrame inicial vacío
df = pd.DataFrame(columns=['No. de parte', 'Modelo', 'Descripcion', 'Marca', 'No. Lote', 'No. Existente', 'Precio Compra', 'Precio Venta', 'Fecha Compra', 'Fecha Venta', 'Proveedor', 'Contacto', 'Email', 'Tel'])
usuarios = pd.DataFrame(columns=['username', 'password'])

# Agregar un producto de ejemplo
df.loc[0] = [
    '777',
    'CJIW-TC001',
    'Modulo control de temperatura 4CH in/4CH out',
    'Omron',
    '2724',
    '1',
    '2500',
    '3000',
    '18/1/23',
    '18/1/24',
    'Barmex',
    'Ing Mauro Lopez',
    'mauriciol@barmex.com.mx',
    '55-5328-2600'
]

# Ruta para la página de inicio
@app.route('/')
def index():
    print('Index page')
    return render_template('index.html')

# Ruta para manejar el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Lógica para verificar el usuario y la contraseña
    if not usuarios.empty and (usuarios['username'] == username).any() and (usuarios['password'] == password).any():
        return redirect(url_for('menu'))
    else:
        return redirect(url_for('index'))

# Ruta para manejar el registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    global usuarios
    if request.method == 'POST':
        new_user = pd.DataFrame({
            'username': [request.form['username']],
            'password': [request.form['password']]
        })
        usuarios = pd.concat([usuarios, new_user], ignore_index=True)
        print('New user registered:')
        print(usuarios)
        return redirect(url_for('index'))
    return render_template('register.html')

# Ruta para el menú principal
@app.route('/menu')
def menu():
    return render_template('menu.html')

# Ruta para listar productos
@app.route('/list_products')
def list_products():
    global df
    if df.empty:
        print("El DataFrame está vacío")
    else:
        print(df)  # Esto debería imprimir el DataFrame en la consola
    return render_template('list_products.html', products=df.to_dict(orient='records'))

# Ruta para agregar producto
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    global df
    if request.method == 'POST':
        new_product = pd.DataFrame({
            'No. de parte': [request.form['No. de parte']],
            'Modelo': [request.form['Modelo']],
            'Descripcion': [request.form['Descripcion']],
            'Marca': [request.form['Marca']],
            'No. Lote': [request.form['No. Lote']],
            'No. Existente': [request.form['No. Existente']],
            'Precio Compra': [request.form['Precio Compra']],
            'Precio Venta': [request.form['Precio Venta']],
            'Fecha Compra': [request.form['Fecha Compra']],
            'Fecha Venta': [request.form['Fecha Venta']],
            'Proveedor': [request.form['Proveedor']],
            'Contacto': [request.form['Contacto']],
            'Email': [request.form['Email']],
            'Tel': [request.form['Tel']]
        })
        df = pd.concat([df, new_product], ignore_index=True)
        print('New product added:')
        print(df)  # Verifica que el producto nuevo se añada correctamente
        return redirect(url_for('list_products'))
    print('Add Product page')
    return render_template('add_product.html')

# Ruta para eliminar producto
@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product():
    global df
    if request.method == 'POST':
        part_number = request.form['No. de parte']
        df = df[df['No. de parte'] != part_number]
        print('Product deleted:')
        print(df)  # Verifica que el producto se elimine correctamente
        return redirect(url_for('list_products'))
    print('Delete Product page')
    return render_template('delete_product.html')

# Ruta para editar producto
@app.route('/edit_product/<string:part_number>', methods=['GET', 'POST'])
def edit_product(part_number):
    global df
    product = df[df['No. de parte'] == part_number].to_dict(orient='records')[0]
    if request.method == 'POST':
        for column in df.columns:
            df.loc[df['No. de parte'] == part_number, column] = request.form[column]
        print('Product edited:')
        print(df)  # Verifica que los cambios se guarden correctamente
        return redirect(url_for('list_products'))
    return render_template('edit_product.html', product=product)

if __name__ == '__main__':
    app.run(debug=True)
