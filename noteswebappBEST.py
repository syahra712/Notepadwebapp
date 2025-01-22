from flask import Flask, request, redirect, render_template_string, flash, url_for
from flask_pymongo import PyMongo
from bson import ObjectId
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Initialize extensions
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User model for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, email, name):
        self.id = user_id
        self.email = email
        self.name = name

@login_manager.user_loader
def load_user(user_id):
    """Load user from the database by user ID."""
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(str(user["_id"]), user["email"], user["name"])
    return None

# HTML Templates
login_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Notes App</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gradient-to-r from-blue-50 to-blue-100 text-gray-800 flex items-center justify-center min-h-screen">
    <div class="bg-white p-8 rounded-lg shadow-xl w-96 transform hover:shadow-2xl transition duration-200">
        <h1 class="text-3xl font-bold mb-6 text-center text-blue-600">
            <i class="fas fa-sign-in-alt mr-2"></i>Login
        </h1>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="mb-4 p-4 rounded-lg {% if category == 'danger' %}bg-red-100 text-red-700{% else %}bg-green-100 text-green-700{% endif %}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form action="/login" method="POST" class="space-y-4">
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-2">
                    <i class="fas fa-envelope mr-2"></i>Email
                </label>
                <input type="email" name="email" required 
                    class="shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md p-2"
                    placeholder="your@email.com">
            </div>
            
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-2">
                    <i class="fas fa-lock mr-2"></i>Password
                </label>
                <input type="password" name="password" required 
                    class="shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md p-2"
                    placeholder="••••••••">
            </div>

            <button type="submit" 
                class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition duration-200 flex items-center justify-center">
                <i class="fas fa-sign-in-alt mr-2"></i>Login
            </button>
        </form>

        <p class="mt-6 text-center text-gray-600">
            Don't have an account? 
            <a href="/register" class="text-blue-500 hover:text-blue-600 font-bold">Register</a>
        </p>
    </div>
</body>
</html>
'''

register_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register - Notes App</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gradient-to-r from-blue-50 to-blue-100 text-gray-800 flex items-center justify-center min-h-screen">
    <div class="bg-white p-8 rounded-lg shadow-xl w-96 transform hover:shadow-2xl transition duration-200">
        <h1 class="text-3xl font-bold mb-6 text-center text-blue-600">
            <i class="fas fa-user-plus mr-2"></i>Register
        </h1>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="mb-4 p-4 rounded-lg {% if category == 'danger' %}bg-red-100 text-red-700{% else %}bg-green-100 text-green-700{% endif %}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <form action="/register" method="POST" class="space-y-4">
            <div>
                <label class="block text-gray-700 text-sm font-bold mb-2">
                    <i class="fas fa-user mr-2"></i>Full Name
                </label>
                <input type="text" name="name" required 
                    class="shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md p-2"
                    placeholder="John Doe">
            </div>

            <div>
                <label class="block text-gray-700 text-sm font-bold mb-2">
                    <i class="fas fa-envelope mr-2"></i>Email
                </label>
                <input type="email" name="email" required 
                    class="shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md p-2"
                    placeholder="your@email.com">
            </div>

            <div>
                <label class="block text-gray-700 text-sm font-bold mb-2">
                    <i class="fas fa-lock mr-2"></i>Password
                </label>
                <input type="password" name="password" required 
                    class="shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md p-2"
                    placeholder="••••••••">
            </div>

            <button type="submit" 
                class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition duration-200 flex items-center justify-center">
                <i class="fas fa-user-plus mr-2"></i>Register
            </button>
        </form>

        <p class="mt-6 text-center text-gray-600">
            Already have an account? 
            <a href="/login" class="text-blue-500 hover:text-blue-600 font-bold">Login</a>
        </p>
    </div>
</body>
</html>
'''

