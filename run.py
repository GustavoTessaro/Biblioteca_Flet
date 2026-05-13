import subprocess
import sys
import os

def setup_environment():
    venv_dir = "venv"
    is_windows = os.name == "nt"
    
    # Define os caminhos do pip e do comando de ativação
    if is_windows:
        pip_exe = os.path.join(venv_dir, "Scripts", "pip")
        activate_cmd = f".\\{venv_dir}\\Scripts\\activate"
    else:
        pip_exe = os.path.join(venv_dir, "bin", "pip")
        activate_cmd = f"source {venv_dir}/bin/activate"

    # 1. Cria a venv se não existir
    if not os.path.exists(venv_dir):
        print("🌱 Criando ambiente virtual (venv)...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
    
    # 2. Instala as dependências
    print("📦 Instalando Flet e dependências...")
    try:
        # Instala o flet básico
        subprocess.check_call([pip_exe, "install", "flet"])
        
        # Instala do requirements.txt se ele existir na sua pasta
        if os.path.exists("requirements.txt"):
            subprocess.check_call([pip_exe, "install", "-r", "requirements.txt"])
            
        # Mensagem final com instruções
        print("\n" + "="*50)
        print("✅ AMBIENTE CONFIGURADO COM SUCESSO!")
        print("="*50)
        print("\nPara rodar seus arquivos de qualquer pasta, primeiro")
        print("COPIE E COLE o comando abaixo no seu terminal:")
        print(f"\n👉  {activate_cmd}")
        print("\nDepois de colar, você verá '(venv)' no início da linha.")
        print("\nCopie o caminho relativo do arquivo")
        print("Aí é só rodar: python pasta/arquivo.py")
        print("="*50)

    except Exception as e:
        print(f"\n❌ Erro durante a instalação: {e}")

if __name__ == "__main__":
    setup_environment()
