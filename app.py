"""
🧠 ORÁCULO CARTOLA FC - SISTEMA PROFISSIONAL
Análise Inteligente | Otimização Matemática | Interface Premium
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Oráculo Cartola FC - Sistema Profissional",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# ESTILOS CSS PROFISSIONAIS
# ==============================================================================

def load_professional_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

        * {
            font-family: 'Poppins', sans-serif;
        }

        .main {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        }

        .stApp {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
        }

        /* HEADER PROFISSIONAL */
        .pro-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        }

        .pro-title {
            font-size: 56px;
            font-weight: 900;
            color: white;
            margin: 0;
            text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }

        .pro-subtitle {
            font-size: 18px;
            color: rgba(255,255,255,0.9);
            margin-top: 10px;
            font-weight: 300;
        }

        /* CARDS PROFISSIONAIS */
        .pro-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            transition: all 0.3s ease;
        }

        .pro-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
            border-color: rgba(102, 126, 234, 0.5);
        }

        /* JOGADOR CARD */
        .player-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            transition: all 0.3s ease;
        }

        .player-card:hover {
            transform: scale(1.02);
            border-color: #667eea;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }

        .player-name {
            font-size: 24px;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
        }

        .player-stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 15px;
        }

        .stat-box {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }

        .stat-label {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.6);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stat-value {
            font-size: 24px;
            font-weight: 700;
            color: #667eea;
            margin-top: 5px;
        }

        /* SCORE BAR */
        .score-bar-container {
            width: 100%;
            height: 30px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 15px;
            overflow: hidden;
            margin: 15px 0;
        }

        .score-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 700;
            font-size: 14px;
            transition: width 0.5s ease;
        }

        /* MÉTRICAS */
        .metric-container {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 30px 0;
        }

        .metric-card {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
        }

        .metric-value-large {
            font-size: 48px;
            font-weight: 900;
            color: #667eea;
        }

        .metric-label-large {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.7);
            margin-top: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* BADGES */
        .badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            margin: 5px;
        }

        .badge-success {
            background: rgba(46, 213, 115, 0.2);
            color: #2ed573;
            border: 1px solid #2ed573;
        }

        .badge-warning {
            background: rgba(255, 159, 67, 0.2);
            color: #ff9f43;
            border: 1px solid #ff9f43;
        }

        .badge-danger {
            background: rgba(255, 71, 87, 0.2);
            color: #ff4757;
            border: 1px solid #ff4757;
        }

        .badge-info {
            background: rgba(102, 126, 234, 0.2);
            color: #667eea;
            border: 1px solid #667eea;
        }

        /* CAMPO DE FUTEBOL */
        .campo-container {
            background: linear-gradient(180deg, #2d5016 0%, #1a3d0a 100%);
            border-radius: 20px;
            padding: 40px;
            margin: 30px 0;
            position: relative;
            min-height: 700px;
            box-shadow: inset 0 0 100px rgba(0,0,0,0.5);
        }

        .campo-linha {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin: 40px 0;
        }

        .jogador-campo {
            background: rgba(0, 0, 0, 0.7);
            border: 3px solid #2ed573;
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            min-width: 120px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }

        .jogador-campo:hover {
            transform: translateY(-10px) scale(1.05);
            box-shadow: 0 15px 40px rgba(46, 213, 115, 0.4);
        }

        .jogador-campo.capitao {
            border-color: #ffd700;
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        }

        .jogador-foto {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: 3px solid #2ed573;
            margin: 0 auto 10px;
        }

        .jogador-campo.capitao .jogador-foto {
            border-color: #ffd700;
        }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# CLASSES DE DADOS
# ==============================================================================

@dataclass
class Jogador:
    """Modelo de dados do jogador"""
    atleta_id: int
    nome: str
    apelido: str
    clube_id: int
    clube_nome: str
    posicao_id: int
    posicao_nome: str
    preco: float
    media: float
    pontos: float
    jogos: int
    status_id: int
    foto: str
    scout: Dict = field(default_factory=dict)

    @property
    def preco_formatado(self) -> str:
        return f"C$ {self.preco:.2f}"

    @property
    def media_formatada(self) -> str:
        return f"{self.media:.2f}"

@dataclass
class AnaliseIA:
    """Resultado da análise de IA"""
    jogador: Jogador
    score: float
    custo_beneficio: float
    tendencia: str
    confiabilidade: float
    explicacao: List[str]
    metricas: Dict[str, float]

# ==============================================================================
# MOTOR DE IA
# ==============================================================================

class InteligenciaArtificial:
    """Sistema de IA para análise de jogadores"""

    @staticmethod
    def calcular_score(jogador: Jogador, partidas: Optional[Dict] = None) -> float:
        """
        Calcula score inteligente do jogador (0-100)

        Fatores considerados:
        - Média de pontos (40%)
        - Custo-benefício (25%)
        - Regularidade (20%)
        - Status/Condição (15%)
        """
        score = 0.0

        # Fator 1: Média de pontos (0-40 pontos)
        if jogador.media > 0:
            media_normalizada = min(jogador.media / 15, 1.0)  # 15 pts = excelente
            score += media_normalizada * 40

        # Fator 2: Custo-benefício (0-25 pontos)
        if jogador.preco > 0 and jogador.media > 0:
            cb = jogador.media / jogador.preco
            cb_normalizado = min(cb / 2, 1.0)  # 2.0 = excelente CB
            score += cb_normalizado * 25

        # Fator 3: Regularidade (0-20 pontos)
        if jogador.jogos >= 5:
            regularidade = min(jogador.jogos / 10, 1.0)
            score += regularidade * 20
        elif jogador.jogos > 0:
            score += (jogador.jogos / 5) * 10

        # Fator 4: Status (0-15 pontos)
        status_pontos = {
            7: 15,  # Provável
            6: 10,  # Dúvida
            5: 0,   # Lesionado
            3: 0,   # Suspenso
            2: 0    # Nulo
        }
        score += status_pontos.get(jogador.status_id, 0)

        return round(score, 2)

    @staticmethod
    def analisar_jogador(jogador: Jogador, partidas: Optional[Dict] = None) -> AnaliseIA:
        """Análise completa do jogador"""

        score = InteligenciaArtificial.calcular_score(jogador, partidas)

        # Custo-benefício
        cb = (jogador.media / jogador.preco) if jogador.preco > 0 else 0

        # Tendência
        if score >= 75:
            tendencia = "EXCELENTE"
        elif score >= 60:
            tendencia = "BOM"
        elif score >= 40:
            tendencia = "REGULAR"
        else:
            tendencia = "EVITAR"

        # Confiabilidade
        confiabilidade = min((jogador.jogos / 10) * 100, 100)

        # Explicação detalhada
        explicacao = []

        if jogador.media >= 8:
            explicacao.append(f"✅ Média excelente de {jogador.media:.1f} pontos")
        elif jogador.media >= 5:
            explicacao.append(f"✓ Média boa de {jogador.media:.1f} pontos")
        elif jogador.media > 0:
            explicacao.append(f"⚠️ Média baixa de {jogador.media:.1f} pontos")
        else:
            explicacao.append("❌ Sem média (não jogou)")

        if cb >= 1.5:
            explicacao.append(f"💰 Excelente custo-benefício ({cb:.2f})")
        elif cb >= 1.0:
            explicacao.append(f"💵 Bom custo-benefício ({cb:.2f})")
        elif cb > 0:
            explicacao.append(f"💸 Custo-benefício regular ({cb:.2f})")

        if jogador.jogos >= 8:
            explicacao.append(f"📊 Muito regular ({jogador.jogos} jogos)")
        elif jogador.jogos >= 5:
            explicacao.append(f"📈 Regularidade boa ({jogador.jogos} jogos)")
        elif jogador.jogos > 0:
            explicacao.append(f"⚡ Pouco rodado ({jogador.jogos} jogos)")
        else:
            explicacao.append("🆕 Ainda não jogou")

        status_msg = {
            7: "🟢 Provável para jogar",
            6: "🟡 Dúvida para jogar",
            5: "🔴 Lesionado",
            3: "🔴 Suspenso",
            2: "⚫ Nulo"
        }
        explicacao.append(status_msg.get(jogador.status_id, "Status desconhecido"))

        metricas = {
            "score": score,
            "media": jogador.media,
            "preco": jogador.preco,
            "custo_beneficio": cb,
            "jogos": jogador.jogos,
            "confiabilidade": confiabilidade
        }

        return AnaliseIA(
            jogador=jogador,
            score=score,
            custo_beneficio=cb,
            tendencia=tendencia,
            confiabilidade=confiabilidade,
            explicacao=explicacao,
            metricas=metricas
        )

# ==============================================================================
# OTIMIZADOR DE TIME
# ==============================================================================

class OtimizadorTime:
    """Otimização matemática para montagem de time"""

    def __init__(self, jogadores: List[Jogador], orcamento: float):
        self.jogadores = jogadores
        self.orcamento = orcamento
        self.ia = InteligenciaArtificial()

    def gerar_time(self, formacao: str) -> Optional[Dict]:
        """
        Gera time otimizado usando algoritmo guloso inteligente
        """

        esquema = {
            "3-4-3": {"goleiro": 1, "zagueiro": 3, "lateral": 0, "meia": 4, "atacante": 3, "tecnico": 1},
            "3-5-2": {"goleiro": 1, "zagueiro": 3, "lateral": 0, "meia": 5, "atacante": 2, "tecnico": 1},
            "4-3-3": {"goleiro": 1, "zagueiro": 2, "lateral": 2, "meia": 3, "atacante": 3, "tecnico": 1},
            "4-4-2": {"goleiro": 1, "zagueiro": 2, "lateral": 2, "meia": 4, "atacante": 2, "tecnico": 1},
            "4-5-1": {"goleiro": 1, "zagueiro": 2, "lateral": 2, "meia": 5, "atacante": 1, "tecnico": 1},
            "5-3-2": {"goleiro": 1, "zagueiro": 3, "lateral": 2, "meia": 3, "atacante": 2, "tecnico": 1},
            "5-4-1": {"goleiro": 1, "zagueiro": 3, "lateral": 2, "meia": 4, "atacante": 1, "tecnico": 1}
        }

        if formacao not in esquema:
            return None

        necessidades = esquema[formacao]

        # Mapeia posições
        pos_map = {
            "goleiro": 1,
            "lateral": 2,
            "zagueiro": 3,
            "meia": 4,
            "atacante": 5,
            "tecnico": 6
        }

        # Analisa todos os jogadores
        analises = [self.ia.analisar_jogador(j) for j in self.jogadores]

        # Separa por posição
        por_posicao = {}
        for pos_nome, pos_id in pos_map.items():
            candidatos = [a for a in analises if a.jogador.posicao_id == pos_id]
            # Ordena por score
            candidatos.sort(key=lambda x: x.score, reverse=True)
            por_posicao[pos_nome] = candidatos

        # Montagem do time
        time_selecionado = []
        custo_total = 0.0

        for posicao, quantidade in necessidades.items():
            if quantidade == 0:
                continue

            candidatos = por_posicao.get(posicao, [])

            for _ in range(quantidade):
                melhor = None

                for candidato in candidatos:
                    if candidato in time_selecionado:
                        continue

                    if custo_total + candidato.jogador.preco <= self.orcamento:
                        melhor = candidato
                        break

                if melhor:
                    time_selecionado.append(melhor)
                    custo_total += melhor.jogador.preco
                else:
                    # Não conseguiu completar o time
                    return None

        if len(time_selecionado) != 12:
            return None

        # Escolhe capitão (maior score)
        capitao = max(time_selecionado, key=lambda x: x.score)

        # Calcula métricas
        score_medio = sum(a.score for a in time_selecionado) / len(time_selecionado)
        previsao_pontos = sum(a.jogador.media for a in time_selecionado) + capitao.jogador.media

        return {
            "jogadores": time_selecionado,
            "capitao": capitao,
            "formacao": formacao,
            "custo_total": custo_total,
            "orcamento_restante": self.orcamento - custo_total,
            "score_medio": score_medio,
            "previsao_pontos": previsao_pontos
        }

# ==============================================================================
# API DO CARTOLA
# ==============================================================================

class CartolaAPI:
    """Cliente para API do Cartola FC"""

    BASE_URL = "https://api.cartola.globo.com"

    @staticmethod
    @st.cache_data(ttl=300)
    def buscar_mercado() -> Optional[Dict]:
        """Busca dados do mercado"""
        try:
            response = requests.get(
                f"{CartolaAPI.BASE_URL}/atletas/mercado",
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"❌ Erro ao buscar mercado: {str(e)}")
            return None

    @staticmethod
    @st.cache_data(ttl=300)
    def buscar_time(nome: str) -> Optional[Dict]:
        """Busca time por nome"""
        try:
            response = requests.get(
                f"{CartolaAPI.BASE_URL}/times",
                params={"q": nome},
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response.raise_for_status()
            times = response.json()

            if times and len(times) > 0:
                time_slug = times[0].get('slug')
                if time_slug:
                    response2 = requests.get(
                        f"{CartolaAPI.BASE_URL}/time/slug/{time_slug}",
                        timeout=10,
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                    response2.raise_for_status()
                    return response2.json()

            return None
        except Exception as e:
            st.error(f"❌ Erro ao buscar time: {str(e)}")
            return None

    @staticmethod
    @st.cache_data(ttl=300)
    def buscar_partidas() -> Optional[Dict]:
        """Busca partidas da rodada"""
        try:
            response = requests.get(
                f"{CartolaAPI.BASE_URL}/partidas",
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            response.raise_for_status()
            return response.json()
        except:
            return None

# ==============================================================================
# PROCESSADOR DE DADOS
# ==============================================================================

class ProcessadorDados:
    """Processa dados da API"""

    @staticmethod
    def processar_mercado(dados: Dict) -> List[Jogador]:
        """Converte dados do mercado em lista de jogadores"""
        jogadores = []

        atletas = dados.get('atletas', [])
        clubes = dados.get('clubes', {})
        posicoes = dados.get('posicoes', {})

        for atleta in atletas:
            try:
                clube_id = atleta.get('clube_id')
                clube_nome = clubes.get(str(clube_id), {}).get('nome', 'Desconhecido')

                pos_id = atleta.get('posicao_id')
                pos_nome = posicoes.get(str(pos_id), {}).get('nome', 'Desconhecido')

                jogador = Jogador(
                    atleta_id=atleta.get('atleta_id'),
                    nome=atleta.get('nome', ''),
                    apelido=atleta.get('apelido', ''),
                    clube_id=clube_id,
                    clube_nome=clube_nome,
                    posicao_id=pos_id,
                    posicao_nome=pos_nome,
                    preco=float(atleta.get('preco_num', 0)),
                    media=float(atleta.get('media_num', 0)),
                    pontos=float(atleta.get('pontos_num', 0)),
                    jogos=int(atleta.get('jogos_num', 0)),
                    status_id=atleta.get('status_id', 7),
                    foto=atleta.get('foto', '').replace('FORMATO', '140x140'),
                    scout=atleta.get('scout', {})
                )

                jogadores.append(jogador)
            except Exception as e:
                continue

        return jogadores

# ==============================================================================
# COMPONENTES DE UI
# ==============================================================================

def render_header():
    """Renderiza header profissional"""
    st.markdown("""
    <div class="pro-header">
        <div class="pro-title">🧠 ORÁCULO CARTOLA FC</div>
        <div class="pro-subtitle">Sistema Profissional de Análise Inteligente | Powered by IA</div>
    </div>
    """, unsafe_allow_html=True)

def render_analise_card(analise: AnaliseIA, is_capitao: bool = False):
    """Renderiza card de análise do jogador"""

    jogador = analise.jogador

    # Define cor do score
    if analise.score >= 75:
        score_color = "#2ed573"
    elif analise.score >= 60:
        score_color = "#667eea"
    elif analise.score >= 40:
        score_color = "#ff9f43"
    else:
        score_color = "#ff4757"

    capitao_badge = "👑 CAPITÃO" if is_capitao else ""

    st.markdown(f"""
    <div class="player-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div class="player-name">{jogador.apelido} {capitao_badge}</div>
                <div style="color: rgba(255,255,255,0.6); font-size: 14px;">
                    {jogador.clube_nome} | {jogador.posicao_nome}
                </div>
            </div>
            <img src="{jogador.foto}" style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid {score_color};">
        </div>

        <div class="score-bar-container">
            <div class="score-bar-fill" style="width: {analise.score}%; background: linear-gradient(90deg, {score_color} 0%, {score_color}88 100%);">
                SCORE: {analise.score:.1f}/100
            </div>
        </div>

        <div class="player-stats">
            <div class="stat-box">
                <div class="stat-label">Preço</div>
                <div class="stat-value" style="color: #2ed573;">{jogador.preco_formatado}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Média</div>
                <div class="stat-value" style="color: #667eea;">{jogador.media_formatada}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">C/B</div>
                <div class="stat-value" style="color: #ff9f43;">{analise.custo_beneficio:.2f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Explicação da IA
    st.markdown("**🤖 Análise da IA:**")
    for explicacao in analise.explicacao:
        st.markdown(f"- {explicacao}")

    # Badge de tendência
    badge_class = {
        "EXCELENTE": "badge-success",
        "BOM": "badge-info",
        "REGULAR": "badge-warning",
        "EVITAR": "badge-danger"
    }

    st.markdown(f"""
    <span class="badge {badge_class.get(analise.tendencia, 'badge-info')}">
        {analise.tendencia}
    </span>
    <span class="badge badge-info">
        Confiabilidade: {analise.confiabilidade:.0f}%
    </span>
    """, unsafe_allow_html=True)

def render_campo_futebol(time: Dict):
    """Renderiza campo de futebol com jogadores"""

    formacao = time['formacao']
    jogadores = time['jogadores']
    capitao = time['capitao']

    # Organiza por posição
    por_posicao = {
        1: [],  # Goleiro
        2: [],  # Lateral
        3: [],  # Zagueiro
        4: [],  # Meia
        5: [],  # Atacante
        6: []   # Técnico
    }

    for analise in jogadores:
        por_posicao[analise.jogador.posicao_id].append(analise)

    st.markdown('<div class="campo-container">', unsafe_allow_html=True)

    # Atacantes
    if por_posicao[5]:
        st.markdown('<div class="campo-linha">', unsafe_allow_html=True)
        for analise in por_posicao[5]:
            is_cap = (analise == capitao)
            cap_class = "capitao" if is_cap else ""
            st.markdown(f"""
            <div class="jogador-campo {cap_class}">
                <img src="{analise.jogador.foto}" class="jogador-foto">
                <div style="color: white; font-weight: 700; font-size: 14px;">{analise.jogador.apelido}</div>
                <div style="color: #2ed573; font-size: 12px;">{analise.score:.0f} pts</div>
                {'<div style="color: #ffd700; font-size: 20px;">👑</div>' if is_cap else ''}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Meias
    if por_posicao[4]:
        st.markdown('<div class="campo-linha">', unsafe_allow_html=True)
        for analise in por_posicao[4]:
            is_cap = (analise == capitao)
            cap_class = "capitao" if is_cap else ""
            st.markdown(f"""
            <div class="jogador-campo {cap_class}">
                <img src="{analise.jogador.foto}" class="jogador-foto">
                <div style="color: white; font-weight: 700; font-size: 14px;">{analise.jogador.apelido}</div>
                <div style="color: #2ed573; font-size: 12px;">{analise.score:.0f} pts</div>
                {'<div style="color: #ffd700; font-size: 20px;">👑</div>' if is_cap else ''}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Zagueiros e Laterais
    defensores = por_posicao[3] + por_posicao[2]
    if defensores:
        st.markdown('<div class="campo-linha">', unsafe_allow_html=True)
        for analise in defensores:
            is_cap = (analise == capitao)
            cap_class = "capitao" if is_cap else ""
            st.markdown(f"""
            <div class="jogador-campo {cap_class}">
                <img src="{analise.jogador.foto}" class="jogador-foto">
                <div style="color: white; font-weight: 700; font-size: 14px;">{analise.jogador.apelido}</div>
                <div style="color: #2ed573; font-size: 12px;">{analise.score:.0f} pts</div>
                {'<div style="color: #ffd700; font-size: 20px;">👑</div>' if is_cap else ''}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Goleiro
    if por_posicao[1]:
        st.markdown('<div class="campo-linha">', unsafe_allow_html=True)
        for analise in por_posicao[1]:
            is_cap = (analise == capitao)
            cap_class = "capitao" if is_cap else ""
            st.markdown(f"""
            <div class="jogador-campo {cap_class}">
                <img src="{analise.jogador.foto}" class="jogador-foto">
                <div style="color: white; font-weight: 700; font-size: 14px;">{analise.jogador.apelido}</div>
                <div style="color: #2ed573; font-size: 12px;">{analise.score:.0f} pts</div>
                {'<div style="color: #ffd700; font-size: 20px;">👑</div>' if is_cap else ''}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Técnico
    if por_posicao[6]:
        st.markdown('<div class="campo-linha">', unsafe_allow_html=True)
        for analise in por_posicao[6]:
            is_cap = (analise == capitao)
            cap_class = "capitao" if is_cap else ""
            st.markdown(f"""
            <div class="jogador-campo {cap_class}">
                <img src="{analise.jogador.foto}" class="jogador-foto">
                <div style="color: white; font-weight: 700; font-size: 14px;">{analise.jogador.apelido}</div>
                <div style="color: #2ed573; font-size: 12px;">{analise.score:.0f} pts</div>
                {'<div style="color: #ffd700; font-size: 20px;">👑</div>' if is_cap else ''}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# APLICAÇÃO PRINCIPAL
# ==============================================================================

def main():
    load_professional_css()
    render_header()

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configurações")

        nome_time = st.text_input(
            "🏆 Nome do seu time:",
            placeholder="Digite o nome do time..."
        )

        st.markdown("---")

        orcamento = st.number_input(
            "💰 Orçamento disponível:",
            min_value=0.0,
            max_value=500.0,
            value=100.0,
            step=1.0,
            format="%.2f"
        )

        formacao = st.selectbox(
            "⚽ Formação:",
            options=["3-4-3", "3-5-2", "4-3-3", "4-4-2", "4-5-1", "5-3-2", "5-4-1"]
        )

        st.markdown("---")
        st.markdown("### 📊 Status da API")

        # Testa conexão
        with st.spinner("Testando conexão..."):
            mercado = CartolaAPI.buscar_mercado()
            if mercado:
                st.success("✅ API Online")
                st.info(f"📈 {len(mercado.get('atletas', []))} jogadores disponíveis")
            else:
                st.error("❌ API Offline")

    # Conteúdo principal
    if not mercado:
        st.error("❌ Não foi possível conectar à API do Cartola FC")
        st.info("Tente novamente em alguns instantes")
        return

    # Processa jogadores
    jogadores = ProcessadorDados.processar_mercado(mercado)

    if not jogadores:
        st.error("❌ Erro ao processar dados dos jogadores")
        return

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏠 MEU TIME", "🚀 GERADOR INTELIGENTE", "📊 RANKING"])

    with tab1:
        if nome_time:
            with st.spinner(f"🔍 Buscando time '{nome_time}'..."):
                time_data = CartolaAPI.buscar_time(nome_time)

            if time_data:
                st.success(f"✅ Time encontrado: **{time_data.get('nome', nome_time)}**")

                # Métricas do time
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-value-large" style="color: #2ed573;">C$ {:.2f}</div>
                        <div class="metric-label-large">Patrimônio</div>
                    </div>
                    """.format(time_data.get('patrimonio', 0)), unsafe_allow_html=True)

                with col2:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-value-large" style="color: #667eea;">{:.1f}</div>
                        <div class="metric-label-large">Pontos</div>
                    </div>
                    """.format(time_data.get('pontos', 0)), unsafe_allow_html=True)

                with col3:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-value-large" style="color: #ff9f43;">{}</div>
                        <div class="metric-label-large">Vitórias</div>
                    </div>
                    """.format(time_data.get('vitorias', 0)), unsafe_allow_html=True)

                with col4:
                    st.markdown("""
                    <div class="metric-card">
                        <div class="metric-value-large" style="color: #764ba2;">#{}</div>
                        <div class="metric-label-large">Posição</div>
                    </div>
                    """.format(time_data.get('posicao', '-')), unsafe_allow_html=True)

                st.markdown("---")

                # Analisa atletas do time
                atletas_time = time_data.get('atletas', [])

                if atletas_time:
                    st.subheader("👥 Análise dos Seus Jogadores")

                    ia = InteligenciaArtificial()

                    for atleta_data in atletas_time:
                        # Busca jogador no mercado
                        atleta_id = atleta_data.get('atleta_id')
                        jogador_encontrado = next((j for j in jogadores if j.atleta_id == atleta_id), None)

                        if jogador_encontrado:
                            analise = ia.analisar_jogador(jogador_encontrado)

                            with st.expander(f"{jogador_encontrado.apelido} - {jogador_encontrado.posicao_nome}"):
                                render_analise_card(analise)
                else:
                    st.info("Time sem jogadores escalados")
            else:
                st.warning(f"⚠️ Time '{nome_time}' não encontrado")
        else:
            st.info("👈 Digite o nome do seu time na barra lateral")

    with tab2:
        st.subheader("🚀 Gerador Inteligente de Times")

        st.markdown("""
        <div class="pro-card">
            <h3 style="color: #667eea; margin-bottom: 15px;">🤖 Como funciona a IA</h3>
            <p style="color: rgba(255,255,255,0.8); line-height: 1.8;">
            O sistema analisa <strong>todos os jogadores disponíveis</strong> usando um algoritmo de otimização matemática que considera:
            </p>
            <ul style="color: rgba(255,255,255,0.7); line-height: 2;">
                <li>📊 <strong>Média de pontos</strong> (peso 40%)</li>
                <li>💰 <strong>Custo-benefício</strong> (peso 25%)</li>
                <li>📈 <strong>Regularidade</strong> (peso 20%)</li>
                <li>🟢 <strong>Status/Condição</strong> (peso 15%)</li>
            </ul>
            <p style="color: rgba(255,255,255,0.8); margin-top: 15px;">
            O algoritmo monta o time que <strong>maximiza o score total</strong> dentro do seu orçamento.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown(f"**💰 Orçamento:** C$ {orcamento:.2f}")
            st.markdown(f"**⚽ Formação:** {formacao}")

        with col2:
            if st.button("🚀 GERAR TIME", type="primary", use_container_width=True):
                with st.spinner("🤖 IA analisando jogadores e otimizando time..."):
                    otimizador = OtimizadorTime(jogadores, orcamento)
                    time_gerado = otimizador.gerar_time(formacao)

                if time_gerado:
                    st.success("✅ Time gerado com sucesso!")
                    st.balloons()

                    # Métricas
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value-large" style="color: #2ed573;">C$ {time_gerado['custo_total']:.2f}</div>
                            <div class="metric-label-large">Custo Total</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value-large" style="color: #ff9f43;">C$ {time_gerado['orcamento_restante']:.2f}</div>
                            <div class="metric-label-large">Restante</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col3:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value-large" style="color: #667eea;">{time_gerado['score_medio']:.1f}</div>
                            <div class="metric-label-large">Score Médio</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col4:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value-large" style="color: #764ba2;">{time_gerado['previsao_pontos']:.1f}</div>
                            <div class="metric-label-large">Previsão</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("---")

                    # Campo de futebol
                    st.subheader("⚽ Visualização do Time")
                    render_campo_futebol(time_gerado)

                    st.markdown("---")

                    # Lista detalhada
                    st.subheader("📋 Análise Detalhada dos Jogadores")

                    for analise in time_gerado['jogadores']:
                        is_capitao = (analise == time_gerado['capitao'])
                        with st.expander(f"{analise.jogador.apelido} - {analise.jogador.posicao_nome} {'👑 CAPITÃO' if is_capitao else ''}"):
                            render_analise_card(analise, is_capitao)
                else:
                    st.error("❌ Não foi possível gerar time com esse orçamento e formação")
                    st.info("💡 Tente aumentar o orçamento ou escolher outra formação")

    with tab3:
        st.subheader("📊 Ranking de Jogadores")

        col1, col2 = st.columns([1, 3])

        with col1:
            posicao_filtro = st.selectbox(
                "Filtrar por posição:",
                options=["Todas"] + list(set(j.posicao_nome for j in jogadores))
            )

        # Filtra jogadores
        if posicao_filtro == "Todas":
            jogadores_filtrados = jogadores
        else:
            jogadores_filtrados = [j for j in jogadores if j.posicao_nome == posicao_filtro]

        # Analisa e ordena
        ia = InteligenciaArtificial()
        analises = [ia.analisar_jogador(j) for j in jogadores_filtrados]
        analises.sort(key=lambda x: x.score, reverse=True)

        st.info(f"📈 Mostrando top 50 de {len(analises)} jogadores")

        # Mostra top 50
        for i, analise in enumerate(analises[:50], 1):
            with st.expander(f"#{i} - {analise.jogador.apelido} (Score: {analise.score:.1f}/100)"):
                render_analise_card(analise)

if __name__ == "__main__":
    main()