index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Notes</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.12.0/dist/cdn.min.js" defer></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gradient-to-r from-blue-50 to-blue-100 text-gray-800 min-h-screen">
    <nav class="bg-white shadow-lg">
        <div class="container mx-auto px-6 py-4 flex justify-between items-center">
            <h1 class="text-2xl font-bold text-blue-600">Welcome, {{ current_user.name }}</h1>
            <div class="flex items-center space-x-4">
                <span class="text-gray-600">
                    <i class="fas fa-user mr-2"></i>{{ current_user.email }}
                </span>
                <a href="/logout" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition duration-200">
                    <i class="fas fa-sign-out-alt mr-2"></i>Logout
                </a>
            </div>
        </div>
    </nav>

    <div class="container mx-auto px-4 py-8">
        <!-- Flash Messages -->
        <div x-data="{ show: true }" x-show="show" class="mb-6">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="animate-fade-in-down bg-{{ 'green' if category == 'success' else 'red' }}-100 border-l-4 border-{{ 'green' if category == 'success' else 'red' }}-500 text-{{ 'green' if category == 'success' else 'red' }}-700 p-4 rounded-lg shadow relative" role="alert">
                            <div class="flex items-center">
                                <i class="fas fa-{{ 'check-circle' if category == 'success' else 'exclamation-circle' }} mr-2"></i>
                                <span class="block sm:inline">{{ message }}</span>
                            </div>
                            <button @click="show = false" class="absolute top-0 right-0 p-4">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>

        <!-- Add Note Card -->
        <div class="bg-white rounded-lg shadow-lg p-6 mb-8 transform hover:shadow-xl transition duration-200">
            <h2 class="text-xl font-bold mb-4 text-gray-700 flex items-center">
                <i class="fas fa-plus-circle mr-2 text-blue-500"></i>Add New Note
            </h2>
            <form action="/add_note" method="POST" class="space-y-4">
                <div class="relative">
                    <label class="block text-gray-700 text-sm font-bold mb-2" for="note">
                        <i class="fas fa-pen mr-2"></i>Note Content
                    </label>
                    <textarea name="note" id="note" rows="3" required 
                        class="shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md p-2"
                        placeholder="What's on your mind?"></textarea>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-gray-700 text-sm font-bold mb-2" for="tags">
                            <i class="fas fa-tags mr-2"></i>Tags
                        </label>
                        <input type="text" name="tags" id="tags" 
                            class="shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                            placeholder="work, personal, ideas">
                    </div>

                    <div>
                        <label class="block text-gray-700 text-sm font-bold mb-2" for="priority">
                            <i class="fas fa-flag mr-2"></i>Priority
                        </label>
                        <select name="priority" id="priority" 
                            class="shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md">
                            <option value="Low">Low</option>
                            <option value="Medium">Medium</option>
                            <option value="High">High</option>
                        </select>
                    </div>
                </div>

                <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-4 rounded-lg transition duration-200 flex items-center justify-center">
                    <i class="fas fa-plus mr-2"></i>Add Note
                </button>
            </form>
        </div>

        <!-- Notes Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {% for note in notes %}
            <div class="bg-white rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition duration-200 border-t-4 
                {% if note.priority == 'High' %}border-red-500{% elif note.priority == 'Medium' %}border-yellow-500{% else %}border-green-500{% endif %}">
                <div class="p-6">
                    <div class="flex items-center justify-between mb-4">
                        <span class="px-3 py-1 rounded-full text-sm font-semibold 
                            {% if note.priority == 'High' %}bg-red-100 text-red-800
                            {% elif note.priority == 'Medium' %}bg-yellow-100 text-yellow-800
                            {% else %}bg-green-100 text-green-800{% endif %}">
                            <i class="fas fa-flag mr-1"></i>{{ note.priority }}
                        </span>
                        <div class="flex space-x-2">
                            <button class="text-blue-500 hover:text-blue-600 edit-btn" 
                                data-id="{{ note._id }}" 
                                data-note="{{ note.note }}" 
                                data-tags="{{ note.tags | join(', ') }}" 
                                data-priority="{{ note.priority }}">
                                <i class="fas fa-edit"></i>
                            </button>
                            <form action="/delete_note/{{ note._id }}" method="POST" class="inline">
                                <button class="text-red-500 hover:text-red-600" 
                                    onclick="return confirm('Are you sure you want to delete this note?')">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </form>
                        </div>
                    </div>
                    <p class="text-gray-800 mb-4">{{ note.note }}</p>
                    <div class="flex flex-wrap gap-2">
                        {% for tag in note.tags %}
                            {% if tag.strip() %}
                            <span class="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                                <i class="fas fa-tag mr-1"></i>{{ tag.strip() }}
                            </span>
                            {% endif %}
                        {% endfor %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- Edit Note Modal -->
    <div id="editModal" class="fixed z-50 inset-0 hidden">
        <div class="absolute inset-0 bg-gray-800 bg-opacity-75 backdrop-filter backdrop-blur-sm"></div>
        <div class="absolute inset-0 flex items-center justify-center p-4">
            <div class="bg-white rounded-lg shadow-xl w-full max-w-md transform transition-all">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h2 class="text-2xl font-bold text-gray-800">
                        <i class="fas fa-edit mr-2"></i>Edit Note
                    </h2>
                </div>
                <form id="editForm" action="/edit_note" method="POST" class="p-6">
                    <input type="hidden" name="note_id" id="editNoteId">
                    <div class="space-y-4">
                        <div>
                            <label for="editNote" class="block text-gray-700 font-medium mb-2">Note Content</label>
                            <textarea id="editNote" name="note" rows="3" 
                                class="shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"></textarea>
                        </div>
                        <div>
                            <label for="editTags" class="block text-gray-700 font-medium mb-2">Tags</label>
                            <input type="text" id="editTags" name="tags" 
                                class="shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md">
                        </div>
                        <div>
                            <label for="editPriority" class="block text-gray-700 font-medium mb-2">Priority</label>
                            <select id="editPriority" name="priority" 
                                class="shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md">
                                <option value="Low">Low</option>
                                <option value="Medium">Medium</option>
                                <option value="High">High</option>
                            </select>
                        </div>
                    </div>
                    <div class="mt-6 flex justify-end space-x-3">
                        <button type="button" class="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition duration-200 close-modal">
                            <i class="fas fa-times mr-2"></i>Cancel
                        </button>
                        <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition duration-200">
                            <i class="fas fa-save mr-2"></i>Save Changes
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <script>
        // Modal functionality
        const modal = document.getElementById('editModal');
        
        document.querySelectorAll('.edit-btn').forEach(button => {
            button.addEventListener('click', function() {
                modal.classList.remove('hidden');
                document.getElementById('editNoteId').value = this.dataset.id;
                document.getElementById('editNote').value = this.dataset.note;
                document.getElementById('editTags').value = this.dataset.tags;
                document.getElementById('editPriority').value = this.dataset.priority;
            });
        });

        document.querySelectorAll('.close-modal').forEach(button => {
            button.addEventListener('click', function() {
                modal.classList.add('hidden');
            });
        });

        // Close modal when clicking outside
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });

        // Flash message auto-hide
        setTimeout(() => {
            const flashMessages = document.querySelectorAll('[role="alert"]');
            flashMessages.forEach(message => {
                message.style.display = 'none';
            });
        }, 5000);
    </script>
