"""
Módulo para cálculo e exibição de métricas (KPIs)
Este módulo contém todas as funções para calcular e exibir métricas do dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any
from config import METRICAS_CONFIG, TEXTOS_INTERFACE


class DashboardMetrics:
    """Classe responsável pelo cálculo e exibição de métricas"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.metricas = {}
    
    def calcular_metricas_basicas(self) -> Dict[str, Any]:
        """
        Calcula métricas básicas do dashboard
        
        Returns:
            Dicionário com as métricas calculadas
        """
        if self.df.empty:
            return {
                'total_testes': 0,
                'eficiencia_media': 0,
                'taxa_aprovacao': 0,
                'temperatura_media': 0,
                'perdas_medias': 0
            }
        
        metricas = {
            'total_testes': len(self.df),
            'eficiencia_media': self.df['Eficiencia_Percentual'].mean(),
            'taxa_aprovacao': (self.df['Status_Aprovacao'].value_counts(normalize=True).get('Aprovado', 0)) * 100,
            'temperatura_media': self.df['Elevacao_Temperatura_C'].mean(),
            'perdas_medias': self.df['Perdas_Totais_kW'].mean()
        }
        
        # Métricas adicionais se as colunas existirem
        if 'Potencia_Nominal_MVA' in self.df.columns:
            metricas['potencia_media'] = self.df['Potencia_Nominal_MVA'].mean()
        
        if 'Corrente_Excitacao_A' in self.df.columns:
            metricas['corrente_media'] = self.df['Corrente_Excitacao_A'].mean()
        
        self.metricas = metricas
        return metricas
    
    def calcular_metricas_avancadas(self) -> Dict[str, Any]:
        """
        Calcula métricas avançadas e estatísticas
        
        Returns:
            Dicionário com métricas avançadas
        """
        if self.df.empty:
            return {}
        
        metricas_avancadas = {
            # Estatísticas de eficiência
            'eficiencia_std': self.df['Eficiencia_Percentual'].std(),
            'eficiencia_min': self.df['Eficiencia_Percentual'].min(),
            'eficiencia_max': self.df['Eficiencia_Percentual'].max(),
            'eficiencia_q25': self.df['Eficiencia_Percentual'].quantile(0.25),
            'eficiencia_q75': self.df['Eficiencia_Percentual'].quantile(0.75),
            
            # Estatísticas de temperatura
            'temperatura_std': self.df['Elevacao_Temperatura_C'].std(),
            'temperatura_min': self.df['Elevacao_Temperatura_C'].min(),
            'temperatura_max': self.df['Elevacao_Temperatura_C'].max(),
            
            # Estatísticas de perdas
            'perdas_std': self.df['Perdas_Totais_kW'].std(),
            'perdas_min': self.df['Perdas_Totais_kW'].min(),
            'perdas_max': self.df['Perdas_Totais_kW'].max(),
            
            # Contagens por categoria
            'testes_por_modelo': self.df['Modelo'].value_counts().to_dict(),
            'testes_por_tipo': self.df['Tipo_Ensaio'].value_counts().to_dict(),
            
            # Métricas de qualidade
            'testes_fora_spec_temp': len(self.df[self.df['Elevacao_Temperatura_C'] > METRICAS_CONFIG['temperatura_maxima']]),
            'testes_fora_spec_efic': len(self.df[self.df['Eficiencia_Percentual'] < METRICAS_CONFIG['eficiencia_minima']]),
            'testes_fora_spec_perdas': len(self.df[self.df['Perdas_Totais_kW'] > METRICAS_CONFIG['perdas_maximas']])
        }
        
        return metricas_avancadas
    
    def card_metric(self, titulo, valor, variacao=None, cor_fundo="#222", cor_borda="#1ecb4f", icone="", cor_texto="#fff", sufixo_variacao="", help_text=None):
        """Exibe um card de métrica customizado"""
        st.markdown(
            f'''
            <div style="background: {cor_fundo}; border-left: 8px solid {cor_borda}; border-radius: 18px; box-shadow: 0 4px 16px rgba(0,0,0,0.12); padding: 24px 18px 18px 18px; margin-bottom: 18px; min-height: 140px; color: {cor_texto}; position: relative;">
                <div style="font-size: 2.2rem; position: absolute; top: 18px; right: 24px;">{icone}</div>
                <div style="font-size: 1.1rem; font-weight: 600; opacity: 0.85;">{titulo}</div>
                <div style="font-size: 2.8rem; font-weight: bold; margin: 8px 0;">{valor}</div>
                {f'<div style="font-size: 1.1rem; font-weight: 500; color: {"#1ecb4f" if variacao and variacao.startswith("+") else "#ff4b4b"};">{"▲" if variacao and variacao.startswith("+") else ("▼" if variacao else "")}{variacao if variacao else ""}{sufixo_variacao}</div>' if variacao else ''}
            </div>
            ''',
            unsafe_allow_html=True
        )
        if help_text:
            st.caption(help_text)

    def exibir_metricas_principais(self):
        """Exibe as métricas principais em colunas com cards customizados"""
        metricas = self.calcular_metricas_basicas()
        st.header(TEXTOS_INTERFACE['metricas_titulo'])
        # Primeira linha de métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            self.card_metric(
                "📊 Total de Testes",
                f"{metricas['total_testes']:,}",
                cor_fundo="#23272e",
                cor_borda="#6c63ff",
                icone="📊",
                help_text="Número total de testes realizados no período selecionado"
            )
        with col2:
            eficiencia = metricas['eficiencia_media']
            delta_eficiencia = eficiencia - METRICAS_CONFIG['eficiencia_minima']
            self.card_metric(
                "⚡ Eficiência Média",
                f"{eficiencia:.2f}%",
                variacao=f"{delta_eficiencia:+.2f}",
                sufixo_variacao="%",
                cor_fundo="#1ecb4f22",
                cor_borda="#1ecb4f",
                icone="⚡",
                help_text=f"Eficiência média dos transformadores (mínimo: {METRICAS_CONFIG['eficiencia_minima']}%)"
            )
        with col3:
            taxa_aprovacao = metricas['taxa_aprovacao']
            delta_aprov = taxa_aprovacao - 90
            self.card_metric(
                "✅ Taxa de Aprovação",
                f"{taxa_aprovacao:.1f}%",
                variacao=f"{delta_aprov:+.1f}",
                sufixo_variacao="%",
                cor_fundo="#1e90ff22",
                cor_borda="#1e90ff",
                icone="✅",
                help_text="Percentual de testes aprovados (meta: 90%)"
            )
        with col4:
            temperatura = metricas['temperatura_media']
            delta_temp = METRICAS_CONFIG['temperatura_maxima'] - temperatura
            self.card_metric(
                "🌡️ Temperatura Média",
                f"{temperatura:.1f}°C",
                variacao=f"{delta_temp:+.1f}",
                sufixo_variacao="°C",
                cor_fundo="#ff4b4b22",
                cor_borda="#ff4b4b",
                icone="🌡️",
                help_text=f"Elevação média de temperatura (máximo: {METRICAS_CONFIG['temperatura_maxima']}°C)"
            )
        # Segunda linha de métricas
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            perdas = metricas['perdas_medias']
            self.card_metric(
                "⚠️ Perdas Médias",
                f"{perdas:.2f} kW",
                cor_fundo="#f7b73122",
                cor_borda="#f7b731",
                icone="⚠️",
                help_text="Perdas totais médias dos transformadores"
            )
        with col6:
            if 'potencia_media' in metricas:
                self.card_metric(
                    "🔌 Potência Média",
                    f"{metricas['potencia_media']:.1f} MVA",
                    cor_fundo="#00b89422",
                    cor_borda="#00b894",
                    icone="🔌",
                    help_text="Potência nominal média dos transformadores testados"
                )
        with col7:
            if 'corrente_media' in metricas:
                self.card_metric(
                    "🔄 Corrente Média",
                    f"{metricas['corrente_media']:.2f} A",
                    cor_fundo="#0984e322",
                    cor_borda="#0984e3",
                    icone="🔄",
                    help_text="Corrente de excitação média"
                )
        with col8:
            metricas_avancadas = self.calcular_metricas_avancadas()
            total_fora_spec = (
                metricas_avancadas.get('testes_fora_spec_temp', 0) +
                metricas_avancadas.get('testes_fora_spec_efic', 0) +
                metricas_avancadas.get('testes_fora_spec_perdas', 0)
            )
            conformidade = ((metricas['total_testes'] - total_fora_spec) / max(metricas['total_testes'], 1)) * 100
            delta_conformidade = conformidade - 95
            self.card_metric(
                "📋 Conformidade",
                f"{conformidade:.1f}%",
                variacao=f"{delta_conformidade:+.1f}",
                sufixo_variacao="%",
                cor_fundo="#a29bfe22",
                cor_borda="#a29bfe",
                icone="📋",
                help_text="Percentual de testes dentro das especificações (meta: 95%)"
            )
    
    def exibir_metricas_detalhadas(self):
        """Exibe métricas detalhadas em um expander com balões coloridos customizados"""
        with st.expander("📈 Métricas Detalhadas", expanded=False):
            metricas_avancadas = self.calcular_metricas_avancadas()
            if not metricas_avancadas:
                st.warning("Nenhum dado disponível para métricas detalhadas")
                return

            # Estatísticas de eficiência
            st.subheader("⚡ Estatísticas de Eficiência")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                self.card_metric(
                    "Mínima",
                    f"{metricas_avancadas['eficiencia_min']:.2f}%",
                    cor_fundo="#e0f7fa",
                    cor_borda="#00b894",
                    icone="⚡",
                    cor_texto="#222"
                )
            with col2:
                self.card_metric(
                    "Máxima",
                    f"{metricas_avancadas['eficiencia_max']:.2f}%",
                    cor_fundo="#d0f2ff",
                    cor_borda="#0984e3",
                    icone="⚡",
                    cor_texto="#222"
                )
            with col3:
                self.card_metric(
                    "Q1 (25%)",
                    f"{metricas_avancadas['eficiencia_q25']:.2f}%",
                    cor_fundo="#eafaf1",
                    cor_borda="#1ecb4f",
                    icone="⚡",
                    cor_texto="#222"
                )
            with col4:
                self.card_metric(
                    "Q3 (75%)",
                    f"{metricas_avancadas['eficiencia_q75']:.2f}%",
                    cor_fundo="#e3e0fa",
                    cor_borda="#6c63ff",
                    icone="⚡",
                    cor_texto="#222"
                )

            # Estatísticas de temperatura
            st.subheader("🌡️ Estatísticas de Temperatura")
            col1, col2, col3 = st.columns(3)
            with col1:
                self.card_metric(
                    "Mínima",
                    f"{metricas_avancadas['temperatura_min']:.1f}°C",
                    cor_fundo="#ffe0e0",
                    cor_borda="#ff4b4b",
                    icone="🌡️",
                    cor_texto="#222"
                )
            with col2:
                self.card_metric(
                    "Máxima",
                    f"{metricas_avancadas['temperatura_max']:.1f}°C",
                    cor_fundo="#fff3e0",
                    cor_borda="#f7b731",
                    icone="🌡️",
                    cor_texto="#222"
                )
            with col3:
                self.card_metric(
                    "Desvio Padrão",
                    f"{metricas_avancadas['temperatura_std']:.1f}°C",
                    cor_fundo="#ffe0fa",
                    cor_borda="#a29bfe",
                    icone="🌡️",
                    cor_texto="#222"
                )

            # Testes fora de especificação
            st.subheader("⚠️ Testes Fora de Especificação")
            col1, col2, col3 = st.columns(3)
            with col1:
                self.card_metric(
                    "Temperatura Alta",
                    metricas_avancadas['testes_fora_spec_temp'],
                    cor_fundo="#fffbe0",
                    cor_borda="#f7b731",
                    icone="⚠️",
                    cor_texto="#222",
                    help_text=f"Testes com temperatura > {METRICAS_CONFIG['temperatura_maxima']}°C"
                )
            with col2:
                self.card_metric(
                    "Eficiência Baixa",
                    metricas_avancadas['testes_fora_spec_efic'],
                    cor_fundo="#e0f7fa",
                    cor_borda="#00b894",
                    icone="⚠️",
                    cor_texto="#222",
                    help_text=f"Testes com eficiência < {METRICAS_CONFIG['eficiencia_minima']}%"
                )
            with col3:
                self.card_metric(
                    "Perdas Altas",
                    metricas_avancadas['testes_fora_spec_perdas'],
                    cor_fundo="#ffe0e0",
                    cor_borda="#ff4b4b",
                    icone="⚠️",
                    cor_texto="#222",
                    help_text=f"Testes com perdas > {METRICAS_CONFIG['perdas_maximas']} kW"
                )
    
    def gerar_relatorio_resumo(self) -> str:
        """
        Gera um relatório resumo em texto
        
        Returns:
            String com o relatório resumo
        """
        metricas = self.calcular_metricas_basicas()
        metricas_avancadas = self.calcular_metricas_avancadas()
        
        if not metricas or metricas['total_testes'] == 0:
            return "Nenhum dado disponível para gerar relatório."
        
        relatorio = f"""
        ## Relatório Resumo - Dashboard TSEA
        
        ### Métricas Gerais
        - **Total de Testes:** {metricas['total_testes']:,}
        - **Eficiência Média:** {metricas['eficiencia_media']:.2f}%
        - **Taxa de Aprovação:** {metricas['taxa_aprovacao']:.1f}%
        - **Temperatura Média:** {metricas['temperatura_media']:.1f}°C
        - **Perdas Médias:** {metricas['perdas_medias']:.2f} kW
        
        ### Análise de Qualidade
        - **Testes fora de especificação (Temperatura):** {metricas_avancadas.get('testes_fora_spec_temp', 0)}
        - **Testes fora de especificação (Eficiência):** {metricas_avancadas.get('testes_fora_spec_efic', 0)}
        - **Testes fora de especificação (Perdas):** {metricas_avancadas.get('testes_fora_spec_perdas', 0)}
        
        ### Distribuição por Modelo
        """
        
        # Adiciona distribuição por modelo
        for modelo, quantidade in metricas_avancadas.get('testes_por_modelo', {}).items():
            percentual = (quantidade / metricas['total_testes']) * 100
            relatorio += f"- **{modelo}:** {quantidade} testes ({percentual:.1f}%)\n"
        
        return relatorio
    
    def comparar_periodos(self, df_anterior: pd.DataFrame) -> Dict[str, float]:
        """
        Compara métricas com período anterior
        
        Args:
            df_anterior: DataFrame do período anterior
            
        Returns:
            Dicionário com as variações percentuais
        """
        if df_anterior.empty:
            return {}
        
        metricas_atual = self.calcular_metricas_basicas()
        metricas_anterior = DashboardMetrics(df_anterior).calcular_metricas_basicas()
        
        comparacao = {}
        
        for metrica in ['total_testes', 'eficiencia_media', 'taxa_aprovacao', 'temperatura_media', 'perdas_medias']:
            if metricas_anterior.get(metrica, 0) != 0:
                variacao = ((metricas_atual[metrica] - metricas_anterior[metrica]) / metricas_anterior[metrica]) * 100
                comparacao[f'{metrica}_variacao'] = variacao
        
        return comparacao


def calcular_kpis_personalizados(df: pd.DataFrame, configuracao: Dict[str, Any]) -> Dict[str, float]:
    """
    Calcula KPIs personalizados baseados em configuração do usuário
    
    Args:
        df: DataFrame com os dados
        configuracao: Dicionário com configuração dos KPIs
        
    Returns:
        Dicionário com os KPIs calculados
    """
    kpis = {}
    
    if df.empty:
        return kpis
    
    # KPI de eficiência por faixa
    if configuracao.get('eficiencia_faixas'):
        for faixa, (min_val, max_val) in configuracao['eficiencia_faixas'].items():
            mask = (df['Eficiencia_Percentual'] >= min_val) & (df['Eficiencia_Percentual'] < max_val)
            kpis[f'eficiencia_{faixa}'] = len(df[mask])
    
    # KPI de conformidade por modelo
    if configuracao.get('conformidade_por_modelo'):
        for modelo in df['Modelo'].unique():
            df_modelo = df[df['Modelo'] == modelo]
            aprovados = len(df_modelo[df_modelo['Status_Aprovacao'] == 'Aprovado'])
            total = len(df_modelo)
            kpis[f'conformidade_{modelo}'] = (aprovados / total * 100) if total > 0 else 0
    
    return kpis

