"""
Módulo para geração e carregamento de dados
Este módulo contém funções para gerar dados fictícios e carregar dados reais
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional
import streamlit as st
from config import (
    DATA_CONFIG, MODELOS_TRANSFORMADORES, TIPOS_ENSAIO, 
    STATUS_APROVACAO, METRICAS_CONFIG
)


class DataGenerator:
    """Classe responsável pela geração e carregamento de dados"""
    
    def __init__(self):
        self.seed = DATA_CONFIG['seed_aleatoria']
        np.random.seed(self.seed)
    
    def gerar_dados_ficticios(self, num_registros: Optional[int] = None) -> pd.DataFrame:
        """
        Gera um DataFrame com dados fictícios de teste de transformadores
        
        Args:
            num_registros: Número de registros a serem gerados
            
        Returns:
            DataFrame com dados fictícios
        """
        if num_registros is None:
            num_registros = DATA_CONFIG['num_registros_ficticios']
        
        # Probabilidades para cada modelo (pode ser ajustado conforme necessário)
        prob_modelos = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]
        
        # Probabilidades para cada tipo de ensaio
        prob_ensaios = [0.50, 0.20, 0.15, 0.10, 0.05]
        
        # Probabilidades para aprovação/reprovação
        prob_aprovacao = [0.92, 0.08]  # 92% aprovação, 8% reprovação
        
        dados = {
            'ID_Transformador': [f'TR-{1000 + i:04d}' for i in range(num_registros)],
            'Modelo': np.random.choice(MODELOS_TRANSFORMADORES, num_registros, p=prob_modelos),
            'Data_Teste': self._gerar_datas_aleatorias(num_registros),
            'Tipo_Ensaio': np.random.choice(TIPOS_ENSAIO, num_registros, p=prob_ensaios),
            'Eficiencia_Percentual': self._gerar_eficiencia(num_registros),
            'Elevacao_Temperatura_C': self._gerar_temperatura(num_registros),
            'Perdas_Totais_kW': self._gerar_perdas(num_registros),
            'Status_Aprovacao': np.random.choice(STATUS_APROVACAO, num_registros, p=prob_aprovacao),
            'Tensao_Primaria_kV': self._gerar_tensao_primaria(num_registros),
            'Tensao_Secundaria_kV': self._gerar_tensao_secundaria(num_registros),
            'Potencia_Nominal_MVA': self._gerar_potencia_nominal(num_registros),
            'Corrente_Excitacao_A': self._gerar_corrente_excitacao(num_registros)
        }
        
        df = pd.DataFrame(dados)
        
        # Adiciona algumas correlações realistas
        df = self._adicionar_correlacoes(df)
        
        return df
    
    def _gerar_datas_aleatorias(self, num_registros: int) -> list:
        """Gera datas aleatórias nos últimos 2 anos"""
        data_inicio = datetime.now() - timedelta(days=730)
        data_fim = datetime.now()
        
        datas = []
        for _ in range(num_registros):
            dias_aleatorios = np.random.randint(0, (data_fim - data_inicio).days)
            data_aleatoria = data_inicio + timedelta(days=dias_aleatorios)
            datas.append(data_aleatoria)
        
        return datas
    
    def _gerar_eficiencia(self, num_registros: int) -> np.ndarray:
        """Gera valores de eficiência com distribuição realística"""
        # Eficiência segue uma distribuição normal truncada
        eficiencia = np.random.normal(99.2, 0.3, num_registros)
        eficiencia = np.clip(eficiencia, 98.0, 99.9)
        return np.round(eficiencia, 2)
    
    def _gerar_temperatura(self, num_registros: int) -> np.ndarray:
        """Gera valores de elevação de temperatura"""
        temperatura = np.random.normal(55, 5, num_registros)
        temperatura = np.clip(temperatura, 40, 70)
        return np.round(temperatura, 1)
    
    def _gerar_perdas(self, num_registros: int) -> np.ndarray:
        """Gera valores de perdas totais"""
        perdas = np.random.lognormal(2.5, 0.4, num_registros)
        perdas = np.clip(perdas, 3, 35)
        return np.round(perdas, 2)
    
    def _gerar_tensao_primaria(self, num_registros: int) -> np.ndarray:
        """Gera valores de tensão primária"""
        tensoes_padrao = [13.8, 23.0, 34.5, 69.0, 138.0, 230.0]
        return np.random.choice(tensoes_padrao, num_registros)
    
    def _gerar_tensao_secundaria(self, num_registros: int) -> np.ndarray:
        """Gera valores de tensão secundária"""
        tensoes_padrao = [0.38, 0.48, 4.16, 13.8, 23.0, 34.5]
        return np.random.choice(tensoes_padrao, num_registros)
    
    def _gerar_potencia_nominal(self, num_registros: int) -> np.ndarray:
        """Gera valores de potência nominal"""
        potencias_padrao = [0.5, 1.0, 2.5, 5.0, 10.0, 15.0, 25.0, 50.0]
        return np.random.choice(potencias_padrao, num_registros)
    
    def _gerar_corrente_excitacao(self, num_registros: int) -> np.ndarray:
        """Gera valores de corrente de excitação"""
        corrente = np.random.uniform(0.5, 3.0, num_registros)
        return np.round(corrente, 2)
    
    def _adicionar_correlacoes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adiciona correlações realísticas entre variáveis"""
        # Transformadores com maior potência tendem a ter mais perdas
        mask_alta_potencia = df['Potencia_Nominal_MVA'] > 10
        df.loc[mask_alta_potencia, 'Perdas_Totais_kW'] *= 1.5
        
        # Transformadores com mais perdas tendem a ter maior elevação de temperatura
        correlacao_temp = df['Perdas_Totais_kW'] * 0.8 + np.random.normal(0, 2, len(df))
        df['Elevacao_Temperatura_C'] = np.clip(
            df['Elevacao_Temperatura_C'] + correlacao_temp, 40, 70
        )
        
        # Transformadores com temperatura muito alta são reprovados
        mask_temp_alta = df['Elevacao_Temperatura_C'] > METRICAS_CONFIG['temperatura_maxima']
        df.loc[mask_temp_alta, 'Status_Aprovacao'] = 'Reprovado'
        
        # Transformadores com eficiência muito baixa são reprovados
        mask_efic_baixa = df['Eficiencia_Percentual'] < METRICAS_CONFIG['eficiencia_minima']
        df.loc[mask_efic_baixa, 'Status_Aprovacao'] = 'Reprovado'
        
        return df
    
    def carregar_dados_excel(self, caminho_arquivo: str) -> pd.DataFrame:
        """
        Carrega dados de um arquivo Excel
        
        Args:
            caminho_arquivo: Caminho para o arquivo Excel
            
        Returns:
            DataFrame com os dados carregados
        """
        try:
            df = pd.read_excel(caminho_arquivo)
            df['Data_Teste'] = pd.to_datetime(df['Data_Teste'])
            return df
        except Exception as e:
            st.error(f"Erro ao carregar arquivo Excel: {str(e)}")
            return pd.DataFrame()
    
    def carregar_dados_csv(self, caminho_arquivo: str) -> pd.DataFrame:
        """
        Carrega dados de um arquivo CSV
        
        Args:
            caminho_arquivo: Caminho para o arquivo CSV
            
        Returns:
            DataFrame com os dados carregados
        """
        try:
            df = pd.read_csv(caminho_arquivo)
            df['Data_Teste'] = pd.to_datetime(df['Data_Teste'])
            return df
        except Exception as e:
            st.error(f"Erro ao carregar arquivo CSV: {str(e)}")
            return pd.DataFrame()


@st.cache_data
def obter_dados(fonte: str = 'ficticios', caminho_arquivo: str = None) -> pd.DataFrame:
    """
    Função principal para obter dados (com cache do Streamlit)
    
    Args:
        fonte: 'ficticios', 'excel' ou 'csv'
        caminho_arquivo: Caminho para o arquivo (se fonte não for 'ficticios')
        
    Returns:
        DataFrame com os dados
    """
    generator = DataGenerator()
    
    if fonte == 'ficticios':
        df = generator.gerar_dados_ficticios()
    elif fonte == 'excel' and caminho_arquivo:
        df = generator.carregar_dados_excel(caminho_arquivo)
    elif fonte == 'csv' and caminho_arquivo:
        df = generator.carregar_dados_csv(caminho_arquivo)
    else:
        st.error("Fonte de dados inválida ou arquivo não especificado")
        return pd.DataFrame()
    
    # Garante que a coluna de data está no formato correto
    if not df.empty and 'Data_Teste' in df.columns:
        df['Data_Teste'] = pd.to_datetime(df['Data_Teste'])
    
    return df

