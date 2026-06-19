import streamlit as st
import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

# ================== CONFIGURAÇÃO INICIAL ==================
st.set_page_config(
    page_title="Ohana Studio",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "ohana_data.json"

DEFAULT_DATA = {
    "looks": {},
    "prompts": [
        {"nome": "Prompt Base Fashion", "categoria": "Modelo IA", "texto": "Fashion editorial, full body, elegant pose, pastel background, soft lighting, 8k"},
        {"nome": "Prompt Carrossel", "categoria": "Carrossel", "texto": "Crie 5 slides sobre tendências de moda primavera, tons rosa e lavanda"},
        {"nome": "Prompt Reels", "categoria": "Reels", "texto": "Roteiro de 15s mostrando transformação do inspo para look final, música trendy"},
    ],
    "pinterest": [
        {"nome": "Inspo Verão", "url": "https://pinterest.com/exemplo1"},
        {"nome": "Casual Chic", "url": "https://pinterest.com/exemplo2"},
    ],
    "shopee": [
        {"nome": "Vestido Floral", "url": "https://shopee.com/exemplo1"},
        {"nome": "Blusa Linho", "url": "https://shopee.com/exemplo2"},
    ],
    "modelos": [
        {
            "nome": "Magra",
            "tipo": "Magra",
            "descricao": "Modelo feminino, corpo magro, 1.70m, estilo editorial fashion.",
            "prompt": "Slim female model, full body, elegant fashion pose, studio lighting"
        },
        {
            "nome": "Plus Size",
            "tipo": "Plus Size",
            "descricao": "Modelo feminino, corpo plus size, 1.65m, estilo empoderado e elegante.",
            "prompt": "Plus size female model, full body, confident fashion pose, soft lighting"
        },
    ]
}

ETAPAS = [
    ("Pinterest Inspo", "📌", "link"),
    ("Curadoria Shopee", "🛍️", "link"),
    ("Gerar Modelo IA", "🤖", "prompt"),
    ("Modelo + Curadoria", "🎨", "prompt"),
    ("Gerar 3-4 Poses", "📸", "prompt"),
    ("Gerar Carrossel", "🎠", "prompt"),
    ("Gerar Vídeo", "🎬", "prompt"),
    ("Gerar Reels", "📱", "prompt"),
    ("Stories (Inspo vs Ohana)", "📖", "prompt"),
]

DIAS_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

CORES = {
    "primario": "#1B4332",       # verde escuro logo
    "secundario": "#C9A96E",     # dourado/creme
    "bg": "#F5F0E8",             # bege off-white
    "bg_card": "#FFFFFF",
    "texto": "#1A1A1A",
    "texto_suave": "#5C5C5C",
    "verde": "#2D6A4F",
    "vermelho": "#C0392B",
    "amarelo": "#B7860B",
    "borda": "#E0D8CC",
}

# ================== PERSISTÊNCIA ==================
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for key in DEFAULT_DATA:
                    if key not in data:
                        data[key] = DEFAULT_DATA[key]
                return data
        except Exception:
            return DEFAULT_DATA.copy()
    return DEFAULT_DATA.copy()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_data():
    if "data" not in st.session_state:
        st.session_state["data"] = load_data()
    return st.session_state["data"]


def save_and_reload(data):
    save_data(data)
    st.session_state["data"] = data
    st.rerun()


# ================== CSS ==================
def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
        background-color: {CORES['bg']} !important;
        color: {CORES['texto']} !important;
    }}

    /* Fundo geral */
    .stApp {{
        background-color: {CORES['bg']} !important;
    }}

    .ohana-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.6rem;
        font-weight: 700;
        color: {CORES['primario']};
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.1rem;
        line-height: 1.1;
    }}

    .ohana-brand {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
        font-weight: 400;
        color: {CORES['secundario']};
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }}

    .ohana-subtitle {{
        color: {CORES['texto_suave']};
        font-weight: 400;
        font-size: 0.95rem;
        margin-bottom: 1rem;
        letter-spacing: 0.02em;
    }}

    .ohana-card {{
        background: {CORES['bg_card']};
        border-radius: 4px;
        padding: 1.2rem 1.4rem;
        border: 1px solid {CORES['borda']};
        margin-bottom: 0.8rem;
        border-left: 3px solid {CORES['primario']};
    }}

    .dia-card {{
        background: {CORES['bg_card']};
        border-radius: 4px;
        padding: 1rem;
        min-height: 130px;
        border: 1px solid {CORES['borda']};
        border-top: 3px solid {CORES['primario']};
        margin-bottom: 0.5rem;
    }}

    .footer {{
        text-align: center;
        padding: 2rem 1rem;
        color: {CORES['texto_suave']};
        font-size: 0.8rem;
        margin-top: 2rem;
        border-top: 1px solid {CORES['borda']};
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }}

    div.stButton > button {{
        border-radius: 2px;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-size: 0.82rem;
        border: 1px solid {CORES['primario']} !important;
        color: {CORES['primario']} !important;
        background: transparent !important;
        transition: all 0.2s ease;
    }}

    div.stButton > button:hover {{
        background: {CORES['primario']} !important;
        color: white !important;
    }}

    div.stButton > button[kind="primary"] {{
        background: {CORES['primario']} !important;
        color: white !important;
    }}

    div.stButton > button[kind="primary"]:hover {{
        background: {CORES['secundario']} !important;
        border-color: {CORES['secundario']} !important;
        color: white !important;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: {CORES['primario']} !important;
    }}

    section[data-testid="stSidebar"] * {{
        color: white !important;
    }}

    section[data-testid="stSidebar"] div.stButton > button {{
        border-color: rgba(255,255,255,0.3) !important;
        color: white !important;
        background: transparent !important;
    }}

    section[data-testid="stSidebar"] div.stButton > button:hover {{
        background: rgba(255,255,255,0.15) !important;
        border-color: white !important;
    }}

    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        border-radius: 2px !important;
        border: 1px solid {CORES['borda']} !important;
        background: white !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab"] {{
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}

    .stTabs [aria-selected="true"] {{
        color: {CORES['primario']} !important;
        border-bottom-color: {CORES['primario']} !important;
    }}

    /* Progress bar */
    .stProgress > div > div > div > div {{
        background-color: {CORES['primario']} !important;
    }}

    hr {{
        border-color: {CORES['borda']} !important;
    }}
    </style>
    """, unsafe_allow_html=True)


# ================== HELPERS ==================
def get_look(data, dia):
    if dia not in data["looks"]:
        data["looks"][dia] = {
            "nome": "",
            "modelo": "Magra",
            "etapas": {nome: {"concluida": False, "valor": ""} for nome, _, _ in ETAPAS},
            "criado_em": datetime.now().isoformat(),
            "atualizado_em": datetime.now().isoformat(),
            "finalizado": False,
        }
    return data["looks"][dia]


def calcular_progresso(look):
    total = len(ETAPAS)
    concluidas = sum(1 for e in look["etapas"].values() if e["concluida"])
    return concluidas / total


def status_dia(look):
    progresso = calcular_progresso(look)
    if look.get("finalizado") or progresso >= 1.0:
        return "●", CORES["verde"], "Finalizado"
    elif progresso >= 0.5:
        return "●", CORES["amarelo"], "Em andamento"
    elif progresso > 0:
        return "●", CORES["vermelho"], "Iniciado"
    return "○", CORES["borda"], "Vazio"


def looks_por_semana(data):
    semanas = defaultdict(list)
    for dia, look in data["looks"].items():
        if look.get("finalizado") or calcular_progresso(look) >= 1.0:
            dt = datetime.fromisoformat(look.get("atualizado_em", datetime.now().isoformat()))
            inicio = dt - timedelta(days=dt.weekday())
            chave = inicio.strftime("%d/%m/%Y")
            semanas[chave].append((dia, look))
    return semanas


# ================== PÁGINAS ==================
def page_dashboard(data):
    st.markdown("<div class='ohana-title'>Ohana</div><div class='ohana-brand'>Lifestyle · Studio</div>", unsafe_allow_html=True)
    st.markdown("<div class='ohana-subtitle'>Curadoria de moda feminina</div>", unsafe_allow_html=True)
    st.markdown("---")

    total_looks = len(data["looks"])
    finalizados = sum(1 for l in data["looks"].values() if l.get("finalizado") or calcular_progresso(l) >= 1.0)
    em_andamento = sum(1 for l in data["looks"].values() if 0 < calcular_progresso(l) < 1)
    atrasados = sum(1 for l in data["looks"].values() if 0 < calcular_progresso(l) < 0.5 and not l.get("finalizado"))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ativos", em_andamento)
    c2.metric("Finalizados", finalizados)
    c3.metric("Atrasados", atrasados)
    c4.metric("Total", total_looks)

    st.markdown("### Calendário Semanal")
    cols = st.columns(7)
    for i, dia in enumerate(DIAS_SEMANA):
        look = get_look(data, dia)
        emoji, cor, label = status_dia(look)
        with cols[i]:
            st.markdown(f"""
            <div class='dia-card'>
                <div style='font-weight:600; color:{CORES['primario']}; font-size:0.78rem; letter-spacing:0.08em; text-transform:uppercase;'>{dia}</div>
                <div style='font-size:1.4rem; margin:0.5rem 0; color:{cor};'>{emoji}</div>
                <div style='font-size:0.72rem; color:{cor}; letter-spacing:0.03em; font-weight:500;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Abrir", key=f"dash_{dia}", use_container_width=True):
                st.session_state["pagina"] = "Criar Look"
                st.session_state["dia_selecionado"] = dia
                st.rerun()

    st.markdown("### Prioridade do Dia")
    prioridade = None
    for dia in DIAS_SEMANA:
        look = get_look(data, dia)
        prog = calcular_progresso(look)
        if 0 < prog < 1 and not look.get("finalizado"):
            prioridade = (dia, look)
            break

    if prioridade:
        dia, look = prioridade
        prog = calcular_progresso(look)
        st.markdown(f"""
        <div class='ohana-card'>
            <b>{dia}</b> — {look.get('nome') or 'Look sem nome'} &nbsp;|&nbsp; Modelo: {look.get('modelo', 'Magra')}
        </div>
        """, unsafe_allow_html=True)
        st.progress(prog, text=f"{int(prog * 100)}% concluído")
        if st.button("Continuar este look", type="primary"):
            st.session_state["pagina"] = "Criar Look"
            st.session_state["dia_selecionado"] = dia
            st.rerun()
    else:
        st.info("Nenhum look em andamento. Crie um novo look na aba 'Criar Look'.")

    st.markdown("### Andamento Geral")
    cards = [(dia, get_look(data, dia)) for dia in DIAS_SEMANA if calcular_progresso(get_look(data, dia)) > 0]
    if not cards:
        st.info("Nenhum look iniciado ainda.")
    for dia, look in cards:
        prog = calcular_progresso(look)
        emoji, cor, label = status_dia(look)
        st.markdown(f"""
        <div class='ohana-card'>
            <b>{emoji} {dia}</b> — {look.get('nome') or 'Sem nome'} &nbsp;
            <span style='color:{cor};'>({label})</span>
        </div>
        """, unsafe_allow_html=True)
        st.progress(prog, text=f"{int(prog * 100)}%")