</body>
</html>
'''

@app.route("/")
@login_required
def index():
    notes = mongo.db.notes.find({"user_id": ObjectId(current_user.id)})
    return render_template_string(index_html, notes=notes)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        if mongo.db.users.find_one({"email": email}):
            flash("Email already registered.", "danger")
            return redirect(url_for("register"))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        mongo.db.users.insert_one({"name": name, "email": email, "password": hashed_password})
        flash("Registration successful.", "success")
        return redirect(url_for("login"))
    return render_template_string(register_html)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = mongo.db.users.find_one({"email": email})
        if user and bcrypt.check_password_hash(user["password"], password):
            user_obj = User(str(user["_id"]), user["email"], user["name"])
            login_user(user_obj)
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        flash("Invalid credentials.", "danger")
    return render_template_string(login_html)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

@app.route("/add_note", methods=["POST"])
@login_required
def add_note():
    note_content = request.form.get("note")
    tags = [tag.strip() for tag in request.form.get("tags", "").split(",") if tag.strip()]
    priority = request.form.get("priority", "Low")
    mongo.db.notes.insert_one({
        "user_id": ObjectId(current_user.id),
        "note": note_content,
        "tags": tags,
        "priority": priority
    })
    flash("Note added successfully.", "success")
    return redirect(url_for("index"))

@app.route("/edit_note", methods=["POST"])
@login_required
def edit_note():
    note_id = request.form.get("note_id")
    note_content = request.form.get("note")
    tags = [tag.strip() for tag in request.form.get("tags", "").split(",") if tag.strip()]
    priority = request.form.get("priority", "Low")
    
    result = mongo.db.notes.update_one(
        {"_id": ObjectId(note_id), "user_id": ObjectId(current_user.id)},
        {"$set": {"note": note_content, "tags": tags, "priority": priority}}
    )
    
    if result.modified_count > 0:
        flash("Note updated successfully!", "success")
    else:
        flash("Error updating note.", "danger")
    return redirect(url_for("index"))

@app.route("/delete_note/<note_id>", methods=["POST"])
@login_required
def delete_note(note_id):
    result = mongo.db.notes.delete_one({
        "_id": ObjectId(note_id),
        "user_id": ObjectId(current_user.id)
    })
    if result.deleted_count == 0:
        flash("Note not found or not authorized to delete.", "danger")
    else:
        flash("Note deleted successfully.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
