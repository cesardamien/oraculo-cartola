"""
💎 ORÁCULO WAR ROOM V9.0 - CARTOLA FC
Versão Final Corrigida - 100% Funcional
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime
from pathlib import Path
import time

st.set_page_config(
    page_title="Oráculo War Room V9.0",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# CONSTANTES
# ==============================================================================

POSICOES = {
    1: "Goleiro",
    2: "Lateral", 
    3: "Zagueiro",
    4: "Meia",
    5: "Atacante",
    6: "Técnico"
}

STATUS = {
    7: ("Provável", "success"),
    6: ("Dúvida", "warning"),
    5: ("Lesionado", "error"),
    3: ("Suspenso", "error"),
    2: ("Nulo", "error")
}

FORMACOES = {
    "3-4-3": {"zagueiros": 3, "laterais": 0, "meias": 4, "atacantes": 3},
    "3-5-2": {"zagueiros": 3, "laterais": 0, "meias": 5, "atacantes": 2},
    "4-3-3": {"zagueiros": 2, "laterais": 2, "meias": 3, "atacantes": 3},
    "4-4-2": {"zagueiros": 2, "laterais": 2, "meias": 4, "atacantes": 2},
    "4-5-1": {"zagueiros": 2, "laterais": 2, "meias": 5, "atacantes": 1},
    "5-3-2": {"zagueiros": 3, "laterais": 2, "meias": 3, "atacantes": 2},
    "5-4-1": {"zagueiros": 3, "laterais": 2, "meias": 4, "atacantes": 1}
}
def load_css():
    """CSS Profissional"""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

        * {
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        .main-header {
            background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%);
            border: 2px solid #58a6ff;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(88, 166, 255, 0.15);
        }

        .main-title {
            font-size: 42px;
            font-weight: 900;
            background: linear-gradient(135deg, #58a6ff 0%, #bc4bff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        .main-subtitle {
            color: #8b949e;
            font-size: 14px;
            letter-spacing: 1px;
        }

        .team-header {
            background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%);
            border: 2px solid #ffd700;
            border-radius: 16px;
            padding: 25px;
            margin-bottom: 25px;
            text-align: center;
        }

        .team-name {
            font-size: 28px;
            font-weight: 900;
            color: #ffd700;
            margin-bottom: 8px;
        }

        .team-info {
            color: #8b949e;
            font-size: 14px;
        }

        .timer-box {
            background: linear-gradient(135deg, #2d1b1e 0%, #1a0f11 100%);
            border: 2px solid #da3633;
            color: #da3633;
            text-align: center;
            padding: 20px;
            font-weight: 900;
            font-size: 24px;
            border-radius: 12px;
            margin-bottom: 25px;
        }

        /* CAMPO DE FUTEBOL */
        .campo-futebol {
            background: linear-gradient(180deg, #1a5c3a 0%, #0d3d24 100%);
            border-radius: 20px;
            padding: 40px 20px;
            margin: 25px 0;
            position: relative;
            min-height: 600px;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.4);
        }

        .campo-futebol::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 5%;
            right: 5%;
            height: 2px;
            background: rgba(255,255,255,0.3);
            transform: translateY(-50%);
        }

        .campo-futebol::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 100px;
            height: 100px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            transform: translate(-50%, -50%);
        }

        .linha-jogadores {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            margin: 30px 0;
            position: relative;
            z-index: 2;
            flex-wrap: wrap;
        }

        .jogador {
            background: rgba(0, 0, 0, 0.6);
            border: 3px solid #2ea043;
            border-radius: 12px;
            padding: 12px;
            text-align: center;
            min-width: 110px;
            max-width: 130px;
            backdrop-filter: blur(10px);
            transition: all 0.3s;
        }

        .jogador.capitao {
            border-color: #ffd700;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
        }

        .jogador:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 8px 20px rgba(46, 160, 67, 0.4);
        }

        .jogador img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: 3px solid #2ea043;
            margin-bottom: 8px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }

        .jogador.capitao img {
            border-color: #ffd700;
        }

        .jogador-nome {
            font-size: 13px;
            font-weight: 700;
            color: white;
            margin-bottom: 4px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        }

        .jogador-stats {
            font-size: 11px;
            color: #2ea043;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .jogador.capitao .jogador-stats {
            color: #ffd700;
        }

        .jogador-preco {
            font-size: 10px;
            color: rgba(255,255,255,0.7);
        }

        .jogador-capitao {
            font-size: 11px;
            color: #ffd700;
            font-weight: 900;
            margin-top: 6px;
        }

        /* PLAYER CARDS */
        .player-card {
            background: linear-gradient(135deg, #161b22 0%, #1a1f2e 100%);
            border: 2px solid #30363d;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            transition: all 0.3s;
        }

        .player-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(88, 166, 255, 0.2);
        }

        .player-card.excellent { border-color: #2ea043; }
        .player-card.good { border-color: #58a6ff; }
        .player-card.warning { border-color: #d29922; }
        .player-card.danger { border-color: #da3633; }

        .player-img {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 3px solid #30363d;
            margin: 0 auto 15px;
            display: block;
        }

        .player-name {
            font-size: 18px;
            font-weight: 700;
            color: #c9d1d9;
            text-align: center;
            margin-bottom: 8px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin: 12px 0;
        }

        .stat-item {
            background: rgba(255,255,255,0.03);
            padding: 8px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-label {
            font-size: 9px;
            color: #8b949e;
            text-transform: uppercase;
            margin-bottom: 4px;
        }

        .stat-value {
            font-size: 15px;
            font-weight: 700;
            color: #c9d1d9;
        }

        .stat-value.price { color: #2ea043; }
        .stat-value.prediction { color: #bc4bff; }

        .player-score-bar {
            height: 6px;
            background: #21262d;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 12px;
        }

        .player-score-fill {
            height: 100%;
            background: linear-gradient(90deg, #58a6ff, #bc4bff);
            transition: width 0.5s ease;
        }

        .metric-box {
            background: rgba(188, 75, 255, 0.1);
            border: 2px solid #bc4bff;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }

        .metric-value {
            font-size: 48px;
            font-weight: 900;
        }
    </style>
    """, unsafe_allow_html=True)
# ==============================================================================
# FUNÇÕES DE API
# ==============================================================================

@st.cache_data(ttl=300)
def get_cartola_data(endpoint, params=None):
    """Busca dados da API do Cartola com validação"""
    url = f"https://api.cartola.globo.com/{endpoint}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data is None:
            return None

        return data

    except requests.exceptions.Timeout:
        st.error("⏱️ Timeout na API do Cartola FC")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Erro na API: {str(e)}")
        return None
    except json.JSONDecodeError:
        st.error("❌ Erro ao decodificar resposta da API")
        return None

def buscar_time_usuario(identificador):
    """Busca time do usuário por nome ou slug"""
    if not identificador or len(identificador.strip()) < 3:
        return None

    identificador = identificador.strip()

    try:
        search_results = get_cartola_data("times", params={"q": identificador})

        if search_results and isinstance(search_results, list) and len(search_results) > 0:
            primeiro = search_results[0]
            time_id = primeiro.get('time_id')

            if time_id:
                time_completo = get_cartola_data(f"time/id/{time_id}")
                if time_completo:
                    return time_completo

        time_data = get_cartola_data(f"time/slug/{identificador}")
        if time_data and 'time' in time_data:
            return time_data

        return None

    except Exception as e:
        st.error(f"Erro ao buscar time: {str(e)}")
        return None

# ==============================================================================
# SISTEMA DE APRENDIZADO
# ==============================================================================

