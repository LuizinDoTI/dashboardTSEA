# ai_agent.py
"""
Módulo do Agente de IA para o Dashboard TSEA
Contém toda a lógica para interagir com o Large Language Model (LLM).
"""
import google.generativeai as genai
import pandas as pd
from config import METRICAS_CONFIG
import streamlit as st

# --- Configuração da API ---
# Idealmente, a chave viria de st.secrets para deploy
# ou de um arquivo .env para desenvolvimento local.
# Por enquanto, vamos configurar diretamente para teste.
# Lembre-se de NUNCA colocar sua chave diretamente no código em um repo público.

try:
    # Tenta obter a chave da API dos segredos do Streamlit (para deploy)
    api_key = st.secrets["GOOGLE_API_KEY"]
except (FileNotFoundError, KeyError):
    # Se não encontrar, avisa para configurar localmente
    st.warning("Chave da API do Google não encontrada nos segredos. Certifique-se de configurar seu arquivo `secrets.toml` para deploy.")
    api_key = "" # Deixe em branco se não configurado

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

class AIAgent:
    """
    O agente de IA que realiza análises inteligentes sobre os dados.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def _checar_modelo(self):
        if model is None:
            st.error("O modelo de IA não foi inicializado. Verifique a configuração da sua chave de API.")
            return False
        return True

    def gerar_diagnostico_transformador(self, id_transformador: str) -> str:
        """
        Gera uma análise completa para um único transformador.

        Args:
            id_transformador: O ID do transformador a ser analisado.

        Returns:
            Uma string em Markdown com a análise completa.
        """
        if not self._checar_modelo():
            return ""

        dados_trafo = self.df[self.df['ID_Transformador'] == id_transformador].iloc[0]

        prompt = f"""
        Você é um engenheiro especialista sênior da TSEA Energia, com 30 anos de experiência em diagnóstico de falhas de transformadores de potência.
        Sua tarefa é analisar os dados de um ensaio de um transformador e fornecer um relatório técnico detalhado, claro e acionável.

        **Dados do Ensaio do Transformador:**
        - **ID:** {dados_trafo['ID_Transformador']}
        - **Modelo:** {dados_trafo['Modelo']}
        - **Data do Teste:** {dados_trafo['Data_Teste'].strftime('%d/%m/%Y')}
        - **Status Final:** {dados_trafo['Status_Aprovacao']}
        - **Eficiência:** {dados_trafo['Eficiencia_Percentual']:.2f}% (Mínimo aceitável: {METRICAS_CONFIG['eficiencia_minima']}%)
        - **Elevação de Temperatura:** {dados_trafo['Elevacao_Temperatura_C']:.1f}°C (Máximo aceitável: {METRICAS_CONFIG['temperatura_maxima']}°C)
        - **Perdas Totais:** {dados_trafo['Perdas_Totais_kW']:.2f} kW (Máximo aceitável: {METRICAS_CONFIG['perdas_maximas']} kW)
        - **Potência Nominal:** {dados_trafo['Potencia_Nominal_MVA']} MVA

        **Instruções:**
        Com base nos dados acima, gere um relatório com as seguintes seções (use Markdown):

        **1. Diagnóstico Geral:**
           - Comece com uma avaliação conclusiva. O transformador está em condição operacional segura? O resultado do ensaio é preocupante?

        **2. Análise de Causa Raiz (Hipóteses):**
           - Se o status for 'Reprovado' ou se alguma métrica estiver fora do padrão, liste as possíveis causas técnicas. Seja específico.
           - Exemplo: Se a temperatura estiver alta, as causas podem ser 'problemas no sistema de refrigeração (radiadores obstruídos)', 'sobrecarga durante o ensaio' ou 'degradação do isolamento do núcleo'.
           - Se estiver 'Aprovado', mas perto dos limites, mencione isso como um ponto de atenção.

        **3. Riscos Potenciais:**
           - Descreva os riscos de operar um transformador com essas características se os problemas não forem corrigidos.
           - Exemplo: 'Risco de falha dielétrica prematura', 'redução da vida útil do equipamento', 'parada não programada', 'risco de incêndio em casos extremos'.

        **4. Recomendações de Ação:**
           - Forneça uma lista de ações claras e priorizadas para a equipe de engenharia ou manutenção.
           - Exemplo: '1. (Urgente) Inspecionar visualmente o sistema de refrigeração.', '2. (Recomendado) Realizar análise de gases dissolvidos (AGD) no óleo isolante.', '3. (Acompanhamento) Agendar novo ensaio de elevação de temperatura em 6 meses.'

        Seja técnico, preciso e use uma linguagem profissional, como um verdadeiro especialista da TSEA.
        """

        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"Erro ao contatar a IA: {e}")
            return "Não foi possível gerar o diagnóstico."

    def gerar_resumo_executivo(self) -> str:
        """
        Gera um resumo executivo dos dados filtrados.

        Returns:
            Uma string em Markdown com os principais insights.
        """
        if not self._checar_modelo():
            return ""

        if self.df.empty:
            return "Não há dados para gerar o resumo."

        # Para otimizar, enviamos apenas um resumo estatístico para a IA
        resumo_estatistico = self.df.describe(include='all')

        prompt = f"""
        Você é um analista de dados sênior da TSEA Energia. Sua tarefa é analisar um resumo estatístico dos resultados de testes de transformadores e escrever um "Resumo Executivo" (Executive Summary) para a gerência.

        **Resumo Estatístico dos Dados Analisados:**
        {resumo_estatistico.to_string()}

        **Instruções:**
        Com base nas estatísticas, escreva 3 a 5 bullets points destacando os insights mais importantes. Foque em:
        - **Tendências Gerais:** A performance geral é boa ou preocupante?
        - **Pontos de Atenção:** Quais modelos ou métricas se destacam (positiva ou negativamente)? Há alguma correlação implícita?
        - **Anomalias Notáveis:** Existem valores máximos ou mínimos que indicam problemas sérios?
        - **Recomendações Estratégicas:** Sugira uma direção para investigação. (Ex: "Recomenda-se uma análise aprofundada no 'Modelo X', que apresenta a maior taxa de reprovação.").

        Seja conciso, direto e foque em informações que gerem valor para a tomada de decisão.
        """
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"Erro ao contatar a IA: {e}")
            return "Não foi possível gerar o resumo."