def page_criar_look(data):
    st.markdown("<div class='ohana-title'>Criar Look</div>", unsafe_allow_html=True)
    st.markdown("<div class='ohana-subtitle'>Preencha as 9 etapas do fluxo de criação</div>", unsafe_allow_html=True)
    st.markdown("---")

    dia = st.selectbox(
        "Dia da semana",
        DIAS_SEMANA,
        index=DIAS_SEMANA.index(st.session_state.get("dia_selecionado", "Segunda"))
    )
    st.session_state["dia_selecionado"] = dia

    look = get_look(data, dia)
    nome_look = st.text_input("Nome do look", value=look.get("nome", ""), placeholder="Ex: Look Sunday Brunch")
    modelo = st.selectbox("Modelo", ["Magra", "Plus Size"], index=0 if look.get("modelo") == "Magra" else 1)

    prog = calcular_progresso(look)
    st.progress(prog, text=f"Progresso: {int(prog * 100)}%")
    st.markdown("---")

    st.markdown("### Etapas do Look")
    for idx, (nome, icone, tipo) in enumerate(ETAPAS):
        with st.expander(f"{icone} {idx + 1}. {nome}", expanded=not look["etapas"][nome]["concluida"]):
            concluida = st.checkbox("Concluída", value=look["etapas"][nome]["concluida"], key=f"chk_{dia}_{idx}")
            look["etapas"][nome]["concluida"] = concluida
            if tipo == "link":
                valor = st.text_input("Link", value=look["etapas"][nome].get("valor", ""), key=f"val_{dia}_{idx}")
            else:
                valor = st.text_area("Prompt / Descrição", value=look["etapas"][nome].get("valor", ""), key=f"val_{dia}_{idx}", height=100)
            look["etapas"][nome]["valor"] = valor

    look["nome"] = nome_look
    look["modelo"] = modelo
    look["atualizado_em"] = datetime.now().isoformat()
    look["finalizado"] = calcular_progresso(look) >= 1.0

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Salvar", type="primary", use_container_width=True):
            data["looks"][dia] = look
            save_and_reload(data)
    with col2:
        if st.button("🗑️ Limpar", use_container_width=True):
            data["looks"].pop(dia, None)
            save_and_reload(data)


