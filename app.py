"""
🧠 ORÁCULO CARTOLA FC - VERSÃO PROFISSIONAL
Sistema Inteligente de Análise e Geração de Times
Desenvolvido com arquitetura robusta e tratamento de erros
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json

# ==============================================================================
# CONFIGURAÇÃO
# ==============================================================================

st.set_page_config(
    page_title="Oráculo Cartola FC",
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

POSICOES_SLUG = {
    1: "goleiro",
    2: "lateral",
    3: "zagueiro",
    4: "meia",
    5: "atacante",
    6: "tecnico"
}

FORMACOES = {
    "3-4-3": {"goleiro": 1, "zagueiro": 3, "lateral": 0, "meia": 4, "atacante": 3, "tecnico": 1},
    "3-5-2": {"goleiro": 1, "zagueiro": 3, "lateral": 0, "meia": 5, "atacante": 2, "tecnico": 1},
    "4-3-3": {"goleiro": 1, "zagueiro": 2, "lateral": 2, "meia": 3, "atacante": 3, "tecnico": 1},
    "4-4-2": {"goleiro": 1, "zagueiro": 2, "lateral": 2, "meia": 4, "atacante": 2, "tecnico": 1},
    "4-5-1": {"goleiro": 1, "zagueiro": 2, "lateral": 2, "meia": 5, "atacante": 1, "tecnico": 1},
    "5-3-2": {"goleiro": 1, "zagueiro": 3, "lateral": 2, "meia": 3, "atacante": 2, "tecnico": 1},
    "5-4-1": {"goleiro": 1, "zagueiro": 3, "lateral": 2, "meia": 4, "atacante": 1, "tecnico": 1}
}

STATUS_JOGADOR = {
    7: ("Provável", "🟢", "success"),
    6: ("Dúvida", "🟡", "warning"),
    5: ("Lesionado", "🔴", "error"),
    3: ("Suspenso", "🔴", "error"),
    2: ("Nulo", "⚫", "error")
}

# ==============================================================================
# DATACLASSES
# ==============================================================================

@dataclass
class Jogador:
    """Representa um jogador com todos os dados necessários"""
    atleta_id: int
    apelido: str
    nome: str
    clube_id: int
    clube_nome: str
    posicao_id: int
    posicao_nome: str
    preco: float
    media: float
    pontos_rodada: float
    status_id: int
    status_nome: str
    jogos_num: int
    scout: Dict
    foto: str

    def __post_init__(self):
        """Validação e conversão de tipos"""
        self.preco = float(self.preco)
        self.media = float(self.media) if self.media else 0.0
        self.pontos_rodada = float(self.pontos_rodada) if self.pontos_rodada else 0.0
        self.jogos_num = int(self.jogos_num) if self.jogos_num else 0

@dataclass
class AnaliseJogador:
    """Resultado da análise de um jogador"""
    jogador: Jogador
    score_ia: float
    custo_beneficio: float
    tendencia: str
    explicacao: List[str]
    recomendacao: str

# ==============================================================================
# API CLIENT
# ==============================================================================

class CartolaAPI:
    """Cliente profissional para API do Cartola FC"""

    BASE_URL = "https://api.cartola.globo.com"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    }

    @classmethod
    @st.cache_data(ttl=300)
    def get(cls, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Faz requisição GET com tratamento robusto de erros"""
        url = f"{cls.BASE_URL}/{endpoint}"

        try:
            response = requests.get(
                url, 
                headers=cls.HEADERS, 
                params=params, 
                timeout=15
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            st.error("⏱️ Timeout na API do Cartola FC")
            return None

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None
            st.error(f"❌ Erro HTTP {e.response.status_code}")
            return None

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erro na requisição: {str(e)}")
            return None

        except json.JSONDecodeError:
            st.error("❌ Resposta inválida da API")
            return None

    @classmethod
    def buscar_mercado(cls) -> Optional[Dict]:
        """Busca dados completos do mercado"""
        return cls.get("atletas/mercado")

    @classmethod
    def buscar_time_por_nome(cls, nome: str) -> Optional[Dict]:
        """Busca time por nome"""
        if not nome or len(nome.strip()) < 3:
            return None

        # Busca por nome
        resultados = cls.get("times", params={"q": nome.strip()})

        if resultados and isinstance(resultados, list) and len(resultados) > 0:
            time_id = resultados[0].get('time_id')
            if time_id:
                return cls.get(f"time/id/{time_id}")

        # Tenta buscar por slug
        return cls.get(f"time/slug/{nome.strip()}")

    @classmethod
    def buscar_partidas(cls) -> Optional[Dict]:
        """Busca partidas da rodada"""
        return cls.get("partidas")

# ==============================================================================
# PROCESSADOR DE DADOS
# ==============================================================================

class ProcessadorMercado:
    """Processa dados do mercado em estruturas otimizadas"""

    @staticmethod
    def processar(mercado: Dict) -> Tuple[Dict[int, Jogador], Dict[int, str], Dict[int, Dict]]:
        """
        Processa mercado e retorna:
        - Dict de jogadores por ID
        - Dict de clubes por ID
        - Dict de status por clube
        """
        jogadores = {}
        clubes = {}
        status_clubes = {}

        # Processa clubes
        for clube_id, clube_data in mercado.get('clubes', {}).items():
            clubes[int(clube_id)] = clube_data.get('nome', 'Desconhecido')

        # Processa status
        for clube_id, status_data in mercado.get('status', {}).items():
            status_clubes[int(clube_id)] = status_data

        # Processa atletas
        for atleta_data in mercado.get('atletas', []):
            try:
                atleta_id = int(atleta_data['atleta_id'])
                clube_id = int(atleta_data['clube_id'])
                posicao_id = int(atleta_data['posicao_id'])

                jogador = Jogador(
                    atleta_id=atleta_id,
                    apelido=atleta_data.get('apelido', 'Sem nome'),
                    nome=atleta_data.get('nome', 'Sem nome'),
                    clube_id=clube_id,
                    clube_nome=clubes.get(clube_id, 'Desconhecido'),
                    posicao_id=posicao_id,
                    posicao_nome=POSICOES.get(posicao_id, 'Desconhecida'),
                    preco=atleta_data.get('preco_num', 0),
                    media=atleta_data.get('media_num', 0),
                    pontos_rodada=atleta_data.get('pontos_num', 0),
                    status_id=atleta_data.get('status_id', 7),
                    status_nome=STATUS_JOGADOR.get(atleta_data.get('status_id', 7), ("Desconhecido", "⚪", "info"))[0],
                    jogos_num=atleta_data.get('jogos_num', 0),
                    scout=atleta_data.get('scout', {}),
                    foto=atleta_data.get('foto', '').replace('FORMATO', '140x140')
                )

                jogadores[atleta_id] = jogador

            except (KeyError, ValueError, TypeError) as e:
                continue  # Pula atletas com dados inválidos

        return jogadores, clubes, status_clubes

# ==============================================================================
# MOTOR DE IA
# ==============================================================================

class MotorIA:
    """Motor de Inteligência Artificial para análise de jogadores"""

    @staticmethod
    def calcular_score(jogador: Jogador, status_clube: Optional[Dict] = None) -> float:
        """
        Calcula score de 0 a 100 baseado em múltiplos fatores
        """
        score = 0.0

        # 1. MÉDIA DE PONTOS (40 pontos)
        if jogador.media > 0:
            score += min(jogador.media * 4, 40)

        # 2. CUSTO-BENEFÍCIO (25 pontos)
        if jogador.preco > 0 and jogador.media > 0:
            cb = (jogador.media / jogador.preco) * 100
            score += min(cb * 2.5, 25)

        # 3. STATUS (20 pontos)
        if jogador.status_id == 7:  # Provável
            score += 20
        elif jogador.status_id == 6:  # Dúvida
            score += 10

        # 4. JOGOS DISPUTADOS (10 pontos)
        if jogador.jogos_num > 0:
            score += min(jogador.jogos_num * 2, 10)

        # 5. PONTOS NA RODADA (5 pontos)
        if jogador.pontos_rodada > 0:
            score += min(jogador.pontos_rodada / 2, 5)

        return min(score, 100)

    @staticmethod
    def analisar_jogador(jogador: Jogador, status_clube: Optional[Dict] = None) -> AnaliseJogador:
        """Análise completa de um jogador"""

        score = MotorIA.calcular_score(jogador, status_clube)
        cb = (jogador.media / jogador.preco) if jogador.preco > 0 else 0

        explicacao = []

        # Análise de média
        if jogador.media >= 8:
            explicacao.append(f"📈 Excelente média: {jogador.media:.1f} pontos")
        elif jogador.media >= 5:
            explicacao.append(f"📊 Média razoável: {jogador.media:.1f} pontos")
        elif jogador.media > 0:
            explicacao.append(f"📉 Média baixa: {jogador.media:.1f} pontos")
        else:
            explicacao.append("⚠️ Sem média (não jogou)")

        # Análise de custo-benefício
        if cb >= 0.5:
            explicacao.append(f"💎 Ótimo custo-benefício: {cb:.2f}")
        elif cb >= 0.3:
            explicacao.append(f"💰 Custo-benefício aceitável: {cb:.2f}")
        elif cb > 0:
            explicacao.append(f"💸 Custo-benefício ruim: {cb:.2f}")

        # Análise de status
        status_info = STATUS_JOGADOR.get(jogador.status_id, ("Desconhecido", "⚪", "info"))
        explicacao.append(f"{status_info[1]} Status: {status_info[0]}")

        # Análise de jogos
        if jogador.jogos_num >= 5:
            explicacao.append(f"✅ Jogou {jogador.jogos_num} partidas (regular)")
        elif jogador.jogos_num > 0:
            explicacao.append(f"⚠️ Jogou apenas {jogador.jogos_num} partidas")
        else:
            explicacao.append("❌ Não jogou nenhuma partida")

        # Tendência
        if jogador.pontos_rodada > jogador.media:
            tendencia = "📈 Em alta"
        elif jogador.pontos_rodada < jogador.media and jogador.pontos_rodada > 0:
            tendencia = "📉 Em baixa"
        else:
            tendencia = "➡️ Estável"

        # Recomendação
        if score >= 70:
            recomendacao = "🟢 RECOMENDADO"
        elif score >= 50:
            recomendacao = "🟡 CONSIDERAR"
        elif score >= 30:
            recomendacao = "🟠 ATENÇÃO"
        else:
            recomendacao = "🔴 EVITAR"

        return AnaliseJogador(
            jogador=jogador,
            score_ia=score,
            custo_beneficio=cb,
            tendencia=tendencia,
            explicacao=explicacao,
            recomendacao=recomendacao
        )

# ==============================================================================
# GERADOR DE TIMES
# ==============================================================================

class GeradorTimes:
    """Gerador inteligente de times otimizados"""

    def __init__(self, jogadores: Dict[int, Jogador], orcamento: float):
        self.jogadores = jogadores
        self.orcamento = orcamento
        self.motor_ia = MotorIA()

    def gerar(self, formacao: str) -> Optional[Dict]:
        """Gera time otimizado para a formação"""

        esquema = FORMACOES.get(formacao)
        if not esquema:
            return None

        time_gerado = []
        custo_total = 0.0

        # Para cada posição na formação
        for posicao_id, posicao_nome in POSICOES.items():
            posicao_slug = POSICOES_SLUG[posicao_id]
            quantidade = esquema.get(posicao_slug, 0)

            if quantidade == 0:
                continue

            # Filtra jogadores da posição
            candidatos = [
                j for j in self.jogadores.values()
                if j.posicao_id == posicao_id and j.status_id in [6, 7]
            ]

            # Analisa e ordena por score
            analises = [self.motor_ia.analisar_jogador(j) for j in candidatos]
            analises.sort(key=lambda x: x.score_ia, reverse=True)

            # Seleciona os melhores que cabem no orçamento
            selecionados = 0
            for analise in analises:
                if selecionados >= quantidade:
                    break

                if custo_total + analise.jogador.preco <= self.orcamento:
                    time_gerado.append(analise)
                    custo_total += analise.jogador.preco
                    selecionados += 1

        # Verifica se conseguiu montar time completo
        if len(time_gerado) != 12:
            return None

        # Escolhe capitão (maior score)
        time_gerado.sort(key=lambda x: x.score_ia, reverse=True)
        capitao = time_gerado[0]

        return {
            'jogadores': time_gerado,
            'capitao': capitao,
            'custo_total': custo_total,
            'orcamento_restante': self.orcamento - custo_total,
            'formacao': formacao,
            'score_medio': np.mean([j.score_ia for j in time_gerado]),
            'previsao_pontos': sum([j.jogador.media * (2 if j == capitao else 1) for j in time_gerado])
        }

# ==============================================================================
# INTERFACE
# ==============================================================================

def render_css():
    """CSS profissional"""
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
        }
        .main-title {
            color: white;
            font-size: 2.5rem;
            font-weight: 900;
            margin: 0;
        }
        .player-card {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        .score-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.2rem;
        }
        .score-excellent { background: #28a745; color: white; }
        .score-good { background: #17a2b8; color: white; }
        .score-warning { background: #ffc107; color: black; }
        .score-danger { background: #dc3545; color: white; }
    </style>
    """, unsafe_allow_html=True)

def render_analise_jogador(analise: AnaliseJogador, is_capitao: bool = False):
    """Renderiza card de análise de jogador"""

    j = analise.jogador

    # Define cor do score
    if analise.score_ia >= 70:
        score_class = "score-excellent"
    elif analise.score_ia >= 50:
        score_class = "score-good"
    elif analise.score_ia >= 30:
        score_class = "score-warning"
    else:
        score_class = "score-danger"

    capitao_badge = "👑 CAPITÃO" if is_capitao else ""

    st.markdown(f"""
    <div class="player-card">
        <h4>{j.apelido} {capitao_badge}</h4>
        <p><strong>{j.posicao_nome}</strong> • {j.clube_nome}</p>
        <span class="score-badge {score_class}">Score: {analise.score_ia:.1f}/100</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Preço", f"C$ {j.preco:.2f}")
    with col2:
        st.metric("📊 Média", f"{j.media:.1f}")
    with col3:
        st.metric("⚽ Última", f"{j.pontos_rodada:.1f}")

    st.write("**🧠 Análise da IA:**")
    for exp in analise.explicacao:
        st.write(f"• {exp}")

    st.write(f"**{analise.recomendacao}** • {analise.tendencia}")

# ==============================================================================
# MAIN
# ==============================================================================

def main():
    render_css()

    st.markdown('<div class="main-header"><h1 class="main-title">🧠 ORÁCULO CARTOLA FC</h1><p style="color: white;">Sistema Profissional de Análise com IA</p></div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configurações")
        nome_time = st.text_input("🔍 Nome do seu time:", placeholder="Digite o nome...")

        st.markdown("---")
        st.markdown("### 📊 Sobre o Sistema")
        st.info("""
        **Motor de IA analisa:**
        • Média de pontos
        • Custo-benefício
        • Status do jogador
        • Regularidade
        • Tendência
        """)

    # Busca mercado
    with st.spinner("🔄 Carregando dados do mercado..."):
        mercado = CartolaAPI.buscar_mercado()

    if not mercado:
        st.error("❌ Erro ao carregar mercado")
        return

    # Processa mercado
    jogadores, clubes, status_clubes = ProcessadorMercado.processar(mercado)
    st.success(f"✅ {len(jogadores)} jogadores carregados")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏠 Meu Time", "🤖 Gerador IA", "📊 Ranking"])

    with tab1:
        if nome_time:
            with st.spinner(f"🔍 Buscando time '{nome_time}'..."):
                time_user = CartolaAPI.buscar_time_por_nome(nome_time)

            if time_user:
                st.success(f"✅ Time encontrado: {time_user.get('nome', 'Sem nome')}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("💰 Patrimônio", f"C$ {time_user.get('patrimonio', 0):.2f}")
                with col2:
                    st.metric("📊 Pontos", time_user.get('pontos', 0))
                with col3:
                    st.metric("🏆 Posição", f"#{time_user.get('posicao_geral', 0):,}")

                st.markdown("---")
                st.subheader("👥 Análise dos Jogadores")

                # Extrai atletas do time
                atletas_time = []
                if 'atletas' in time_user:
                    if isinstance(time_user['atletas'], dict):
                        atletas_time = list(time_user['atletas'].values())
                    elif isinstance(time_user['atletas'], list):
                        atletas_time = time_user['atletas']

                capitao_id = time_user.get('capitao_id')

                if atletas_time:
                    for atleta_data in atletas_time:
                        atleta_id = int(atleta_data.get('atleta_id', 0))

                        if atleta_id in jogadores:
                            jogador = jogadores[atleta_id]
                            analise = MotorIA.analisar_jogador(jogador)

                            with st.expander(f"{jogador.apelido} - {jogador.posicao_nome}"):
                                render_analise_jogador(analise, atleta_id == capitao_id)
                        else:
                            st.warning(f"⚠️ Jogador ID {atleta_id} não encontrado no mercado")
                else:
                    st.warning("⚠️ Nenhum atleta encontrado no time")
            else:
                st.error("❌ Time não encontrado")
        else:
            st.info("👈 Digite o nome do seu time na barra lateral")

    with tab2:
        st.subheader("🤖 Gerador Inteligente de Times")

        col1, col2 = st.columns(2)
        with col1:
            orcamento = st.number_input(
                "💰 Orçamento disponível:",
                min_value=0.0,
                max_value=500.0,
                value=100.0,
                step=1.0,
                format="%.2f"
            )
        with col2:
            formacao = st.selectbox(
                "⚽ Escolha a formação:",
                options=list(FORMACOES.keys())
            )

        if st.button("🚀 GERAR TIME OTIMIZADO", type="primary", use_container_width=True):
            with st.spinner("🤖 IA gerando time otimizado..."):
                gerador = GeradorTimes(jogadores, orcamento)
                time_gerado = gerador.gerar(formacao)

            if time_gerado:
                st.success("✅ Time gerado com sucesso!")
                st.balloons()

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("💰 Custo Total", f"C$ {time_gerado['custo_total']:.2f}")
                with col2:
                    st.metric("💵 Restante", f"C$ {time_gerado['orcamento_restante']:.2f}")
                with col3:
                    st.metric("📊 Score Médio", f"{time_gerado['score_medio']:.1f}/100")
                with col4:
                    st.metric("🎯 Previsão", f"{time_gerado['previsao_pontos']:.1f} pts")

                st.markdown("---")
                st.subheader(f"👑 Capitão: {time_gerado['capitao'].jogador.apelido}")

                st.markdown("---")
                st.subheader("👥 Escalação Completa")

                for analise in time_gerado['jogadores']:
                    is_capitao = (analise == time_gerado['capitao'])
                    with st.expander(f"{analise.jogador.apelido} - {analise.jogador.posicao_nome} {'👑' if is_capitao else ''}"):
                        render_analise_jogador(analise, is_capitao)
            else:
                st.error("❌ Não foi possível gerar time com esse orçamento e formação")

    with tab3:
        st.subheader("📊 Ranking de Jogadores por Posição")

        posicao_filtro = st.selectbox(
            "Escolha a posição:",
            options=list(POSICOES.values())
        )

        posicao_id = [k for k, v in POSICOES.items() if v == posicao_filtro][0]

        candidatos = [j for j in jogadores.values() if j.posicao_id == posicao_id]
        analises = [MotorIA.analisar_jogador(j) for j in candidatos]
        analises.sort(key=lambda x: x.score_ia, reverse=True)

        st.write(f"**{len(analises)} jogadores encontrados**")

        for i, analise in enumerate(analises[:20], 1):
            with st.expander(f"#{i} - {analise.jogador.apelido} (Score: {analise.score_ia:.1f})"):
                render_analise_jogador(analise)

if __name__ == "__main__":
    main()
