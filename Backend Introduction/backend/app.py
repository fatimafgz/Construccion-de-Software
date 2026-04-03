from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {
    "origins": "*", 
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"],
    "max_age": 3600
}})

@app.route("/")
def home():
    return "Hello, Flask! Welcome to Session 1."

tasks = []
users = []

# POST - crear usuario
@app.route("/users", methods=["POST"])
def add_user():
    data = request.json

    # Validaciones básicas
    if not data or "name" not in data or "lastname" not in data or "address" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    address = data["address"]

    if "city" not in address or "country" not in address:
        return jsonify({"error": "Incomplete address"}), 400

    user = {
        "id": len(users),
        "name": data["name"].strip(),
        "lastname": data["lastname"].strip(),
        "address": {
            "city": address["city"].strip(),
            "country": address["country"].strip(),
            "postal_code": address["postal_code"].strip()
        }
    }

    users.append(user)
    return jsonify({"message": "User created!", "user": user}), 201

# GET - listar usuarios
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"users": users})

# GET - usuario por ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            return jsonify({"user": user})
    
    return jsonify({"error": "User not found"}), 404

# PUT - actualizar usuario
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    
    
    for user in users:
        if user["id"] == user_id:
            if "name" in data:
                user["name"] = data["name"].strip()
            if "lastname" in data:
                user["lastname"] = data["lastname"].strip()
            
            
            if "address" in data:
                addr = data["address"]
                if "city" in addr:
                    user["address"]["city"] = addr["city"].strip()
                if "country" in addr:
                    user["address"]["country"] = addr["country"].strip()
                if "postal_code" in addr:
                    user["address"]["postal_code"] = addr["postal_code"].strip()
            
            return jsonify({"message": "User updated!", "user": user})
    
    return jsonify({"error": "User not found"}), 404

# DELETE - eliminar usuario
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    for i, user in enumerate(users):
        if user["id"] == user_id:
            removed = users.pop(i)
            return jsonify({"message": "User deleted!", "user": removed})
    
    return jsonify({"error": "User not found"}), 404

# GET - obtener tareas
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})

# GET - obtener una tarea por ID 
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify({"task": task})
    
    return jsonify({"error": "Task not found"}), 404

# POST - crear tarea
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json

    # Validar que exista contenido
    if not data or "content" not in data:
        return jsonify({"error": "Content is required"}), 400

    content = data["content"].strip()

    # Validar que no esté vacío
    if content == "":
        return jsonify({"error": "Content cannot be empty"}), 400
    
    task = {
        "id": len(tasks),
        "content": content,
        "done": False  
    }
    tasks.append(task)
    return jsonify({"message": "Task added!", "task": task}), 201

# PUT - marcar tarea como completada
@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return jsonify({"message": "Task completed!", "task": task})
    
    return jsonify({"error": "Task not found"}), 404

# PUT - actualizar tarea
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if task_id >= len(tasks):
        return jsonify({"error": "Task not found"}), 404
    data = request.json
    tasks[task_id]["content"] = data.get("content", tasks[task_id]["content"])
    return jsonify({"message": "Task updated!", "task": tasks[task_id]})

# DELETE - eliminar tarea
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id >= len(tasks):
        return jsonify({"error": "Task not found"}), 404
    removed = tasks.pop(task_id)
    return jsonify({"message": "Task deleted!", "task": removed})



if __name__ == "__main__":
    app.run(debug=True)