def page_biblioteca(data):
    st.markdown("<div class='ohana-title'>Biblioteca</div>", unsafe_allow_html=True)
    st.markdown("<div class='ohana-subtitle'>Acervo de prompts, referências e modelos</div>", unsafe_allow_html=True)
    st.markdown("---")

    tabs = st.tabs(["📝 Prompts", "📌 Pinterest", "🛍️ Shopee", "👗 Modelos"])

    with tabs[0]:
        busca = st.text_input("Buscar", key="busca_prompts")
        for i, p in enumerate(data["prompts"]):
            if busca.lower() in (p["nome"] + p["texto"] + p["categoria"]).lower():
                st.markdown(f"""
                <div class='ohana-card'>
                    <b>{p['nome']}</b> <span style='color:{CORES['dourado']};'>({p['categoria']})</span><br>
                    <small>{p['texto']}</small>
                </div>
                """, unsafe_allow_html=True)
                col1, col2 = st.columns([4, 1])
                with col2:
                    if st.button("Copiar", key=f"copy_prompt_{i}"):
                        st.code(p["texto"])
        with st.expander("➕ Novo prompt"):
            nome = st.text_input("Nome", key="np_nome")
            cat = st.selectbox("Categoria", ["Modelo IA", "Curadoria", "Poses", "Carrossel", "Vídeo", "Reels", "Stories"], key="np_cat")
            texto = st.text_area("Texto", key="np_texto")
            if st.button("Adicionar"):
                if nome and texto:
                    data["prompts"].append({"nome": nome, "categoria": cat, "texto": texto})
                    save_and_reload(data)
                else:
                    st.warning("Preencha nome e texto.")

    with tabs[1]:
        for item in data["pinterest"]:
            st.markdown(f"""
            <div class='ohana-card'>
                📌 <b>{item['nome']}</b><br>
                <a href='{item['url']}' target='_blank' style='color:{CORES['rosa']};'>{item['url']}</a>
            </div>
            """, unsafe_allow_html=True)
        with st.expander("➕ Novo link"):
            nome = st.text_input("Nome", key="pin_nome")
            url = st.text_input("URL", key="pin_url")
            if st.button("Adicionar", key="add_pin"):
                if nome and url:
                    data["pinterest"].append({"nome": nome, "url": url})
                    save_and_reload(data)

    with tabs[2]:
        for item in data["shopee"]:
            st.markdown(f"""
            <div class='ohana-card'>
                🛍️ <b>{item['nome']}</b><br>
                <a href='{item['url']}' target='_blank' style='color:{CORES['rosa']};'>{item['url']}</a>
            </div>
            """, unsafe_allow_html=True)
        with st.expander("➕ Novo link"):
            nome = st.text_input("Nome", key="shop_nome")
            url = st.text_input("URL", key="shop_url")
            if st.button("Adicionar", key="add_shop"):
                if nome and url:
                    data["shopee"].append({"nome": nome, "url": url})
                    save_and_reload(data)

    with tabs[3]:
        for m in data["modelos"]:
            st.markdown(f"""
            <div class='ohana-card'>
                👗 <b>{m['nome']}</b> <span style='color:{CORES['dourado']};'>({m['tipo']})</span><br>
                {m['descricao']}<br>
                <small><i>{m['prompt']}</i></small>
            </div>
            """, unsafe_allow_html=True)


