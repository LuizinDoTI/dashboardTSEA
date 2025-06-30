"""
Arquivo de configuração para o Dashboard TSEA
Este arquivo contém todas as configurações que podem ser facilmente modificadas
"""

# Configurações da aplicação
APP_CONFIG = {
    'page_title': 'Dashboard de Testes | TSEA Energia',
    'page_icon': '⚡',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Configurações dos dados
DATA_CONFIG = {
    'num_registros_ficticios': 500,  # Número de registros para dados fictícios
    'seed_aleatoria': 42,  # Semente para reprodutibilidade
    'formato_data': 'DD/MM/YYYY'
}

# Modelos de transformadores disponíveis
MODELOS_TRANSFORMADORES = [
    'TSEA-1000', 
    'TSEA-2500', 
    'TSEA-5000', 
    'TSEA-SPECIAL',
    'TSEA-7500',  # Novo modelo adicionado
    'TSEA-10000'  # Novo modelo adicionado
]

# Tipos de ensaio disponíveis
TIPOS_ENSAIO = [
    'Ensaio de Rotina',
    'Ensaio de Tipo', 
    'Ensaio Especial',
    'Ensaio de Aceitação',  # Novo tipo adicionado
    'Ensaio de Comissionamento'  # Novo tipo adicionado
]

# Status de aprovação
STATUS_APROVACAO = ['Aprovado', 'Reprovado']

# Configurações dos gráficos
GRAFICOS_CONFIG = {
    'altura_padrao': 400,
    'cores_personalizadas': [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', 
        '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'
    ],
    'template': 'plotly_white'
}

# Configurações das métricas (KPIs)
METRICAS_CONFIG = {
    'eficiencia_minima': 98.0,  # Eficiência mínima aceitável (%)
    'temperatura_maxima': 65.0,  # Temperatura máxima aceitável (°C)
    'perdas_maximas': 30.0  # Perdas máximas aceitáveis (kW)
}

# Configurações de exportação
EXPORT_CONFIG = {
    'nome_arquivo_csv': 'dados_filtrados_tsea.csv',
    'nome_arquivo_excel': 'dados_filtrados_tsea.xlsx',
    'encoding': 'utf-8'
}

# Textos da interface (facilita tradução futura)
TEXTOS_INTERFACE = {
    'titulo_principal': '⚡ Dashboard de Análise de Testes de Transformadores',
    'subtitulo': 'Use os filtros na barra lateral para analisar os resultados dos ensaios de produção.',
    'filtros_titulo': 'Filtros Interativos',
    'metricas_titulo': 'Métricas Gerais do Período Selecionado',
    'graficos_titulo': 'Visualizações Gráficas',
    'dados_titulo': 'Dados Detalhados dos Testes',
    'sem_dados': 'Nenhum dado encontrado para os filtros selecionados.',
    'botao_download_csv': '📥 Baixar dados como CSV',
    'botao_download_excel': '📊 Baixar dados como Excel'
}

