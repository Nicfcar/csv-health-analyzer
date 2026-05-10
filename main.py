import csv
import statistics

def carregar_dados_pacientes(arquivo_csv):
    """Carrega dados de pacientes do arquivo CSV"""
    pacientes = []
    try:
        with open(arquivo_csv, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for linha in reader:
                pacientes.append(linha)
        return pacientes
    except FileNotFoundError:
        print(f"Erro: arquivo '{arquivo_csv}' não encontrado!")
        return None

def calcular_estatisticas(pacientes):
    """Calcula estatísticas básicas dos dados dos pacientes"""
    
    if not pacientes:
        print("Nenhum paciente para analisar!")
        return
    
    # Extrair idades e pressões arteriais
    idades = []
    pressoes_sistolicas = []
    pressoes_diastolicas = []
    
    for paciente in pacientes:
        try:
            idade = int(paciente.get("idade", 0))
            pressao = paciente.get("pressao_arterial", "0/0")
            sistolica, diastolica = map(int, pressao.split("/"))
            
            idades.append(idade)
            pressoes_sistolicas.append(sistolica)
            pressoes_diastolicas.append(diastolica)
        except (ValueError, AttributeError):
            print(f"Aviso: dados inválidos para paciente {paciente}")
            continue
    
    if not idades:
        print("Nenhum dado válido para processar!")
        return
    
    # Calcular estatísticas
    print("\n" + "="*50)
    print("ESTATÍSTICAS DOS PACIENTES")
    print("="*50)
    
    print(f"\nTotal de pacientes: {len(pacientes)}")
    
    print("\n--- IDADE ---")
    print(f"Média: {statistics.mean(idades):.2f} anos")
    print(f"Mediana: {statistics.median(idades):.2f} anos")
    print(f"Mínima: {min(idades)} anos")
    print(f"Máxima: {max(idades)} anos")
    if len(idades) > 1:
        print(f"Desvio padrão: {statistics.stdev(idades):.2f} anos")
    
    print("\n--- PRESSÃO ARTERIAL SISTÓLICA ---")
    print(f"Média: {statistics.mean(pressoes_sistolicas):.2f} mmHg")
    print(f"Mediana: {statistics.median(pressoes_sistolicas):.2f} mmHg")
    print(f"Mínima: {min(pressoes_sistolicas)} mmHg")
    print(f"Máxima: {max(pressoes_sistolicas)} mmHg")
    if len(pressoes_sistolicas) > 1:
        print(f"Desvio padrão: {statistics.stdev(pressoes_sistolicas):.2f} mmHg")
    
    print("\n--- PRESSÃO ARTERIAL DIASTÓLICA ---")
    print(f"Média: {statistics.mean(pressoes_diastolicas):.2f} mmHg")
    print(f"Mediana: {statistics.median(pressoes_diastolicas):.2f} mmHg")
    print(f"Mínima: {min(pressoes_diastolicas)} mmHg")
    print(f"Máxima: {max(pressoes_diastolicas)} mmHg")
    if len(pressoes_diastolicas) > 1:
        print(f"Desvio padrão: {statistics.stdev(pressoes_diastolicas):.2f} mmHg")
    
    print("\n" + "="*50 + "\n")

def main():
    # Carrega e analisa dados dos pacientes
    pacientes = carregar_dados_pacientes("pacientes.csv")
    
    if pacientes:
        print(f"✓ {len(pacientes)} pacientes carregados com sucesso!\n")
        calcular_estatisticas(pacientes)

if __name__ == "__main__":
    main()