class SistemaAprendizado:
    """Sistema que aprende com resultados reais"""

    def __init__(self):
        self.arquivo = Path("historico_previsoes.json")
        self.historico = self._carregar()

    def _carregar(self):
        if self.arquivo.exists():
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self._criar_novo()
        return self._criar_novo()

    def _criar_novo(self):
        return {
            'previsoes': [],
            'fator_ajuste': 1.0,
            'versao': '9.0'
        }

    def _salvar(self):
        try:
            with open(self.arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.historico, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Erro ao salvar histórico: {str(e)}")

    def registrar(self, time_gerado, rodada):
        """Registra uma previsão"""
        previsao = {
            'rodada': int(rodada),
            'data': datetime.now().isoformat(),
            'formacao': time_gerado['formacao'],
            'previsao_total': float(time_gerado['previsao_com_capitao']),
            'custo_total': float(time_gerado['custo_total']),
            'capitao': {
                'atleta_id': int(time_gerado['capitao']['atleta_id']),
                'apelido': time_gerado['capitao']['apelido'],
                'previsao': float(time_gerado['capitao']['PREVISAO'])
            },
            'jogadores': [
                {
                    'atleta_id': int(p['atleta_id']),
                    'apelido': p['apelido'],
                    'posicao': POSICOES.get(p['posicao_id'], 'N/A'),
                    'previsao': float(p['PREVISAO']),
                    'preco': float(p['preco_num'])
                }
                for p in time_gerado['titulares']
            ],
            'pontos_reais': None,
            'conferido': False,
            'fator_usado': float(self.historico['fator_ajuste'])
        }

        self.historico['previsoes'].append(previsao)
        self._salvar()

        return len(self.historico['previsoes']) - 1

    def conferir(self, indice, pontos_reais):
        """Confere resultado e ajusta fator"""
        if indice >= len(self.historico['previsoes']):
            return None

        previsao = self.historico['previsoes'][indice]

        if previsao['conferido']:
            return {
                'erro': 'Previsão já foi conferida',
                'previsao': previsao['previsao_total'],
                'real': previsao['pontos_reais']
            }

        previsao['pontos_reais'] = float(pontos_reais)
        previsao['conferido'] = True
        previsao['data_conferencia'] = datetime.now().isoformat()

        erro = abs(previsao['previsao_total'] - pontos_reais)
        erro_percentual = (erro / previsao['previsao_total']) * 100 if previsao['previsao_total'] > 0 else 0

        fator_atual = self.historico['fator_ajuste']

        if erro_percentual > 25:
            novo_fator = fator_atual * 0.95
        elif erro_percentual > 15:
            novo_fator = fator_atual * 0.98
        elif erro_percentual < 5:
            novo_fator = fator_atual * 1.01
        elif erro_percentual < 10:
            novo_fator = fator_atual * 1.005
        else:
            novo_fator = fator_atual

        self.historico['fator_ajuste'] = max(0.6, min(1.3, novo_fator))

        self._salvar()

        return {
            'previsao': previsao['previsao_total'],
            'real': pontos_reais,
            'erro': erro,
            'erro_percentual': erro_percentual,
            'fator_anterior': fator_atual,
            'fator': self.historico['fator_ajuste'],
            'ajuste': 'reduzido' if novo_fator < fator_atual else 'aumentado' if novo_fator > fator_atual else 'mantido'
        }

    def get_fator(self):
        return self.historico['fator_ajuste']

    def get_estatisticas(self):
        conferidos = [p for p in self.historico['previsoes'] if p['conferido']]

        if not conferidos:
            return None

        erros = [abs(p['previsao_total'] - p['pontos_reais']) for p in conferidos]

        return {
            'total_previsoes': len(self.historico['previsoes']),
            'conferidas': len(conferidos),
            'erro_medio': np.mean(erros),
            'erro_minimo': min(erros),
            'erro_maximo': max(erros),
            'fator_ajuste': self.historico['fator_ajuste']
        }
# ==============================================================================
# ANALISADOR DE TIME
# ==============================================================================

class AnalisadorTime:
    """Analisa time do usuário"""

    def __init__(self, mercado_data, partidas_data):
        self.mercado = mercado_data
        self.partidas = partidas_data
        self.mandantes = self._get_mandantes()

    def _get_mandantes(self):
        mandantes = []
        if self.partidas:
            for p in self.partidas.get('partidas', []):
                mandantes.append(str(p.get('clube_casa_id', '')))
        return mandantes

    def calcular_previsao(self, atleta):
        """Calcula previsão de pontos"""
        media = float(atleta.get('media_num', 0))
        variacao = float(atleta.get('variacao_num', 0))
        jogos = int(atleta.get('jogos_num', 0))
        status = int(atleta.get('status_id', 0))

        if media == 0 or jogos < 2:
            return 0.0

        previsao = media

        if variacao > 0:
            previsao += min(variacao * 0.25, 1.5)
        elif variacao < 0:
            previsao += max(variacao * 0.15, -1.0)

        clube_id = str(atleta.get('clube_id', ''))
        if clube_id in self.mandantes:
            previsao *= 1.12
        else:
            previsao *= 0.96

        if status == 7:
            previsao *= 1.0
        elif status == 6:
            previsao *= 0.65
        else:
            previsao *= 0.25

        return max(0.0, previsao)

    def analisar_time_completo(self, atletas_time, capitao_id):
        """Analisa todos os atletas do time"""

        atletas_mercado = {str(a['atleta_id']): a for a in self.mercado.get('atletas', [])}

        analises = []
        alertas_criticos = []

        for atleta_time in atletas_time:
            atleta_id = str(atleta_time.get('atleta_id', ''))

            if atleta_id not in atletas_mercado:
                continue

            atleta_merc = atletas_mercado[atleta_id]

            analise = {
                'atleta_id': int(atleta_id),
                'apelido': atleta_merc.get('apelido', 'N/A'),
                'posicao': POSICOES.get(atleta_merc.get('posicao_id'), 'N/A'),
                'posicao_id': atleta_merc.get('posicao_id'),
                'clube': self.mercado.get('clubes', {}).get(str(atleta_merc.get('clube_id', '')), {}).get('nome', 'N/A'),
                'foto': str(atleta_merc.get('foto', '')).replace('FORMATO', '220x220'),
                'preco': float(atleta_merc.get('preco_num', 0)),
                'media': float(atleta_merc.get('media_num', 0)),
                'variacao': float(atleta_merc.get('variacao_num', 0)),
                'jogos': int(atleta_merc.get('jogos_num', 0)),
                'status_id': atleta_merc.get('status_id', 0),
                'status': STATUS.get(atleta_merc.get('status_id', 0), ('Desconhecido', 'error'))[0],
                'capitao': atleta_id == str(capitao_id),
                'previsao': 0.0,
                'score': 0,
                'problemas': [],
                'qualidades': [],
                'classificacao': 'warning'
            }

            analise['previsao'] = self.calcular_previsao(atleta_merc)

            score = 0
            problemas = []
            qualidades = []

            # Status (40 pontos)
            if analise['status_id'] == 7:
                score += 40
                qualidades.append("Provável para jogar")
            elif analise['status_id'] == 6:
                score += 20
                problemas.append("Status DÚVIDA")
                alertas_criticos.append({
                    'atleta': analise['apelido'],
                    'posicao': analise['posicao'],
                    'motivo': 'Status: DÚVIDA',
                    'gravidade': 'warning'
                })
            else:
                score += 0
                problemas.append(f"Status: {analise['status']}")
                alertas_criticos.append({
                    'atleta': analise['apelido'],
                    'posicao': analise['posicao'],
                    'motivo': f"Status: {analise['status']} - SUBSTITUIR",
                    'gravidade': 'error'
                })

            # Média (30 pontos)
            if analise['media'] >= 7:
                score += 30
                qualidades.append(f"Média excelente ({analise['media']:.2f})")
            elif analise['media'] >= 5:
                score += 20
                qualidades.append(f"Média boa ({analise['media']:.2f})")
            elif analise['media'] >= 3:
                score += 10
                problemas.append(f"Média baixa ({analise['media']:.2f})")
            else:
                score += 0
                problemas.append(f"Média muito baixa ({analise['media']:.2f})")

            # Variação (20 pontos)
            if analise['variacao'] > 2:
                score += 20
                qualidades.append(f"Em alta (+{analise['variacao']:.1f})")
            elif analise['variacao'] > 0:
                score += 15
            elif analise['variacao'] > -2:
                score += 10
            else:
                score += 0
                problemas.append(f"Em queda ({analise['variacao']:.1f})")

            # Jogos (10 pontos)
            if analise['jogos'] >= 5:
                score += 10
            elif analise['jogos'] >= 3:
                score += 5
            else:
                problemas.append(f"Poucos jogos ({analise['jogos']})")

            analise['score'] = min(100, score)
            analise['problemas'] = problemas
            analise['qualidades'] = qualidades

            if analise['score'] >= 75:
                analise['classificacao'] = 'excellent'
                analise['label'] = 'EXCELENTE'
            elif analise['score'] >= 55:
                analise['classificacao'] = 'good'
                analise['label'] = 'BOM'
            elif analise['score'] >= 35:
                analise['classificacao'] = 'warning'
                analise['label'] = 'ATENÇÃO'
            else:
                analise['classificacao'] = 'danger'
                analise['label'] = 'CRÍTICO'

            analises.append(analise)

        score_geral = np.mean([a['score'] for a in analises]) if analises else 0

        previsao_total = sum([
            a['previsao'] * (2 if a['capitao'] else 1)
            for a in analises
        ])

        return {
            'analises': analises,
            'score_geral': score_geral,
            'previsao_total': previsao_total,
            'alertas_criticos': alertas_criticos,
            'total_atletas': len(analises),
            'provaveis': len([a for a in analises if a['status_id'] == 7]),
            'duvidas': len([a for a in analises if a['status_id'] == 6]),
            'nao_provaveis': len([a for a in analises if a['status_id'] not in [6, 7]]),
            'media_geral': np.mean([a['media'] for a in analises]) if analises else 0
        }

# ==============================================================================
# GERADOR DE TIMES
# ==============================================================================

class GeradorTimesIA:
    """Gerador inteligente de times"""

    def __init__(self, mercado_data, partidas_data, patrimonio, sistema):
        self.mercado = mercado_data
        self.partidas = partidas_data
        self.patrimonio = float(patrimonio) if patrimonio else 100.0
        self.sistema = sistema

        if 'atletas' in mercado_data:
            self.atletas = pd.DataFrame(mercado_data['atletas'])
            self.atletas = self.atletas[self.atletas['atleta_id'].notna()]
            self.atletas['preco_num'] = pd.to_numeric(self.atletas['preco_num'], errors='coerce').fillna(0)
            self.atletas['media_num'] = pd.to_numeric(self.atletas['media_num'], errors='coerce').fillna(0)
            self.atletas['variacao_num'] = pd.to_numeric(self.atletas['variacao_num'], errors='coerce').fillna(0)
            self.atletas['jogos_num'] = pd.to_numeric(self.atletas['jogos_num'], errors='coerce').fillna(0)
        else:
            self.atletas = pd.DataFrame()

        self.clubes = mercado_data.get('clubes', {})
        self.mandantes = self._get_mandantes()

    def _get_mandantes(self):
        mandantes = []
        if self.partidas:
            for p in self.partidas.get('partidas', []):
                mandantes.append(str(p.get('clube_casa_id', '')))
        return mandantes

    def calcular_previsao(self, atleta):
        """Calcula previsão"""
        media = float(atleta.get('media_num', 0))
        variacao = float(atleta.get('variacao_num', 0))
        jogos = int(atleta.get('jogos_num', 0))
        status = int(atleta.get('status_id', 0))

        if media == 0 or jogos < 2:
            return 0.0

        previsao = media

        if variacao > 0:
            previsao += min(variacao * 0.25, 1.5)
        elif variacao < 0:
            previsao += max(variacao * 0.15, -1.0)

        clube_id = str(atleta.get('clube_id', ''))
        if clube_id in self.mandantes:
            previsao *= 1.12
        else:
            previsao *= 0.96

        if status == 7:
            previsao *= 1.0
        elif status == 6:
            previsao *= 0.65
        else:
            previsao *= 0.25

        fator = self.sistema.get_fator()
        previsao *= fator

        return max(0.0, previsao)

    def calcular_custo_beneficio(self, atleta):
        previsao = self.calcular_previsao(atleta)
        preco = float(atleta.get('preco_num', 1))

        if preco == 0:
            return 0.0

        return previsao / preco

    def selecionar_jogadores_por_posicao(self, posicao_id, quantidade, orcamento_disponivel):
        """Seleciona jogadores de uma posição"""
        if self.atletas.empty:
            return []

        candidatos = self.atletas[
            (self.atletas['posicao_id'] == posicao_id) &
            (self.atletas['status_id'] == 7) &
            (self.atletas['preco_num'] > 0) &
            (self.atletas['media_num'] > 0)
        ].copy()

        if candidatos.empty:
            return []

        candidatos['PREVISAO'] = candidatos.apply(self.calcular_previsao, axis=1)
        candidatos['CB'] = candidatos.apply(self.calcular_custo_beneficio, axis=1)

        candidatos = candidatos[candidatos['PREVISAO'] > 0]

        if candidatos.empty:
            return []

        candidatos = candidatos.sort_values('CB', ascending=False)

        selecionados = []
        orcamento_restante = orcamento_disponivel

        for _, jogador in candidatos.iterrows():
            if len(selecionados) >= quantidade:
                break

            preco = float(jogador['preco_num'])
            posicoes_restantes = quantidade - len(selecionados) - 1
            reserva_minima = posicoes_restantes * 3.0

            if preco <= (orcamento_restante - reserva_minima):
                selecionados.append(jogador.to_dict())
                orcamento_restante -= preco

        if len(selecionados) < quantidade:
            candidatos_baratos = candidatos[
                ~candidatos['atleta_id'].isin([j['atleta_id'] for j in selecionados])
            ].sort_values('preco_num')

            for _, jogador in candidatos_baratos.iterrows():
                if len(selecionados) >= quantidade:
                    break

                preco = float(jogador['preco_num'])
                if preco <= orcamento_restante:
                    selecionados.append(jogador.to_dict())
                    orcamento_restante -= preco

        return selecionados
    def gerar_time_por_formacao(self, formacao):
        """Gera time completo"""
        if formacao not in FORMACOES:
            return None

        esquema = FORMACOES[formacao]

        orcamento_titulares = self.patrimonio * 0.90
        orcamento_banco = self.patrimonio * 0.10

        titulares = []
        orcamento_usado = 0.0

        # 1. Goleiro
        goleiros = self.selecionar_jogadores_por_posicao(1, 1, orcamento_titulares - orcamento_usado)
        if not goleiros or len(goleiros) < 1:
            return None
        titulares.extend(goleiros)
        orcamento_usado += sum([float(g['preco_num']) for g in goleiros])

        # 2. Laterais
        if esquema['laterais'] > 0:
            laterais = self.selecionar_jogadores_por_posicao(2, esquema['laterais'], orcamento_titulares - orcamento_usado)
            if not laterais or len(laterais) < esquema['laterais']:
                return None
            titulares.extend(laterais)
            orcamento_usado += sum([float(l['preco_num']) for l in laterais])

        # 3. Zagueiros
        zagueiros = self.selecionar_jogadores_por_posicao(3, esquema['zagueiros'], orcamento_titulares - orcamento_usado)
        if not zagueiros or len(zagueiros) < esquema['zagueiros']:
            return None
        titulares.extend(zagueiros)
        orcamento_usado += sum([float(z['preco_num']) for z in zagueiros])

        # 4. Meias
        meias = self.selecionar_jogadores_por_posicao(4, esquema['meias'], orcamento_titulares - orcamento_usado)
        if not meias or len(meias) < esquema['meias']:
            return None
        titulares.extend(meias)
        orcamento_usado += sum([float(m['preco_num']) for m in meias])

        # 5. Atacantes
        atacantes = self.selecionar_jogadores_por_posicao(5, esquema['atacantes'], orcamento_titulares - orcamento_usado)
        if not atacantes or len(atacantes) < esquema['atacantes']:
            return None
        titulares.extend(atacantes)
        orcamento_usado += sum([float(a['preco_num']) for a in atacantes])

        # 6. Técnico
        tecnicos = self.selecionar_jogadores_por_posicao(6, 1, orcamento_titulares - orcamento_usado)
        if not tecnicos or len(tecnicos) < 1:
            return None
        titulares.extend(tecnicos)
        orcamento_usado += sum([float(t['preco_num']) for t in tecnicos])

        if len(titulares) != 12:
            return None

        capitao = max(titulares, key=lambda x: float(x.get('PREVISAO', 0)))

        previsao_sem_capitao = sum([float(j.get('PREVISAO', 0)) for j in titulares])
        previsao_com_capitao = previsao_sem_capitao + float(capitao.get('PREVISAO', 0))

        # Banco
        banco = []
        orcamento_restante_banco = self.patrimonio - orcamento_usado

        for pos_id in [1, 2, 3, 4, 5]:
            reservas = self.selecionar_jogadores_por_posicao(pos_id, 1, orcamento_restante_banco)
            if reservas:
                reserva = reservas[0]
                if reserva['atleta_id'] not in [t['atleta_id'] for t in titulares]:
                    banco.append(reserva)
                    orcamento_restante_banco -= float(reserva['preco_num'])

        custo_banco = sum([float(r['preco_num']) for r in banco])
        custo_total = orcamento_usado + custo_banco
        economia = self.patrimonio - custo_total

        analise = self._analisar_time_gerado(titulares, formacao)

        return {
            'formacao': formacao,
            'titulares': titulares,
            'banco': banco,
            'capitao': capitao,
            'custo_total': custo_total,
            'custo_titulares': orcamento_usado,
            'custo_banco': custo_banco,
            'economia': economia,
            'previsao_sem_capitao': previsao_sem_capitao,
            'previsao_com_capitao': previsao_com_capitao,
            'analise': analise
        }

    def _analisar_time_gerado(self, titulares, formacao):
        """Analisa time gerado"""
        pontos_fortes = []
        pontos_fracos = []
        recomendacoes = []

        media_geral = np.mean([float(j.get('media_num', 0)) for j in titulares])
        if media_geral >= 6:
            pontos_fortes.append(f"Média geral excelente ({media_geral:.2f})")
        elif media_geral >= 4.5:
            pontos_fortes.append(f"Média geral boa ({media_geral:.2f})")
        else:
            pontos_fracos.append(f"Média geral baixa ({media_geral:.2f})")

        previsao_total = sum([float(j.get('PREVISAO', 0)) for j in titulares])
        if previsao_total >= 70:
            pontos_fortes.append(f"Alto potencial ({previsao_total:.1f} pts)")
        elif previsao_total >= 55:
            pontos_fortes.append(f"Bom potencial ({previsao_total:.1f} pts)")
        else:
            pontos_fracos.append(f"Potencial limitado ({previsao_total:.1f} pts)")

        if formacao in ["3-4-3", "4-3-3"]:
            recomendacoes.append("Formação ofensiva - ideal contra times fracos")
        elif formacao in ["5-3-2", "5-4-1"]:
            recomendacoes.append("Formação defensiva - buscar saldo de gols")
        else:
            recomendacoes.append("Formação equilibrada - versátil")

        if not pontos_fracos:
            pontos_fracos.append("Nenhum ponto crítico")

        return {
            'pontos_fortes': pontos_fortes,
            'pontos_fracos': pontos_fracos,
            'recomendacoes': recomendacoes
        }

# ==============================================================================
# FUNÇÕES DE RENDERIZAÇÃO
# ==============================================================================

def render_campo_futebol(titulares, capitao_id):
    """
    Renderiza campo de futebol - VERSÃO CORRIGIDA
    """

    goleiros = [p for p in titulares if p['posicao_id'] == 1]
    laterais = [p for p in titulares if p['posicao_id'] == 2]
    zagueiros = [p for p in titulares if p['posicao_id'] == 3]
    meias = [p for p in titulares if p['posicao_id'] == 4]
    atacantes = [p for p in titulares if p['posicao_id'] == 5]

    html = """
    <div class="campo-futebol">
    """

    # ATACANTES
    if atacantes:
        html += '<div class="linha-jogadores">'
        for atk in atacantes:
            is_capitao = int(atk['atleta_id']) == int(capitao_id)
            foto = str(atk.get('foto', '')).replace('FORMATO', '220x220')

            html += f"""
            <div class="jogador {'capitao' if is_capitao else ''}">
                <img src="{foto}" alt="{atk['apelido']}">
                <div class="jogador-nome">{atk['apelido']}</div>
                <div class="jogador-stats">{atk.get('PREVISAO', 0):.1f} pts</div>
                <div class="jogador-preco">C$ {atk.get('preco_num', 0):.1f}</div>
                {'<div class="jogador-capitao">👑 CAPITÃO</div>' if is_capitao else ''}
            </div>
            """
        html += '</div>'

    # MEIAS
    if meias:
        html += '<div class="linha-jogadores">'
        for mei in meias:
            is_capitao = int(mei['atleta_id']) == int(capitao_id)
            foto = str(mei.get('foto', '')).replace('FORMATO', '220x220')

            html += f"""
            <div class="jogador {'capitao' if is_capitao else ''}">
                <img src="{foto}" alt="{mei['apelido']}">
                <div class="jogador-nome">{mei['apelido']}</div>
                <div class="jogador-stats">{mei.get('PREVISAO', 0):.1f} pts</div>
                <div class="jogador-preco">C$ {mei.get('preco_num', 0):.1f}</div>
                {'<div class="jogador-capitao">👑 CAPITÃO</div>' if is_capitao else ''}
            </div>
            """
        html += '</div>'

    # DEFENSORES
    defensores = laterais + zagueiros
    if defensores:
        html += '<div class="linha-jogadores">'
        for def_p in defensores:
            is_capitao = int(def_p['atleta_id']) == int(capitao_id)
            foto = str(def_p.get('foto', '')).replace('FORMATO', '220x220')

            html += f"""
            <div class="jogador {'capitao' if is_capitao else ''}">
                <img src="{foto}" alt="{def_p['apelido']}">
                <div class="jogador-nome">{def_p['apelido']}</div>
                <div class="jogador-stats">{def_p.get('PREVISAO', 0):.1f} pts</div>
                <div class="jogador-preco">C$ {def_p.get('preco_num', 0):.1f}</div>
                {'<div class="jogador-capitao">👑 CAPITÃO</div>' if is_capitao else ''}
            </div>
            """
        html += '</div>'

    # GOLEIRO
    if goleiros:
        html += '<div class="linha-jogadores">'
        gk = goleiros[0]
        is_capitao = int(gk['atleta_id']) == int(capitao_id)
        foto = str(gk.get('foto', '')).replace('FORMATO', '220x220')

        html += f"""
        <div class="jogador {'capitao' if is_capitao else ''}">
            <img src="{foto}" alt="{gk['apelido']}">
            <div class="jogador-nome">{gk['apelido']}</div>
            <div class="jogador-stats">{gk.get('PREVISAO', 0):.1f} pts</div>
            <div class="jogador-preco">C$ {gk.get('preco_num', 0):.1f}</div>
            {'<div class="jogador-capitao">👑 CAPITÃO</div>' if is_capitao else ''}
        </div>
        """
        html += '</div>'

    html += '</div>'

    # FIX CRÍTICO - unsafe_allow_html=True
    st.markdown(html, unsafe_allow_html=True)


def render_player_card(analise):
    """Renderiza card de jogador - RETORNA HTML"""

    card_class = f"player-card {analise.get('classificacao', 'good')}"
    foto = str(analise.get('foto', '')).replace('FORMATO', '220x220')

    html = f"""
    <div class="{card_class}">
        <img src="{foto}" class="player-img" alt="{analise['apelido']}">

        <div class="player-name">{analise['apelido']}</div>

        <div style="text-align: center; margin: 10px 0;">
            <span style="background: {'#2ea043' if analise['classificacao'] == 'excellent' else '#d29922' if analise['classificacao'] == 'warning' else '#da3633' if analise['classificacao'] == 'danger' else '#58a6ff'}; 
                         color: white; 
                         padding: 4px 12px; 
                         border-radius: 12px; 
                         font-size: 11px; 
                         font-weight: 700;">
                {analise.get('label', 'BOM')}
            </span>
        </div>

        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">Posição</div>
                <div class="stat-value">{analise['posicao']}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Preço</div>
                <div class="stat-value price">C$ {analise['preco']:.1f}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Média</div>
                <div class="stat-value">{analise['media']:.2f}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Variação</div>
                <div class="stat-value" style="color: {'#2ea043' if analise['variacao'] > 0 else '#da3633' if analise['variacao'] < 0 else '#8b949e'}">
                    {analise['variacao']:+.1f}
                </div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Previsão</div>
                <div class="stat-value prediction">{analise['previsao']:.1f}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Status</div>
                <div class="stat-value" style="font-size: 11px;">{analise['status']}</div>
            </div>
        </div>

        <div class="player-score-bar">
            <div class="player-score-fill" style="width: {analise['score']}%"></div>
        </div>
        <div style="text-align: center; font-size: 11px; color: #8b949e; margin-top: 4px;">
            Score: {analise['score']}/100
        </div>
    """

    if analise.get('qualidades'):
        html += '<div style="margin-top: 12px;">'
        html += '<div style="font-size: 11px; color: #2ea043; font-weight: 700; margin-bottom: 6px;">✅ QUALIDADES</div>'
        for qual in analise['qualidades'][:2]:
            html += f'<div style="font-size: 10px; color: #8b949e; margin-bottom: 3px;">• {qual}</div>'
        html += '</div>'

    if analise.get('problemas'):
        html += '<div style="margin-top: 12px;">'
        html += '<div style="font-size: 11px; color: #d29922; font-weight: 700; margin-bottom: 6px;">⚠️ ATENÇÃO</div>'
        for prob in analise['problemas'][:2]:
            html += f'<div style="font-size: 10px; color: #8b949e; margin-bottom: 3px;">• {prob}</div>'
        html += '</div>'

    html += '</div>'

    return html
# ==============================================================================
# FUNÇÃO MAIN
# ==============================================================================

def main():
    """Função principal"""

    load_css()

    # Inicializa sistema
    if 'sistema' not in st.session_state:
        st.session_state['sistema'] = SistemaAprendizado()

    sistema = st.session_state['sistema']

    # HEADER
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🧠 ORÁCULO WAR ROOM V9.0</div>
        <div class="main-subtitle">SISTEMA INTELIGENTE COM APRENDIZADO DE IA</div>
    </div>
    """, unsafe_allow_html=True)

    # SIDEBAR
    with st.sidebar:
        st.markdown("### ⚙️ Configurações")

        user_slug = st.text_input(
            "🔍 Nome ou Slug do Time",
            placeholder="Ex: meu-time-fc",
            help="Digite o nome ou slug do seu time",
            key="input_slug"
        )

        if user_slug and len(user_slug.strip()) >= 3:
            if st.button("🔎 Buscar Time", use_container_width=True):
                st.session_state['user_slug'] = user_slug.strip()
                st.rerun()

        st.markdown("---")
        st.markdown("### 🧠 Sistema de Aprendizado")

        stats = sistema.get_estatisticas()
        if stats:
            st.metric("Previsões", stats['total_previsoes'])
            st.metric("Conferidas", stats['conferidas'])
            st.metric("Fator", f"{stats['fator_ajuste']:.3f}")
            if stats['conferidas'] > 0:
                st.metric("Erro Médio", f"{stats['erro_medio']:.1f} pts")
        else:
            st.info("Nenhuma previsão ainda")

        st.markdown("---")
        st.markdown("""
        <div style="font-size: 11px; color: #8b949e; text-align: center;">
            Oráculo War Room V9.0<br>
            Desenvolvido com IA
        </div>
        """, unsafe_allow_html=True)

    # CARREGA DADOS DA API
    with st.spinner("🔄 Carregando dados do Cartola FC..."):
        mercado = get_cartola_data("atletas/mercado")
        partidas = get_cartola_data("partidas")
        status_mercado = get_cartola_data("mercado/status")

    if not mercado or 'atletas' not in mercado:
        st.error("""
        🚫 **Erro ao carregar dados da API**

        Possíveis causas:
        - API fora do ar
        - Problema de conexão
        - Mercado fechado

        Tente novamente em alguns minutos.
        """)
        st.stop()

    # TIMER DO MERCADO
    if status_mercado and 'fechamento' in status_mercado:
        try:
            fechamento = status_mercado['fechamento'].get('timestamp', 0)
            agora = time.time()
            restante = fechamento - agora

            if restante > 0:
                horas = int(restante // 3600)
                minutos = int((restante % 3600) // 60)

                st.markdown(
                    f'<div class="timer-box">⏰ MERCADO FECHA EM: {horas:02d}h {minutos:02d}min</div>',
                    unsafe_allow_html=True
                )
            else:
                st.warning("⚠️ Mercado fechado")
        except:
            pass

    # BUSCA TIME DO USUÁRIO
    user_team = None
    patrimonio = 100.0

    if 'user_slug' in st.session_state and st.session_state['user_slug']:
        with st.spinner(f"🔍 Buscando time '{st.session_state['user_slug']}'..."):
            user_team = buscar_time_usuario(st.session_state['user_slug'])

            if user_team:
                if 'time' in user_team:
                    time_info = user_team['time']
                    nome_time = time_info.get('nome', 'Time não encontrado')
                    patrimonio = float(time_info.get('patrimonio', 100.0))
                else:
                    nome_time = user_team.get('nome', 'Time não encontrado')
                    patrimonio = float(user_team.get('patrimonio', 100.0))

                st.markdown(f"""
                <div class="team-header">
                    <div class="team-name">{nome_time}</div>
                    <div class="team-info">
                        💰 Patrimônio: <strong>C$ {patrimonio:.2f}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"""
                ⚠️ **Time '{st.session_state['user_slug']}' não encontrado**

                Verifique se:
                - O nome está correto
                - O time existe no Cartola FC
                - Você digitou o slug correto
                """)
                st.stop()

    # TABS PRINCIPAIS
    if user_team:
        tab1, tab2, tab3 = st.tabs([
            "📊 Análise do Seu Time",
            "🎯 Gerador de Times",
            "📈 Histórico de Aprendizado"
        ])

        # ====================================================================
        # TAB 1: ANÁLISE DO SEU TIME
        # ====================================================================

        with tab1:
            st.markdown("### 📊 Análise Completa do Seu Time")

            atletas_time = []
            capitao_id = None

            atletas_time = []
