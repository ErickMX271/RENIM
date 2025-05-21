from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_super_secreta"  # Necesaria para usar sesiones

# Usuario y contraseña definidos (puedes cambiar esto o poner varios si gustas)
USUARIOS = {}  # Usamos un diccionario para almacenar los usuarios registrados

# Lista de medicamentos
medicamentos = [
    {"id": 1, "nombre": "Paracetamol", "categoria": "Analgésico", "cantidad": 100, "disponible": True},
    {"id": 2, "nombre": "Ibuprofeno", "categoria": "Antiinflamatorio", "cantidad": 50, "disponible": False},
]

@app.route("/")
def inicio():
    return render_template("index.html")

# Ruta de login
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]
        if usuario in USUARIOS and USUARIOS[usuario] == contrasena:
            session["usuario"] = usuario
            return redirect(url_for("medicamentos_view"))
        else:
            error = "Usuario o contraseña incorrectos."
    return render_template("login.html", error=error)

# Ruta de logout
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("inicio"))

# Sección protegida: Medicamentos
@app.route("/medicamentos")
def medicamentos_view():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("medicamentos.html", medicamentos=medicamentos)

# Sección protegida: Agregar medicamentos
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if "usuario" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        categoria = request.form["categoria"]
        cantidad = int(request.form["cantidad"])
        disponible = "disponible" in request.form

        nuevo_id = len(medicamentos) + 1
        nuevo_medicamento = {
            "id": nuevo_id,
            "nombre": nombre,
            "categoria": categoria,
            "cantidad": cantidad,
            "disponible": disponible
        }

        medicamentos.append(nuevo_medicamento)
        return redirect(url_for("medicamentos_view"))
    
    return render_template("agregar.html")

# Ruta para registro de usuario
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]

        # Verificar si el usuario ya está registrado
        if usuario in USUARIOS:
            error = "El usuario ya existe. Por favor, elige otro."
            return render_template("registro.html", error=error)

        # Registrar el nuevo usuario
        USUARIOS[usuario] = contrasena
        return redirect(url_for("login"))
    
    return render_template("registro.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/acerca")
def acerca():
    return render_template("acerca.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    medicamento = next((m for m in medicamentos if m["id"] == id), None)

    if not medicamento:
        return redirect(url_for("medicamentos_view"))

    if request.method == "POST":
        medicamento["nombre"] = request.form["nombre"]
        medicamento["categoria"] = request.form["categoria"]
        medicamento["cantidad"] = int(request.form["cantidad"])
        medicamento["disponible"] = "disponible" in request.form

        return redirect(url_for("medicamentos_view"))

    return render_template("editar.html", medicamento=medicamento)

@app.route("/eliminar/<int:id>")
def eliminar(id):
    medicamento = next((m for m in medicamentos if m["id"] == id), None)
    
    if medicamento:
        medicamentos.remove(medicamento)
        
    return redirect(url_for("medicamentos_view"))

@app.route("/consulta")
def consulta():
    return render_template("consulta.html", medicamentos=medicamentos)

if __name__ == "__main__":
    app.run(debug=True)
