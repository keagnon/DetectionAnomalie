import os
import subprocess

# Installer Sphinx si nécessaire
def install_sphinx():
    subprocess.run(["poetry", "add", "--dev", "sphinx", "sphinx-autodoc-typehints"], check=True)
    subprocess.run(["poetry", "run", "sphinx-quickstart", "-q", "-p", "{{cookiecutter.project_name}}", "-a", "Author", "-v", "0.1", "--sep", "--ext-autodoc", "--ext-viewcode", "docs"], check=True)

# Rechercher les fichiers Python dans src/ et exclure __init__.py
def get_python_files():
    src_dir = os.path.join("src")
    py_files = [f for f in os.listdir(src_dir) if f.endswith('.py') and f != "__init__.py"]
    return py_files

# Générer automatiquement les fichiers .rst pour chaque fichier .py
def generate_docs():
    py_files = get_python_files()
    docs_dir = os.path.join("docs")
    for py_file in py_files:
        module = py_file.replace('.py', '')
        rst_file = os.path.join(docs_dir, f"{module}.rst")
        with open(rst_file, "w") as f:
            f.write(f"{module} module\n")
            f.write("=" * (len(module) + 7) + "\n\n")
            f.write(f".. automodule:: src.{module}\n")
            f.write("   :members:\n")
    
    # Ajouter les fichiers .rst dans index.rst
    index_path = os.path.join(docs_dir, "index.rst")
    with open(index_path, "a") as index_file:
        for py_file in py_files:
            module = py_file.replace('.py', '')
            index_file.write(f"   {module}\n")

# Exécution
if __name__ == "__main__":
    install_sphinx()
    generate_docs()
