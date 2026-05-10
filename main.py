import csv
import statistics
import sys
from pathlib import Path

class AnalisadorPacientes:
    """Responsável por análise de dados de pacientes em CSV"""
    
    def __init__(self, caminho_arquivo_csv):
        self.caminho_arquivo = Path(caminho_arquivo_csv)
        self.pacientes_brutos = []
        self.dados_numericos_extraidos = {}
    
    def carregar_arquivo_csv(self):
        """Carrega e valida o arquivo CSV de pacientes"""
        try:
            with open(self.caminho_arquivo, newline="", encoding="utf-8") as arquivo:
                leitor_csv = csv.DictReader(arquivo)
                self.pacientes_brutos = list(leitor_csv)
            
            if not self.pacientes_brutos:
                print(f"⚠️  Arquivo '{self.caminho_arquivo}' vazio!")
                return False
            
            print(f"✓ {len(self.pacientes_brutos)} pacientes carregados!")
            return True
        
        except FileNotFoundError:
            print(f"❌ Erro: arquivo '{self.caminho_arquivo}' não encontrado!")
            return False
        except Exception as erro:
            print(f"❌ Erro ao ler arquivo: {erro}")
            return False
    
    def _identificar_coluna_idade(self):
        """Identifica automaticamente a coluna de idade"""
        variações_idade = ["idade", "age", "anos", "age_years"]
        
        for coluna in self.pacientes_brutos[0].keys():
            coluna_lower = coluna.lower().replace("_", " ").replace("-", " ")
            if any(var in coluna_lower for var in variações_idade):
                return coluna
        return None
    
    def _identificar_coluna_pressao(self):
        """Identifica automaticamente a coluna de pressão arterial"""
        palavras_chave_pressao = ["pressao", "pressão", "pressure", "blood_pressure", "pressao_arterial", "pressão_arterial"]
        
        for coluna in self.pacientes_brutos[0].keys():
            coluna_lower = coluna.lower().replace("_", " ").replace("-", " ")
            # Verificar correspondência exata de palavras
            palavras = coluna_lower.split()
            for palavra in palavras:
                for chave in palavras_chave_pressao:
                    if chave.replace("_", " ") in palavra or palavra in chave:
                        return coluna
            # Verificar se a coluna contém substring significativa
            for chave in palavras_chave_pressao:
                if chave in coluna_lower:
                    return coluna
        return None
    
    def _extrair_valor_numerico(self, valor_bruto):
        """Converte valor para número, retornando None se inválido"""
        try:
            return float(valor_bruto)
        except (ValueError, TypeError):
            return None
    
    def _extrair_sistolica_diastolica(self, valor_pressao):
        """Separa pressão no formato 'sistólica/diastólica'"""
        try:
            partes = str(valor_pressao).split("/")
            if len(partes) == 2:
                sistolica = float(partes[0])
                diastolica = float(partes[1])
                return sistolica, diastolica
        except (ValueError, IndexError):
            pass
        return None, None
    
    def extrair_dados_numericos(self):
        """Extrai dados numéricos relevantes do CSV"""
        coluna_idade = self._identificar_coluna_idade()
        coluna_pressao = self._identificar_coluna_pressao()
        
        if not coluna_idade and not coluna_pressao:
            print("⚠️  Nenhuma coluna de idade ou pressão encontrada!")
            return False
        
        idades_valores = []
        pressoes_sistolicas = []
        pressoes_diastolicas = []
        
        for paciente in self.pacientes_brutos:
            # Processar idade
            if coluna_idade:
                valor_idade = self._extrair_valor_numerico(paciente.get(coluna_idade))
                if valor_idade is not None:
                    idades_valores.append(valor_idade)
            
            # Processar pressão arterial
            if coluna_pressao:
                sist, diast = self._extrair_sistolica_diastolica(paciente.get(coluna_pressao))
                if sist is not None and diast is not None:
                    pressoes_sistolicas.append(sist)
                    pressoes_diastolicas.append(diast)
        
        self.dados_numericos_extraidos = {
            "idade": {
                "coluna": coluna_idade,
                "valores": idades_valores
            },
            "pressao_sistolica": {
                "coluna": coluna_pressao,
                "valores": pressoes_sistolicas
            },
            "pressao_diastolica": {
                "coluna": coluna_pressao,
                "valores": pressoes_diastolicas
            }
        }
        
        return bool(idades_valores or pressoes_sistolicas)
    
    def _calcular_estatisticas_basicas(self, valores):
        """Calcula média, mediana, mín, máx e desvio padrão"""
        if not valores:
            return None
        
        return {
            "media": statistics.mean(valores),
            "mediana": statistics.median(valores),
            "minimo": min(valores),
            "maximo": max(valores),
            "desvio_padrao": statistics.stdev(valores) if len(valores) > 1 else 0
        }
    
    def _exibir_estatisticas_campo(self, nome_campo, unidade, valores):
        """Exibe estatísticas formatadas para um campo específico"""
        if not valores:
            return
        
        stats = self._calcular_estatisticas_basicas(valores)
        
        print(f"\n--- {nome_campo.upper()} ---")
        print(f"Média:          {stats['media']:.2f} {unidade}")
        print(f"Mediana:        {stats['mediana']:.2f} {unidade}")
        print(f"Mínimo:         {stats['minimo']:.2f} {unidade}")
        print(f"Máximo:         {stats['maximo']:.2f} {unidade}")
        print(f"Desvio padrão:  {stats['desvio_padrao']:.2f} {unidade}")
    
    def gerar_relatorio_estatistico(self):
        """Gera e exibe relatório completo de estatísticas"""
        print("\n" + "="*55)
        print("RELATÓRIO ESTATÍSTICO DE PACIENTES")
        print("="*55)
        print(f"\nTotal de pacientes analisados: {len(self.pacientes_brutos)}")
        
        dados_idade = self.dados_numericos_extraidos.get("idade", {})
        dados_pressao_sistolica = self.dados_numericos_extraidos.get("pressao_sistolica", {})
        dados_pressao_diastolica = self.dados_numericos_extraidos.get("pressao_diastolica", {})
        
        if dados_idade.get("valores"):
            self._exibir_estatisticas_campo("Idade", "anos", dados_idade["valores"])
        
        if dados_pressao_sistolica.get("valores"):
            self._exibir_estatisticas_campo("Pressão Arterial Sistólica", "mmHg", dados_pressao_sistolica["valores"])
        
        if dados_pressao_diastolica.get("valores"):
            self._exibir_estatisticas_campo("Pressão Arterial Diastólica", "mmHg", dados_pressao_diastolica["valores"])
        
        print("\n" + "="*55 + "\n")
    
    def executar_analise_completa(self):
        """Executa o fluxo completo de análise"""
        if not self.carregar_arquivo_csv():
            return False
        
        if not self.extrair_dados_numericos():
            print("❌ Nenhum dado numérico válido encontrado!")
            return False
        
        self.gerar_relatorio_estatistico()
        return True


def obter_caminho_arquivo():
    """Obtém caminho do arquivo CSV (argumentos ou input do usuário)"""
    if len(sys.argv) > 1:
        return sys.argv[1]
    
    caminho_padrao = "pacientes.csv"
    entrada = input(f"Informe o caminho do arquivo CSV [{caminho_padrao}]: ").strip()
    return entrada if entrada else caminho_padrao


def main():
    """Ponto de entrada principal do programa"""
    caminho_csv = obter_caminho_arquivo()
    
    analisador = AnalisadorPacientes(caminho_csv)
    analisador.executar_analise_completa()


if __name__ == "__main__":
    main()