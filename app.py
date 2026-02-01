"""
🧠 ORÁCULO CARTOLA FC - IA INTELIGENTE
Sistema completo de análise e geração de times
"""

import streamlit as st
import pandas as pd
import numpy as np
import requests
from typing import Dict, List, Tuple

st.set_page_config(
    page_title="Oráculo Cartola FC - IA",
    page_icon="🧠",
    layout="wide"
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

FORMACOES = {
    "3-4-3": {"goleiro": 1, "zagueiro": 3, "lateral": 0, "meia": 4, "atacante": 3, "tecnico": 1},
    "3-5-2": {"goleiro": 1, "zagueiro": 3, "lateral": 0, "meia": 5, "atacante": 2, "tecnico": 1},
    "4-3-3": {"goleiro": 1, "zagueiro": 2, "lateral": 2, "meia": 3, "atacante": 3, "tecnico": 1},
    "4-4-2": {"goleiro": 1, "zagueiro": 2, "lateral": 2, "meia": 4, "atacante": 2, "tecnico": 1},
    "4-5-1": {"goleiro": 1, "zagueiro": 2, "lateral": 2, "meia": 5, "atacante": 1, "tecnico": 1},
    "5-3-2": {"goleiro": 1, "zagueiro": 3, "lateral": 2, "meia": 3, "atacante": 2, "tecnico": 1},
    "5-4-1": {"goleiro": 1, "zagueiro": 3, "lateral": 2, "meia": 4, "atacante": 1, "tecnico": 1}
}

# ==============================================================================
# FUNÇÕES DE API
# ==============================================================================

@st.cache_data(ttl=300)
def buscar_mercado():
    """Busca dados do mercado"""
    try:
        response = requests.get("https://api.cartola.globo.com/atletas/mercado", timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

@st.cache_data(ttl=300)
def buscar_partidas():
    """Busca partidas da rodada"""
    try:
        response = requests.get("https://api.cartola.globo.com/partidas", timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

def buscar_time_usuario(slug: str):
    """Busca time do usuário"""
    try:
        response = requests.get(f"https://api.cartola.globo.com/time/slug/{slug}", timeout=10)
        return response.json() if response.status_code == 200 else None
    except:
        return None

# ==============================================================================
# MOTOR DE INTELIGÊNCIA ARTIFICIAL
# ==============================================================================

class AnalisadorIA:
    """IA que analisa e pontua jogadores"""

    def __init__(self, mercado: Dict, partidas: Dict):
        self.mercado = mercado
        self.partidas = partidas
        self.atletas = mercado.get('atletas', [])
        self.clubes = mercado.get('clubes', {})
        self.scouts = mercado.get('scout', {})

    def calcular_score_jogador(self, atleta: Dict) -> Tuple[float, Dict]:
        """
        Calcula score inteligente do jogador (0-100)
        Retorna: (score, explicacao)
        """
        explicacao = {}
        score = 0

        # 1. MÉDIA DE PONTOS (peso 35)
        media = atleta.get('media_num', 0)
        if media > 0:
            score_media = min((media / 10) * 35, 35)
            score += score_media
            explicacao['media'] = f"Média: {media:.1f} pts (+{score_media:.0f})"

        # 2. CUSTO-BENEFÍCIO (peso 25)
        preco = atleta.get('preco_num', 1)
        if preco > 0 and media > 0:
            cb = (media / preco) * 100
            score_cb = min(cb * 2.5, 25)
            score += score_cb
            explicacao['custo_beneficio'] = f"C/B: {cb:.2f} (+{score_cb:.0f})"

        # 3. VALORIZAÇÃO (peso 15)
        variacao = atleta.get('variacao_num', 0)
        if variacao > 0:
            score_val = min(variacao * 3, 15)
            score += score_val
            explicacao['valorizacao'] = f"Subindo {variacao:.1f}% (+{score_val:.0f})"
        elif variacao < 0:
            explicacao['valorizacao'] = f"Caindo {variacao:.1f}%"

        # 4. JOGOS EM CASA (peso 10)
        clube_id = atleta.get('clube_id')
        if clube_id and self.partidas:
            joga_casa = self._joga_em_casa(clube_id)
            if joga_casa:
                score += 10
                explicacao['mando'] = "Joga em casa (+10)"
            else:
                explicacao['mando'] = "Joga fora"

        # 5. MINUTOS JOGADOS (peso 10)
        minutos = atleta.get('minutos_jogados', 0)
        if minutos >= 270:  # 3 jogos completos
            score += 10
            explicacao['minutos'] = f"{minutos} min (+10)"
        elif minutos > 0:
            score_min = (minutos / 270) * 10
            score += score_min
            explicacao['minutos'] = f"{minutos} min (+{score_min:.0f})"

        # 6. STATUS (peso 5)
        status = atleta.get('status_id', 7)
        if status == 7:  # Provável
            score += 5
            explicacao['status'] = "Provável (+5)"
        elif status == 6:  # Dúvida
            score -= 5
            explicacao['status'] = "Dúvida (-5)"
        else:
            score -= 20
            explicacao['status'] = "Não joga (-20)"

        return round(score, 1), explicacao

    def _joga_em_casa(self, clube_id: int) -> bool:
        """Verifica se joga em casa"""
        if not self.partidas or 'partidas' not in self.partidas:
            return False

        for partida in self.partidas['partidas']:
            if partida.get('clube_casa_id') == clube_id:
                return True
        return False

    def rankear_por_posicao(self, posicao_id: int, limite_preco: float = None) -> List[Dict]:
        """Retorna jogadores rankeados por score"""
        jogadores = [a for a in self.atletas if a.get('posicao_id') == posicao_id]

        if limite_preco:
            jogadores = [j for j in jogadores if j.get('preco_num', 999) <= limite_preco]

        # Calcula score para cada um
        jogadores_com_score = []
        for j in jogadores:
            score, explicacao = self.calcular_score_jogador(j)
            j['SCORE_IA'] = score
            j['EXPLICACAO_IA'] = explicacao
            jogadores_com_score.append(j)

        # Ordena por score
        return sorted(jogadores_com_score, key=lambda x: x['SCORE_IA'], reverse=True)

# ==============================================================================
# GERADOR DE TIMES INTELIGENTE
# ==============================================================================

class GeradorTimesIA:
    """Gera o melhor time possível dentro do orçamento"""

    def __init__(self, analisador: AnalisadorIA, orcamento: float):
        self.analisador = analisador
        self.orcamento = orcamento

    def gerar_time_otimizado(self, formacao: str) -> Dict:
        """Gera o melhor time possível"""
        esquema = FORMACOES[formacao]
        time_final = []
        gasto_total = 0

        # Para cada posição, pega os melhores
        for pos_nome, quantidade in esquema.items():
            if quantidade == 0:
                continue

            # Mapeia nome para ID
            pos_id = self._nome_para_id(pos_nome)
            orcamento_restante = self.orcamento - gasto_total
            limite_por_jogador = orcamento_restante / (12 - len(time_final))

            # Busca melhores da posição
            melhores = self.analisador.rankear_por_posicao(pos_id, limite_por_jogador)

            # Seleciona a quantidade necessária
            for i in range(quantidade):
                if i < len(melhores):
                    jogador = melhores[i]
                    time_final.append(jogador)
                    gasto_total += jogador.get('preco_num', 0)

        # Escolhe capitão (maior score)
        if time_final:
            capitao = max(time_final, key=lambda x: x['SCORE_IA'])

            return {
                'sucesso': True,
                'time': time_final,
                'capitao': capitao,
                'custo_total': gasto_total,
                'economia': self.orcamento - gasto_total,
                'score_medio': np.mean([j['SCORE_IA'] for j in time_final])
            }

        return {'sucesso': False}

    def _nome_para_id(self, nome: str) -> int:
        """Converte nome da posição para ID"""
        mapa = {
            'goleiro': 1,
            'lateral': 2,
            'zagueiro': 3,
            'meia': 4,
            'atacante': 5,
            'tecnico': 6
        }
        return mapa.get(nome, 1)

# ==============================================================================
# INTERFACE
# ==============================================================================

def main():
    st.title("🧠 ORÁCULO CARTOLA FC - IA INTELIGENTE")
    st.markdown("---")

    # SIDEBAR
    with st.sidebar:
        st.header("⚙️ Configurações")
        slug = st.text_input("🔍 Nome do Time", placeholder="ex: meu-time-fc")

        if st.button("🚀 BUSCAR TIME", type="primary", use_container_width=True):
            if slug:
                with st.spinner("Buscando..."):
                    user_data = buscar_time_usuario(slug)
                    if user_data and 'time' in user_data:
                        st.session_state['user_data'] = user_data
                        st.success("✅ Time encontrado!")
                    else:
                        st.error("❌ Time não encontrado")

    # CONTEÚDO PRINCIPAL
    if 'user_data' in st.session_state:
        user_data = st.session_state['user_data']
        patrimonio = user_data.get('patrimonio', 100)

        st.success(f"**Time:** {user_data['time']['nome']} | **Patrimônio:** C$ {patrimonio:.2f}")

        # Busca dados
        mercado = buscar_mercado()
        partidas = buscar_partidas()

        if mercado:
            analisador = AnalisadorIA(mercado, partidas)
            gerador = GeradorTimesIA(analisador, patrimonio)

            # TABS
            tab1, tab2 = st.tabs(["🤖 GERADOR INTELIGENTE", "📊 ANÁLISE DE JOGADORES"])

            with tab1:
                st.subheader("🤖 Gerador Automático com IA")

                col1, col2 = st.columns([2, 1])
                with col1:
                    formacao = st.selectbox("Escolha a formação", list(FORMACOES.keys()))
                with col2:
                    if st.button("⚡ GERAR TIME", type="primary", use_container_width=True):
                        with st.spinner("IA analisando 800+ jogadores..."):
                            resultado = gerador.gerar_time_otimizado(formacao)

                            if resultado['sucesso']:
                                st.session_state['time_gerado'] = resultado
                                st.balloons()

                # Mostra time gerado
                if 'time_gerado' in st.session_state:
                    res = st.session_state['time_gerado']

                    # Métricas
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("💰 Custo Total", f"C$ {res['custo_total']:.2f}")
                    with col2:
                        st.metric("💵 Economia", f"C$ {res['economia']:.2f}")
                    with col3:
                        st.metric("📊 Score Médio", f"{res['score_medio']:.1f}/100")
                    with col4:
                        st.metric("👑 Capitão", res['capitao']['apelido'])

                    st.markdown("---")
                    st.subheader("⚽ Escalação Gerada")

                    # Tabela de jogadores
                    dados_tabela = []
                    for j in res['time']:
                        dados_tabela.append({
                            'Jogador': j['apelido'],
                            'Posição': POSICOES[j['posicao_id']],
                            'Clube': mercado['clubes'][str(j['clube_id'])]['nome'],
                            'Preço': f"C$ {j['preco_num']:.2f}",
                            'Média': f"{j.get('media_num', 0):.1f}",
                            'Score IA': f"{j['SCORE_IA']:.1f}/100",
                            'Capitão': '👑' if j['atleta_id'] == res['capitao']['atleta_id'] else ''
                        })

                    df = pd.DataFrame(dados_tabela)
                    st.dataframe(df, use_container_width=True, hide_index=True)

                    # Explicações
                    st.markdown("---")
                    st.subheader("🧠 Por que a IA escolheu esses jogadores?")

                    for j in res['time']:
                        with st.expander(f"⚽ {j['apelido']} - Score: {j['SCORE_IA']:.1f}/100"):
                            explicacao = j['EXPLICACAO_IA']
                            for chave, texto in explicacao.items():
                                st.write(f"• {texto}")

            with tab2:
                st.subheader("📊 Análise de Jogadores por Posição")

                posicao_escolhida = st.selectbox(
                    "Escolha a posição",
                    options=list(POSICOES.keys()),
                    format_func=lambda x: POSICOES[x]
                )

                limite = st.slider("Preço máximo", 0.0, 50.0, 20.0, 0.5)

                if st.button("🔍 ANALISAR", type="primary"):
                    with st.spinner("Analisando..."):
                        ranking = analisador.rankear_por_posicao(posicao_escolhida, limite)

                        st.success(f"✅ Encontrados {len(ranking)} jogadores")

                        # Top 10
                        for i, j in enumerate(ranking[:10], 1):
                            with st.expander(f"#{i} - {j['apelido']} (Score: {j['SCORE_IA']:.1f}/100)"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"**Clube:** {mercado['clubes'][str(j['clube_id'])]['nome']}")
                                    st.write(f"**Preço:** C$ {j['preco_num']:.2f}")
                                    st.write(f"**Média:** {j.get('media_num', 0):.1f} pts")
                                with col2:
                                    st.write("**Análise da IA:**")
                                    for texto in j['EXPLICACAO_IA'].values():
                                        st.write(f"• {texto}")
        else:
            st.error("❌ Erro ao buscar dados do mercado")
    else:
        st.info("👈 Digite o nome do seu time na barra lateral para começar")

if __name__ == "__main__":
    main()
