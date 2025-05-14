from flows.main_flow import run_flow

# Caminho real do arquivo para teste
real_file_path = "data/seu arquivo.pdf"  # Substitua pelo caminho do seu arquivo real

def test_run_real_flow():
    result = run_flow(real_file_path)
    
    print("\n📊 RESULTADO FINAL DO FLUXO CREW AI:\n")
    print(result)

if __name__ == "__main__":
    test_run_real_flow()