def page_historico(data):
    st.markdown("<div class='ohana-title'>Histórico</div>", unsafe_allow_html=True)
    st.markdown("<div class='ohana-subtitle'>Looks finalizados organizados por semana</div>", unsafe_allow_html=True)
    st.markdown("---")

    semanas = looks_por_semana(data)
    if not semanas:
        st.info("Nenhum look finalizado ainda. Complete todas as 9 etapas para vê-los aqui.")
        return

    for semana in sorted(semanas.keys(), reverse=True):
        with st.expander(f"🗓️ Semana de {semana}", expanded=True):
            for dia, look in semanas[semana]:
                concluidas = sum(1 for e in look["etapas"].values() if e["concluida"])
                st.markdown(f"""
                <div class='ohana-card'>
                    ✅ <b>{dia}</b> — {look.get('nome') or 'Sem nome'} &nbsp;|&nbsp;
                    Modelo: {look.get('modelo', 'Magra')} &nbsp;|&nbsp;
                    {concluidas}/9 etapas
                </div>
                """, unsafe_allow_html=True)


# ================== SIDEBAR ==================
def sidebar(data):
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align:center; padding:1.5rem 0 1rem 0;'>
            <div style='font-family:Cormorant Garamond, Georgia, serif; font-size:2rem; font-weight:700; color:white; letter-spacing:0.1em; text-transform:uppercase; line-height:1;'>OHANA</div>
            <div style='font-family:Inter, sans-serif; font-size:0.7rem; font-weight:400; color:{CORES['secundario']}; letter-spacing:0.25em; text-transform:uppercase; margin-top:4px;'>LIFESTYLE · STUDIO</div>
        </div>
        """, unsafe_allow_html=True)

        if "pagina" not in st.session_state:
            st.session_state["pagina"] = "Dashboard"

        for p in ["Dashboard", "Criar Look", "Biblioteca", "Histórico"]:
            if st.button(p, key=f"nav_{p}", use_container_width=True):
                st.session_state["pagina"] = p
                st.rerun()

        st.markdown("---")
        if st.button("🔄 Resetar dados", use_container_width=True):
            save_data(DEFAULT_DATA.copy())
            st.session_state["data"] = DEFAULT_DATA.copy()
            st.success("Resetado!")
            st.rerun()

        st.markdown(f"<div style='font-size:0.7rem; color:{CORES['secundario']}; margin-top:1rem; letter-spacing:0.1em; text-transform:uppercase;'>v1.0 · Ohana Studio</div>", unsafe_allow_html=True)


# ================== MAIN ==================
def main():
    inject_css()
    data = get_data()
    sidebar(data)

    pagina = st.session_state.get("pagina", "Dashboard")
    if pagina == "Dashboard":
        page_dashboard(data)
    elif pagina == "Criar Look":
        page_criar_look(data)
    elif pagina == "Biblioteca":
        page_biblioteca(data)
    elif pagina == "Histórico":
        page_historico(data)

    st.markdown("""
    <div class='footer'>
        OHANA LIFESTYLE · STUDIO &nbsp;·&nbsp; Curadoria de moda feminina
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
