import os
import sys
import shutil
import subprocess


def build_windows():
    print("=" * 60)
    print("Iniciando build do executável para Windows...")
    print("=" * 60)
    
    if os.path.exists('build'):
        print("Removendo diretório build antigo...")
        shutil.rmtree('build')
    
    if os.path.exists('dist'):
        print("Removendo diretório dist antigo...")
        shutil.rmtree('dist')
    
    sep = ';' if os.name == 'nt' else ':'
    
    # Usar o pyinstaller do ambiente virtual ou do Python atual
    pyinstaller_cmd = 'pyinstaller'
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # Estamos em um ambiente virtual
        venv_scripts = os.path.join(sys.prefix, 'Scripts')
        pyinstaller_path = os.path.join(venv_scripts, 'pyinstaller.exe')
        if os.path.exists(pyinstaller_path):
            pyinstaller_cmd = pyinstaller_path
    
    command = [
        pyinstaller_cmd,
        '--name=T2FCalculadoraEventos',
        '--windowed',
        '--onefile',
        '--icon=icon.ico' if os.path.exists('icon.ico') else '',
        f'--add-data=src{sep}src',
        f'--add-data=icon.ico{sep}.' if os.path.exists('icon.ico') else '',
        f'--add-data=t2f.png{sep}.' if os.path.exists('t2f.png') else '',
        '--noconsole',
        'main.py'
    ]
    
    command = [arg for arg in command if arg]
    
    print("\nExecutando PyInstaller...")
    print(f"Comando: {' '.join(command)}\n")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        print("\n" + "=" * 60)
        print("Build concluído com sucesso!")
        print("=" * 60)
        print(f"\nO executável está em: dist/CalculadoraEventos.exe")
        print("\nVocê pode distribuir o arquivo .exe para outros computadores Windows.")
        print("Não é necessário instalar Python ou outras dependências.")
        
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 60)
        print("ERRO durante o build!")
        print("=" * 60)
        print(e.stderr)
        sys.exit(1)


def check_dependencies():
    print("Verificando dependências...\n")
    
    try:
        import PySide6
        print("✓ PySide6 instalado")
    except ImportError:
        print("✗ PySide6 não encontrado")
        return False
    
    try:
        import matplotlib
        print("✓ matplotlib instalado")
    except ImportError:
        print("✗ matplotlib não encontrado")
        return False
    
    try:
        import PyInstaller
        print("✓ PyInstaller instalado")
    except ImportError:
        print("✗ PyInstaller não encontrado")
        return False
    
    print("\nTodas as dependências estão instaladas!\n")
    return True


if __name__ == '__main__':
    print("Calculadora de Eventos - Build Script")
    print("=" * 60)
    
    if not check_dependencies():
        print("\nInstalando dependências...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("\nDependências instaladas. Execute o script novamente.")
        sys.exit(0)
    
    build_windows()