capitao_id = None

if 'time' in user_team:
    time_data = user_team['time']

    if 'atletas' in time_data:
        atletas_obj = time_data['atletas']

        if isinstance(atletas_obj, dict):
            atletas_time = list(atletas_obj.values())
        elif isinstance(atletas_obj, list):
            atletas_time = atletas_obj
        else:
            atletas_time = []

    capitao_id = time_data.get('capitao_id')

elif 'atletas' in user_team:
    atletas_obj = user_team['atletas']

    if isinstance(atletas_obj, dict):
        atletas_time = list(atletas_obj.values())
    elif isinstance(atletas_obj, list):
        atletas_time = atletas_obj
    else:
        atletas_time = []

    capitao_id = user_team.get('capitao_id')
                st.warning("⚠️ Nenhum atleta encontrado no seu time")
            else:
                analisador = AnalisadorTime(mercado, partidas)
                resultado_analise = analisador.analisar_time_completo(atletas_time, capitao_id)

                # MÉTRICAS GERAIS
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    score_cor = (
                        "#2ea043" if resultado_analise['score_geral'] >= 75 
                        else "#d29922" if resultado_analise['score_geral'] >= 50 
                        else "#da3633"
                    )
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size: 12px; color: #8b949e; margin-bottom: 8px;">SCORE GERAL</div>
                        <div class="metric-value" style="color: {score_cor};">
                            {resultado_analise['score_geral']:.0f}
                        </div>
                        <div style="font-size: 11px; color: #8b949e; margin-top: 4px;">/100</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size: 12px; color: #8b949e; margin-bottom: 8px;">PREVISÃO TOTAL</div>
                        <div class="metric-value" style="color: #bc4bff;">
                            {resultado_analise['previsao_total']:.1f}
                        </div>
                        <div style="font-size: 11px; color: #8b949e; margin-top: 4px;">pontos</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size: 12px; color: #8b949e; margin-bottom: 8px;">MÉDIA GERAL</div>
                        <div class="metric-value" style="color: #58a6ff;">
                            {resultado_analise['media_geral']:.2f}
                        </div>
                        <div style="font-size: 11px; color: #8b949e; margin-top: 4px;">pontos/jogo</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col4:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size: 12px; color: #8b949e; margin-bottom: 8px;">STATUS</div>
                        <div style="font-size: 14px; margin-top: 8px;">
                            <div style="color: #2ea043;">✅ {resultado_analise['provaveis']} Prováveis</div>
                            <div style="color: #d29922;">⚠️ {resultado_analise['duvidas']} Dúvidas</div>
                            <div style="color: #da3633;">❌ {resultado_analise['nao_provaveis']} Outros</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # ALERTAS CRÍTICOS
                if resultado_analise['alertas_criticos']:
                    st.markdown("---")
                    st.markdown("### 🚨 Alertas Críticos")

                    for alerta in resultado_analise['alertas_criticos']:
                        if alerta['gravidade'] == 'error':
                            st.error(f"**{alerta['atleta']}** ({alerta['posicao']}): {alerta['motivo']}")
                        else:
                            st.warning(f"**{alerta['atleta']}** ({alerta['posicao']}): {alerta['motivo']}")

                # CARDS DOS ATLETAS
                st.markdown("---")
                st.markdown("### 👥 Seus Atletas")

                analises_ordenadas = sorted(
                    resultado_analise['analises'],
                    key=lambda x: x['score']
                )

                cols = st.columns(3)
                for i, analise in enumerate(analises_ordenadas):
                    with cols[i % 3]:
                        st.markdown(
                            render_player_card(analise),
                            unsafe_allow_html=True
                        )
        # ====================================================================
        # TAB 2: GERADOR DE TIMES
        # ====================================================================

        with tab2:
            st.markdown("### 🎯 Gerador Inteligente de Times")

            fator = sistema.get_fator()
            cor_fator = (
                "#2ea043" if 0.9 <= fator <= 1.1 
                else "#d29922" if 0.8 <= fator <= 1.2 
                else "#da3633"
            )

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #161b22 0%, #1a1f2e 100%); 
                        border: 2px solid #30363d; 
                        border-radius: 16px; 
                        padding: 20px; 
                        margin-bottom: 25px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div>
                        <div style="font-size: 12px; color: #8b949e; margin-bottom: 8px;">💰 SEU ORÇAMENTO</div>
                        <div style="font-size: 32px; font-weight: 900; color: #2ea043;">C$ {patrimonio:.2f}</div>
                        <div style="font-size: 11px; color: #8b949e; margin-top: 6px;">
                            Disponível para montar o time
                        </div>
                    </div>
                    <div>
                        <div style="font-size: 12px; color: #8b949e; margin-bottom: 8px;">🧠 FATOR DE APRENDIZADO</div>
                        <div style="font-size: 32px; font-weight: 900; color: {cor_fator};">{fator:.3f}</div>
                        <div style="font-size: 11px; color: #8b949e; margin-top: 6px;">
                            {'Otimista' if fator > 1.0 else 'Conservador' if fator < 1.0 else 'Neutro'}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_form, col_info = st.columns([1, 2])

            with col_form:
                st.markdown("#### 📐 Escolha a Formação")

                formacao_escolhida = st.selectbox(
                    "Esquema Tático",
                    list(FORMACOES.keys()),
                    help="Escolha a formação"
                )

                comp = FORMACOES[formacao_escolhida]
                st.info(f"""
                **Composição:**
                - {comp['zagueiros']} Zagueiros
                - {comp['laterais']} Laterais
                - {comp['meias']} Meias
                - {comp['atacantes']} Atacantes
                """)

                rodada_atual = st.number_input(
                    "Rodada Atual",
                    min_value=1,
                    max_value=38,
                    value=1,
                    help="Número da rodada"
                )

                if st.button("⚡ GERAR TIME COM IA", type="primary", use_container_width=True):
                    with st.spinner(f"🤖 Montando time {formacao_escolhida}..."):
                        try:
                            gerador = GeradorTimesIA(mercado, partidas, patrimonio, sistema)
                            time_gerado = gerador.gerar_time_por_formacao(formacao_escolhida)

                            if time_gerado and time_gerado['titulares']:
                                if 'times_gerados' not in st.session_state:
                                    st.session_state['times_gerados'] = []

                                indice = sistema.registrar(time_gerado, rodada_atual)
                                time_gerado['indice_previsao'] = indice
                                time_gerado['rodada'] = rodada_atual

                                st.session_state['times_gerados'].append(time_gerado)

                                st.success(f"✅ Time {formacao_escolhida} gerado!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("""
                                ❌ **Não foi possível gerar o time**

                                Possíveis motivos:
                                - Orçamento insuficiente (mínimo C$ 80)
                                - Poucos jogadores prováveis
                                - Formação muito cara

                                **Sugestões:**
                                - Tente outra formação
                                - Aguarde atualização do mercado
                                """)
                        except Exception as e:
                            st.error(f"❌ Erro: {str(e)}")

            with col_info:
                st.markdown("#### 💡 Dicas de Formação")

                st.markdown("""
                **Formações Ofensivas:**
                - **3-4-3**: Máximo de atacantes
                - **4-3-3**: Ataque forte equilibrado

                **Formações Equilibradas:**
                - **4-4-2**: Clássica e confiável
                - **3-5-2**: Meio-campo forte

                **Formações Defensivas:**
                - **5-3-2**: Defesa reforçada
                - **5-4-1**: Máxima proteção
                - **4-5-1**: Meio-campo povoado

                ---

                **🧠 Sistema de Aprendizado:**

                1. IA registra cada previsão
                2. Você confere o resultado real
                3. IA ajusta automaticamente
                4. Previsões ficam mais precisas
                """)

            # EXIBIÇÃO DOS TIMES GERADOS
            if 'times_gerados' in st.session_state and st.session_state['times_gerados']:
                st.markdown("---")
                st.markdown(f"### 📋 Times Gerados ({len(st.session_state['times_gerados'])})")

                col_btn1, col_btn2 = st.columns([3, 1])

                with col_btn2:
                    if st.button("🗑️ Limpar Todos", type="secondary", use_container_width=True):
                        st.session_state['times_gerados'] = []
                        st.success("✅ Times limpos!")
                        st.rerun()

                for idx, time_gerado in enumerate(st.session_state['times_gerados'], 1):

                    if time_gerado['previsao_com_capitao'] >= 70:
                        icone = "🏆"
                    elif time_gerado['previsao_com_capitao'] >= 55:
                        icone = "⚽"
                    else:
                        icone = "⚠️"

                    with st.expander(
                        f"{icone} **TIME {idx}**: {time_gerado['formacao']} - "
                        f"Rodada {time_gerado['rodada']} - "
                        f"{time_gerado['previsao_com_capitao']:.1f} pts previstos",
                        expanded=(idx == len(st.session_state['times_gerados']))
                    ):

                        # MÉTRICAS DO TIME
                        col1, col2, col3, col4 = st.columns(4)

                        col1.metric(
                            "💰 Custo Total",
                            f"C$ {time_gerado['custo_total']:.2f}",
                            f"-C$ {patrimonio - time_gerado['custo_total']:.2f}"
                        )

                        col2.metric(
                            "📊 Previsão",
                            f"{time_gerado['previsao_com_capitao']:.1f} pts",
                            f"+{time_gerado['capitao']['PREVISAO']:.1f} (capitão)"
                        )

                        col3.metric(
                            "👑 Capitão",
                            time_gerado['capitao']['apelido'][:15],
                            f"{time_gerado['capitao']['PREVISAO']:.1f} pts"
                        )

                        col4.metric(
                            "💵 Economia",
                            f"C$ {time_gerado['economia']:.2f}",
                            f"{(time_gerado['economia']/patrimonio)*100:.1f}%"
                        )

                        st.markdown("---")

                        # CAMPO DE FUTEBOL
                        render_campo_futebol(
                            time_gerado['titulares'],
                            time_gerado['capitao']['atleta_id']
                        )

                        st.markdown("---")

                        # ANÁLISE DO TIME
                        st.markdown("#### 📊 Análise do Time")

                        col_forte, col_fraco = st.columns(2)

                        with col_forte:
                            st.success("**✅ PONTOS FORTES**")
                            for ponto in time_gerado['analise']['pontos_fortes']:
                                st.markdown(f"• {ponto}")

                        with col_fraco:
                            st.warning("**⚠️ PONTOS FRACOS**")
                            for ponto in time_gerado['analise']['pontos_fracos']:
                                st.markdown(f"• {ponto}")

                        st.info("**💡 RECOMENDAÇÕES**")
                        for rec in time_gerado['analise']['recomendacoes']:
                            st.markdown(f"• {rec}")

                        st.markdown("---")

                        # CONFERIR RESULTADO
                        st.markdown("#### ✅ Conferir Resultado da Rodada")

                        st.info("""
                        **Como funciona:**
                        Após a rodada, digite quantos pontos seu time fez e clique em "Conferir".
                        A IA vai comparar e ajustar para melhorar nas próximas.
                        """)

                        col_conf1, col_conf2 = st.columns([3, 1])

                        with col_conf1:
                            pontos_reais = st.number_input(
                                "Quantos pontos o time fez?",
                                min_value=0.0,
                                max_value=300.0,
                                step=0.1,
                                value=0.0,
                                key=f"pontos_{idx}_{time_gerado['rodada']}",
                                help="Digite a pontuação real"
                            )

                        with col_conf2:
                            st.markdown("<br>", unsafe_allow_html=True)
                            if st.button(
                                "📊 Conferir",
                                key=f"btn_{idx}_{time_gerado['rodada']}",
                                use_container_width=True,
                                type="primary"
                            ):
                                if pontos_reais > 0:
                                    resultado = sistema.conferir(
                                        time_gerado['indice_previsao'],
                                        pontos_reais
                                    )

                                    if resultado and 'erro' not in resultado:
                                        precisao = 100 - resultado['erro_percentual']

                                        if precisao >= 90:
                                            cor = "#2ea043"
                                            emoji = "🎯"
                                            texto = "EXCELENTE"
                                        elif precisao >= 75:
                                            cor = "#58a6ff"
                                            emoji = "✅"
                                            texto = "MUITO BOM"
                                        elif precisao >= 60:
                                            cor = "#d29922"
                                            emoji = "⚠️"
                                            texto = "RAZOÁVEL"
                                        else:
                                            cor = "#da3633"
                                            emoji = "❌"
                                            texto = "PRECISA MELHORAR"

                                        st.markdown(f"""
                                        <div style="background: linear-gradient(135deg, #161b22 0%, #1a1f2e 100%);
                                                    border: 2px solid {cor};
                                                    border-radius: 12px;
                                                    padding: 20px;
                                                    margin-top: 15px;">
                                            <div style="text-align: center; font-size: 48px; margin-bottom: 10px;">
                                                {emoji}
                                            </div>
                                            <div style="text-align: center; font-size: 24px; font-weight: 900; color: {cor}; margin-bottom: 15px;">
                                                {texto}
                                            </div>
                                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 20px;">
                                                <div style="text-align: center;">
                                                    <div style="font-size: 12px; color: #8b949e;">PREVISÃO</div>
                                                    <div style="font-size: 28px; font-weight: 900; color: #bc4bff;">
                                                        {resultado['previsao']:.1f}
                                                    </div>
                                                </div>
                                                <div style="text-align: center;">
                                                    <div style="font-size: 12px; color: #8b949e;">REAL</div>
                                                    <div style="font-size: 28px; font-weight: 900; color: #2ea043;">
                                                        {resultado['real']:.1f}
                                                    </div>
                                                </div>
                                            </div>
                                            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #30363d;">
                                                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                                    <span style="color: #8b949e;">Erro:</span>
                                                    <span style="color: white; font-weight: 700;">{resultado['erro']:.1f} pts</span>
                                                </div>
                                                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                                                    <span style="color: #8b949e;">Precisão:</span>
                                                    <span style="color: {cor}; font-weight: 700;">{precisao:.1f}%</span>
                                                </div>
                                                <div style="display: flex; justify-content: space-between;">
                                                    <span style="color: #8b949e;">Novo Fator:</span>
                                                    <span style="color: white; font-weight: 700;">{resultado['fator']:.3f}</span>
                                                </div>
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)

                                        st.success("✅ Resultado conferido! IA ajustada.")
                                        time.sleep(2)
                                        st.rerun()
                                    else:
                                        st.warning("⚠️ Previsão já conferida.")
                                else:
                                    st.error("❌ Digite um valor maior que zero.")

                        # BANCO
                        if time_gerado.get('banco'):
                            st.markdown("---")
                            with st.expander(
                                f"📋 Banco ({len(time_gerado['banco'])} jogadores) - "
                                f"C$ {time_gerado['custo_banco']:.2f}"
                            ):
                                cols_banco = st.columns(len(time_gerado['banco']))

                                for i, reserva in enumerate(time_gerado['banco']):
                                    with cols_banco[i]:
                                        foto = str(reserva.get('foto', '')).replace('FORMATO', '140x140')
                                        st.image(foto, use_container_width=True)
                                        st.markdown(f"**{reserva['apelido']}**")
                                        st.caption(f"{POSICOES.get(reserva['posicao_id'], 'N/A')}")
                                        st.info(f"C$ {reserva.get('preco_num', 0):.1f}")

            else:
                st.info("""
                👆 **Como usar:**

                1. Escolha uma formação
                2. Clique em "Gerar Time"
                3. IA monta o melhor time
                4. Confira resultado após rodada
                """)
        # ====================================================================
        # TAB 3: HISTÓRICO DE APRENDIZADO
        # ====================================================================

        with tab3:
            st.markdown("### 📈 Sistema de Aprendizado da IA")

            stats = sistema.get_estatisticas()

            if stats and stats['conferidas'] > 0:

                # MÉTRICAS PRINCIPAIS
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size: 12px; color: #8b949e; margin-bottom: 8px;">TOTAL</div>
                        <div class="metric-value" style="color: #58a6ff;">
                            {stats['total_previsoes']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size: 12px; color: #8b949e; margin-bottom: 8px;">CONFERIDAS</div>
                        <div class="metric-value" style="color: #2ea043;">
                            {stats['conferidas']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col3:
                    cor_erro = "#2ea043" if stats['erro_medio'] < 5 else "#d29922" if stats['erro_medio'] < 10 else "#da3633"
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size: 12px; color: #8b949e; margin-bottom: 8px;">ERRO MÉDIO</div>
                        <div class="metric-value" style="color: {cor_erro};">
                            {stats['erro_medio']:.1f}
                        </div>
                        <div style="font-size: 11px; color: #8b949e; margin-top: 4px;">pontos</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col4:
                    cor_fator = "#2ea043" if 0.9 <= stats['fator_ajuste'] <= 1.1 else "#d29922"
                    st.markdown(f"""
                    <div class="metric-box">
                        <div style="font-size: 12px; color: #8b949e; margin-bottom: 8px;">FATOR</div>
                        <div class="metric-value" style="color: {cor_fator};">
                            {stats['fator_ajuste']:.3f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                # EXPLICAÇÃO
                st.markdown("#### 🧠 Como Funciona o Aprendizado")

                col_exp1, col_exp2 = st.columns(2)

                with col_exp1:
                    st.success("""
                    **✅ Processo:**

                    1. Você gera um time
                    2. IA registra a previsão
                    3. Você informa pontos reais
                    4. IA calcula erro e ajusta
                    5. Próximas previsões melhoram
                    """)

                with col_exp2:
                    st.info("""
                    **📊 Fator de Ajuste:**

                    - **> 1.0**: IA otimista
                    - **= 1.0**: IA neutra
                    - **< 1.0**: IA conservadora

                    Ajusta automaticamente baseado
                    na precisão anterior.
                    """)

                st.markdown("---")

                # ESTATÍSTICAS DETALHADAS
                st.markdown("#### 📊 Estatísticas Detalhadas")

                col_det1, col_det2, col_det3 = st.columns(3)

                with col_det1:
                    st.metric(
                        "Melhor Previsão",
                        f"{stats['erro_minimo']:.1f} pts erro",
                        "🎯 Mais precisa"
                    )

                with col_det2:
                    st.metric(
                        "Pior Previsão",
                        f"{stats['erro_maximo']:.1f} pts erro",
                        "⚠️ Menos precisa"
                    )

                with col_det3:
                    precisao_media = 100 - ((stats['erro_medio'] / 60) * 100)
                    precisao_media = max(0, min(100, precisao_media))
                    st.metric(
                        "Precisão Média",
                        f"{precisao_media:.1f}%",
                        "📈 Geral"
                    )

                st.markdown("---")

                # HISTÓRICO
                st.markdown("#### 📜 Histórico de Previsões")

                historico_data = []
                for prev in sistema.historico['previsoes']:
                    if prev['conferido']:
                        erro = abs(prev['previsao_total'] - prev['pontos_reais'])
                        erro_perc = (erro / prev['previsao_total']) * 100 if prev['previsao_total'] > 0 else 0
                        precisao = 100 - erro_perc

                        historico_data.append({
                            'Rodada': prev['rodada'],
                            'Formação': prev['formacao'],
                            'Previsão': f"{prev['previsao_total']:.1f}",
                            'Real': f"{prev['pontos_reais']:.1f}",
                            'Erro': f"{erro:.1f}",
                            'Precisão': f"{precisao:.1f}%",
                            'Fator': f"{prev['fator_usado']:.3f}"
                        })

                if historico_data:
                    df_historico = pd.DataFrame(historico_data)
                    st.dataframe(
                        df_historico,
                        use_container_width=True,
                        hide_index=True
                    )

                    csv = df_historico.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Baixar Histórico (CSV)",
                        data=csv,
                        file_name=f"historico_oraculo_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info("Nenhuma previsão conferida.")

                st.markdown("---")

                # GRÁFICO
                if len(historico_data) >= 3:
                    st.markdown("#### 📈 Evolução da Precisão")

                    rodadas = [h['Rodada'] for h in historico_data]
                    precisoes = [float(h['Precisão'].replace('%', '')) for h in historico_data]

                    df_grafico = pd.DataFrame({
                        'Rodada': rodadas,
                        'Precisão (%)': precisoes
                    })

                    st.line_chart(df_grafico.set_index('Rodada'))

                    if len(precisoes) >= 2:
                        tendencia = precisoes[-1] - precisoes[0]
                        if tendencia > 5:
                            st.success(f"📈 Tendência positiva! Melhorou {tendencia:.1f}%")
                        elif tendencia < -5:
                            st.warning(f"📉 Caiu {abs(tendencia):.1f}%. Continue conferindo!")
                        else:
                            st.info("➡️ Precisão estável.")

            else:
                # SEM DADOS
                st.info("""
                ### 🎓 Bem-vindo ao Sistema de Aprendizado!

                Você ainda não tem previsões conferidas.
                """)

                col_t1, col_t2, col_t3 = st.columns(3)

                with col_t1:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #161b22 0%, #1a1f2e 100%);
                                border: 2px solid #58a6ff;
                                border-radius: 12px;
                                padding: 20px;
                                text-align: center;
                                height: 200px;">
                        <div style="font-size: 48px; margin-bottom: 15px;">1️⃣</div>
                        <div style="font-size: 16px; font-weight: 700; color: #58a6ff; margin-bottom: 10px;">
                            GERE UM TIME
                        </div>
                        <div style="font-size: 12px; color: #8b949e;">
                            Vá para "Gerador de Times"
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_t2:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #161b22 0%, #1a1f2e 100%);
                                border: 2px solid #2ea043;
                                border-radius: 12px;
                                padding: 20px;
                                text-align: center;
                                height: 200px;">
                        <div style="font-size: 48px; margin-bottom: 15px;">2️⃣</div>
                        <div style="font-size: 16px; font-weight: 700; color: #2ea043; margin-bottom: 10px;">
                            AGUARDE RODADA
                        </div>
                        <div style="font-size: 12px; color: #8b949e;">
                            Veja quantos pontos fez
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with col_t3:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #161b22 0%, #1a1f2e 100%);
                                border: 2px solid #bc4bff;
                                border-radius: 12px;
                                padding: 20px;
                                text-align: center;
                                height: 200px;">
                        <div style="font-size: 48px; margin-bottom: 15px;">3️⃣</div>
                        <div style="font-size: 16px; font-weight: 700; color: #bc4bff; margin-bottom: 10px;">
                            CONFIRA RESULTADO
                        </div>
                        <div style="font-size: 12px; color: #8b949e;">
                            IA vai aprender!
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")

                st.success("""
                **💡 Dica:** Quanto mais você usar, mais precisa a IA fica!
                """)

    else:
        # SEM TIME
        st.info("""
        ### 👋 Bem-vindo ao Oráculo War Room V9.0!

        Digite o nome do seu time na barra lateral para começar.

        **Funcionalidades:**
        - 📊 Análise completa do time
        - 🚀 Gerador inteligente
        - 🧠 Sistema de aprendizado
        - 📈 Estatísticas
        """)

        col_f1, col_f2, col_f3 = st.columns(3)

        with col_f1:
            st.success("""
            **📊 Análise Inteligente**

            - Score 0-100
            - Alertas críticos
            - Recomendações
            - Previsão de pontos
            """)

        with col_f2:
            st.info("""
            **🚀 Gerador de Times**

            - 7 formações
            - Usa todo orçamento
            - Melhor custo-benefício
            - Campo visual
            """)

        with col_f3:
            st.warning("""
            **🧠 Aprendizado de IA**

            - Registra previsões
            - Você confere resultados
            - IA ajusta sozinha
            - Fica mais precisa
            """)

# ==============================================================================
# EXECUÇÃO
# ==============================================================================

if __name__ == "__main__":
    main()
