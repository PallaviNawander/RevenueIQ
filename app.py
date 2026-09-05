import streamlit as st

from tools import scan_for_leaks
from agent import investigate
from data import MERCHANTS


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RevenueIQ",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# HELPER
# =========================================================

def render_html(content):
    """
    Render custom HTML using Streamlit's native HTML renderer.
    """
    st.html(content)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       REMOVE STREAMLIT TOP HEADER / BLACK STRIP
       ===================================================== */

    header[data-testid="stHeader"] {
        display: none !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    [data-testid="stStatusWidget"] {
        display: none !important;
    }

    /* Hide sidebar completely */
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Remove Streamlit default top spacing */
    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 4rem !important;
        max-width: 1120px !important;
    }

    /* Main page */
    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(137, 53, 190, 0.22),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 5%,
                rgba(255, 130, 195, 0.13),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #190b27 0%,
                #100719 45%,
                #08050d 100%
            );

        color: #fff;
    }

    /* Remove default horizontal line */
    hr {
        display: none !important;
    }

    /* Streamlit text */
    .stMarkdown,
    .stText {
        color: #f8f2fb;
    }

    /* =====================================================
       SELECTBOX
       ===================================================== */

    div[data-baseweb="select"] {
        background: rgba(255,255,255,0.055) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] > div {
        background: transparent !important;
        color: white !important;
        border: none !important;
    }

    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }

    div[data-baseweb="select"] svg {
        fill: #ffffff !important;
    }

    label[data-testid="stWidgetLabel"] {
        color: #b7a8bf !important;
        font-size: 12px !important;
    }

    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        width: 100%;
        min-height: 46px;

        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.15);

        background:
            linear-gradient(
                135deg,
                rgba(192, 114, 255, 0.22),
                rgba(255, 181, 220, 0.12)
            );

        color: #ffffff;

        font-weight: 700;
        font-size: 14px;

        transition:
            transform 0.18s ease,
            border-color 0.18s ease,
            background 0.18s ease;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.18);
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        border-color: rgba(236, 174, 255, 0.55);

        background:
            linear-gradient(
                135deg,
                rgba(192, 114, 255, 0.35),
                rgba(255, 181, 220, 0.20)
            );
    }

    .stButton > button:focus {
        box-shadow:
            0 0 0 2px rgba(221, 151, 255, 0.2);
    }

    /* =====================================================
       HEADER
       ===================================================== */

    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 12px 0 22px 0;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .brand-logo {
        width: 48px;
        height: 48px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 14px;

        background:
            linear-gradient(
                135deg,
                rgba(217, 164, 255, 0.20),
                rgba(255, 209, 230, 0.08)
            );

        border: 1px solid rgba(255,255,255,0.16);

        font-size: 25px;

        box-shadow:
            0 10px 35px rgba(130, 56, 170, 0.22);
    }

    .brand-name {
        font-size: 23px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #ffffff;
    }

    .brand-subtitle {
        margin-top: 2px;

        color: #9f8ba8;

        font-size: 12px;
        font-weight: 500;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 7px;

        padding: 9px 14px;

        border-radius: 999px;

        background: rgba(130, 255, 188, 0.07);

        border: 1px solid rgba(130, 255, 188, 0.20);

        color: #91ffc0;

        font-size: 12px;
        font-weight: 700;
    }

    .status-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: #7dffb5;

        box-shadow:
            0 0 10px rgba(125,255,181,0.75);
    }

    /* =====================================================
       MERCHANT SELECTOR
       ===================================================== */

    .monitor-card {
        margin-top: 8px;
        margin-bottom: 48px;

        padding: 19px 22px;

        border-radius: 18px;

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.065),
                rgba(255,255,255,0.035)
            );

        border: 1px solid rgba(255,255,255,0.12);

        box-shadow:
            0 18px 50px rgba(0,0,0,0.20);
    }

    .monitor-label {
        color: #a998b0;

        font-size: 10px;
        font-weight: 800;

        letter-spacing: 1.5px;

        text-transform: uppercase;

        margin-bottom: 8px;
    }

    .monitor-name {
        color: #ffffff;

        font-size: 20px;
        font-weight: 800;
    }

    /* =====================================================
       HERO
       ===================================================== */

    .hero {
        margin-top: 8px;
        margin-bottom: 42px;
    }

    .hero-kicker {
        color: #d39aff;

        font-size: 12px;
        font-weight: 800;

        letter-spacing: 1.4px;

        text-transform: uppercase;

        margin-bottom: 13px;
    }

    .hero-title {
        max-width: 780px;

        font-size: 52px;
        line-height: 1.02;

        letter-spacing: -2.4px;

        font-weight: 800;

        color: #fff;

        margin-bottom: 18px;
    }

    .hero-title .gradient {
        background:
            linear-gradient(
                90deg,
                #e5b7ff,
                #f6b7df,
                #ffdcae
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        max-width: 760px;

        color: #aa98b2;

        font-size: 15px;
        line-height: 1.7;
    }

    .hero-description strong {
        color: #d7c7dc;
    }

    /* =====================================================
       METRIC CARDS
       ===================================================== */

    .metric-card {
        min-height: 138px;

        padding: 22px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.065),
                rgba(255,255,255,0.035)
            );

        border: 1px solid rgba(255,255,255,0.11);

        box-shadow:
            0 16px 40px rgba(0,0,0,0.16);
    }

    .metric-label {
        color: #a899af;

        font-size: 10px;
        font-weight: 800;

        text-transform: uppercase;

        letter-spacing: 0.7px;

        margin-bottom: 12px;
    }

    .metric-value {
        color: #fff;

        font-size: 31px;
        font-weight: 800;

        letter-spacing: -1px;

        margin-bottom: 8px;
    }

    .metric-description {
        color: #8f7f98;

        font-size: 11px;
    }

    /* =====================================================
       SECTION TITLES
       ===================================================== */

    .section {
        margin-top: 50px;
        margin-bottom: 20px;
    }

    .section-title {
        color: #ffffff;

        font-size: 23px;
        font-weight: 800;

        letter-spacing: -0.5px;

        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #918099;

        font-size: 12px;
    }

    /* =====================================================
       HEALTH CARDS
       ===================================================== */

    .health-card {
        min-height: 175px;

        padding: 23px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.055),
                rgba(255,255,255,0.025)
            );

        border: 1px solid rgba(255,255,255,0.10);
    }

    .health-title {
        color: #ffffff;

        font-size: 14px;
        font-weight: 750;

        margin-bottom: 20px;
    }

    .health-number {
        color: #fff;

        font-size: 29px;
        font-weight: 800;

        margin-bottom: 7px;
    }

    .health-text {
        color: #95849e;

        font-size: 11px;
    }

    .progress {
        height: 7px;

        margin-top: 17px;

        border-radius: 99px;

        background: rgba(255,255,255,0.08);

        overflow: hidden;
    }

    .progress-fill {
        height: 100%;

        border-radius: 99px;

        background:
            linear-gradient(
                90deg,
                #9d5de9,
                #efb5dc
            );
    }

    /* =====================================================
       LEAK CARDS
       ===================================================== */

    .leak-card {
        padding: 22px;

        margin-bottom: 15px;

        border-radius: 18px;

        background:
            linear-gradient(
                145deg,
                rgba(255,255,255,0.065),
                rgba(255,255,255,0.025)
            );

        border: 1px solid rgba(255,255,255,0.11);

        box-shadow:
            0 15px 40px rgba(0,0,0,0.15);
    }

    .leak-top {
        display: flex;
        justify-content: space-between;
        align-items: center;

        margin-bottom: 14px;
    }

    .leak-type {
        color: #ffffff;

        font-size: 15px;
        font-weight: 800;
    }

    .severity {
        padding: 6px 10px;

        border-radius: 999px;

        font-size: 9px;
        font-weight: 900;

        letter-spacing: 0.8px;
    }

    .severity-high {
        color: #ff9fae;

        background: rgba(255,94,119,0.09);

        border: 1px solid rgba(255,94,119,0.18);
    }

    .severity-medium {
        color: #ffd38c;

        background: rgba(255,190,92,0.09);

        border: 1px solid rgba(255,190,92,0.18);
    }

    .severity-low {
        color: #9effc5;

        background: rgba(100,255,164,0.08);

        border: 1px solid rgba(100,255,164,0.18);
    }

    .leak-info {
        display: grid;

        grid-template-columns:
            repeat(3, 1fr);

        gap: 15px;

        margin-bottom: 17px;
    }

    .info-label {
        color: #8e7d97;

        font-size: 9px;

        text-transform: uppercase;

        letter-spacing: 0.7px;

        margin-bottom: 5px;
    }

    .info-value {
        color: #e9deed;

        font-size: 13px;
        font-weight: 700;
    }

    .evidence {
        padding: 12px 14px;

        border-radius: 10px;

        background: rgba(0,0,0,0.17);

        color: #aa9aae;

        font-size: 11px;

        line-height: 1.55;
    }

    /* =====================================================
       INVESTIGATION PANEL
       ===================================================== */

    .investigation-panel {
        margin-top: 20px;

        padding: 25px;

        border-radius: 20px;

        background:
            linear-gradient(
                145deg,
                rgba(166,91,224,0.11),
                rgba(255,184,219,0.045)
            );

        border: 1px solid rgba(211,154,255,0.20);

        box-shadow:
            0 20px 60px rgba(0,0,0,0.20);
    }

    .ai-badge {
        display: inline-block;

        padding: 6px 10px;

        border-radius: 999px;

        color: #e4b9ff;

        background: rgba(196,111,255,0.09);

        border: 1px solid rgba(196,111,255,0.18);

        font-size: 9px;
        font-weight: 900;

        letter-spacing: 1px;

        margin-bottom: 13px;
    }

    .investigation-title {
        color: #ffffff;

        font-size: 21px;
        font-weight: 800;

        margin-bottom: 8px;
    }

    .investigation-summary {
        color: #b5a4bd;

        font-size: 13px;

        line-height: 1.6;

        margin-bottom: 22px;
    }

    .finding-box {
        padding: 17px;

        border-radius: 13px;

        background: rgba(0,0,0,0.16);

        border: 1px solid rgba(255,255,255,0.07);
    }

    .finding-label {
        color: #9f8da7;

        font-size: 9px;
        font-weight: 800;

        letter-spacing: 1px;

        text-transform: uppercase;

        margin-bottom: 8px;
    }

    .finding-text {
        color: #ddd1e1;

        font-size: 12px;

        line-height: 1.65;
    }

    .evidence-list {
        margin: 0;
        padding-left: 19px;

        color: #c5b5ca;

        font-size: 12px;

        line-height: 1.8;
    }

    .action-box {
        margin-top: 18px;

        padding: 17px;

        border-radius: 13px;

        background: rgba(143,255,186,0.045);

        border: 1px solid rgba(143,255,186,0.12);
    }

    .action-label {
        color: #92ffbf;

        font-size: 9px;

        font-weight: 900;

        letter-spacing: 1px;

        text-transform: uppercase;

        margin-bottom: 7px;
    }

    .action-value {
        color: #ffffff;

        font-size: 17px;

        font-weight: 800;
    }

    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {
        margin-top: 60px;
        padding-top: 22px;

        border-top: 1px solid rgba(255,255,255,0.07);

        color: #65576d;

        font-size: 10px;

        text-align: center;
    }

    /* =====================================================
       RESPONSIVE
       ===================================================== */

    @media (max-width: 900px) {

        .hero-title {
            font-size: 42px;
        }

        .metric-value {
            font-size: 27px;
        }

    }

    @media (max-width: 650px) {

        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .top-header {
            align-items: flex-start;
        }

        .status-pill {
            display: none;
        }

        .hero-title {
            font-size: 36px;
            letter-spacing: -1.5px;
        }

        .leak-info {
            grid-template-columns: 1fr;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "investigation" not in st.session_state:
    st.session_state.investigation = None

if "investigating_leak" not in st.session_state:
    st.session_state.investigating_leak = None

if "last_merchant_id" not in st.session_state:
    st.session_state.last_merchant_id = None


# =========================================================
# HEADER
# =========================================================

render_html(
    """
    <div class="top-header">

        <div class="brand">

            <div class="brand-logo">
                ◇
            </div>

            <div>
                <div class="brand-name">
                    RevenueIQ
                </div>

                <div class="brand-subtitle">
                    AI revenue recovery intelligence
                </div>
            </div>

        </div>

        <div class="status-pill">
            <span class="status-dot"></span>
            Detection engine active
        </div>

    </div>
    """
)


# =========================================================
# MERCHANT SELECTOR
# =========================================================

merchant_names = [
    merchant["name"]
    for merchant in MERCHANTS
]

selected_name = st.selectbox(
    "Merchant",
    merchant_names,
    label_visibility="collapsed",
)

selected_merchant = next(
    merchant
    for merchant in MERCHANTS
    if merchant["name"] == selected_name
)

merchant_id = selected_merchant["id"]


# =========================================================
# RESET AI INVESTIGATION WHEN MERCHANT CHANGES
# =========================================================

if st.session_state.last_merchant_id != merchant_id:

    st.session_state.investigation = None
    st.session_state.investigating_leak = None
    st.session_state.last_merchant_id = merchant_id


# =========================================================
# MONITORING CARD
# =========================================================

render_html(
    f"""
    <div class="monitor-card">

        <div class="monitor-label">
            Currently monitoring
        </div>

        <div class="monitor-name">
            {selected_merchant["name"]}
        </div>

    </div>
    """
)


# =========================================================
# HERO
# =========================================================

render_html(
    f"""
    <div class="hero">

        <div class="hero-kicker">
            {selected_merchant["industry"].upper()}
            ·
            {merchant_id}
        </div>

        <div class="hero-title">
            Find the money<br>
            you're <span class="gradient">losing.</span>
        </div>

        <div class="hero-description">
            RevenueIQ continuously analyzes transaction activity
            for <strong>{selected_merchant["name"]}</strong>
            to identify suspicious payments, failed renewals,
            duplicate refunds, and recoverable revenue.
        </div>

    </div>
    """
)


# =========================================================
# RUN DETECTION
# =========================================================

leaks = scan_for_leaks(merchant_id)


# =========================================================
# METRICS
# =========================================================

revenue_at_risk = sum(
    leak["amount"]
    for leak in leaks
)

potential_recovery = sum(
    leak["amount"]
    for leak in leaks
    if leak["severity"] in ["HIGH", "MEDIUM"]
)

high_priority = sum(
    1
    for leak in leaks
    if leak["severity"] == "HIGH"
)


metric1, metric2, metric3, metric4 = st.columns(4)


with metric1:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Revenue at risk
            </div>

            <div class="metric-value">
                ₹{revenue_at_risk:,.0f}
            </div>

            <div class="metric-description">
                Detected across transactions
            </div>

        </div>
        """
    )


with metric2:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Leaks detected
            </div>

            <div class="metric-value">
                {len(leaks)}
            </div>

            <div class="metric-description">
                Revenue anomalies found
            </div>

        </div>
        """
    )


with metric3:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                Potential recovery
            </div>

            <div class="metric-value">
                ₹{potential_recovery:,.0f}
            </div>

            <div class="metric-description">
                High + medium priority
            </div>

        </div>
        """
    )


with metric4:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                High priority
            </div>

            <div class="metric-value">
                {high_priority}
            </div>

            <div class="metric-description">
                Requires attention
            </div>

        </div>
        """
    )


# =========================================================
# MERCHANT HEALTH
# =========================================================

render_html(
    """
    <div class="section">

        <div class="section-title">
            Merchant health
        </div>

        <div class="section-subtitle">
            Current revenue integrity signals
        </div>

    </div>
    """
)


health1, health2, health3 = st.columns(3)


# =========================================================
# HEALTH 1
# =========================================================

with health1:

    if revenue_at_risk == 0:

        risk_percentage = 0

    else:

        risk_percentage = min(
            int(
                (
                    revenue_at_risk
                    / selected_merchant["monthly_revenue"]
                )
                * 100
            ),
            100,
        )

    render_html(
        f"""
        <div class="health-card">

            <div class="health-title">
                Revenue exposure
            </div>

            <div class="health-number">
                {risk_percentage}%
            </div>

            <div class="health-text">
                Estimated monthly revenue exposed
            </div>

            <div class="progress">

                <div
                    class="progress-fill"
                    style="width:{risk_percentage}%"
                ></div>

            </div>

        </div>
        """
    )


# =========================================================
# HEALTH 2
# =========================================================

with health2:

    high_count = sum(
        1
        for leak in leaks
        if leak["severity"] == "HIGH"
    )

    medium_count = sum(
        1
        for leak in leaks
        if leak["severity"] == "MEDIUM"
    )

    render_html(
        f"""
        <div class="health-card">

            <div class="health-title">
                Risk distribution
            </div>

            <div class="health-number">
                {high_count}
            </div>

            <div class="health-text">
                High priority leaks · {medium_count} medium
            </div>

            <div class="progress">

                <div
                    class="progress-fill"
                    style="width:{min(high_count * 30, 100)}%"
                ></div>

            </div>

        </div>
        """
    )


# =========================================================
# HEALTH 3
# =========================================================

with health3:

    avg_confidence = (
        sum(
            leak["confidence"]
            for leak in leaks
        )
        / len(leaks)
        if leaks
        else 0
    )

    render_html(
        f"""
        <div class="health-card">

            <div class="health-title">
                Detection confidence
            </div>

            <div class="health-number">
                {avg_confidence:.0f}%
            </div>

            <div class="health-text">
                Average confidence across detected leaks
            </div>

            <div class="progress">

                <div
                    class="progress-fill"
                    style="width:{avg_confidence}%"
                ></div>

            </div>

        </div>
        """
    )


# =========================================================
# PRIORITY LEAKS
# =========================================================

render_html(
    """
    <div class="section">

        <div class="section-title">
            Priority leaks
        </div>

        <div class="section-subtitle">
            Revenue anomalies detected by the rules engine
        </div>

    </div>
    """
)


# =========================================================
# NO LEAKS
# =========================================================

if not leaks:

    render_html(
        """
        <div class="leak-card">

            <div class="leak-type">
                No revenue leaks detected
            </div>

            <div class="evidence">
                The detection engine found no suspicious
                transaction patterns for this merchant.
            </div>

        </div>
        """
    )


# =========================================================
# LEAK LIST
# =========================================================

for leak in leaks:

    severity = leak["severity"].lower()

    severity_class = f"severity-{severity}"

    render_html(
        f"""
        <div class="leak-card">

            <div class="leak-top">

                <div class="leak-type">
                    {leak["type"]}
                </div>

                <div class="severity {severity_class}">
                    {leak["severity"]}
                </div>

            </div>

            <div class="leak-info">

                <div>

                    <div class="info-label">
                        Customer
                    </div>

                    <div class="info-value">
                        {leak["customer"]}
                    </div>

                </div>

                <div>

                    <div class="info-label">
                        Amount
                    </div>

                    <div class="info-value">
                        ₹{leak["amount"]:,.0f}
                    </div>

                </div>

                <div>

                    <div class="info-label">
                        Confidence
                    </div>

                    <div class="info-value">
                        {leak["confidence"]}%
                    </div>

                </div>

            </div>

            <div class="evidence">
                {leak["evidence"]}
            </div>

        </div>
        """
    )


    # =====================================================
    # INVESTIGATE BUTTON
    # =====================================================

    button_key = f"investigate_{leak['id']}"

    if st.button(
        f"🔍 Investigate {leak['id']}",
        key=button_key,
        use_container_width=True,
    ):

        st.session_state.investigating_leak = leak["id"]

        with st.spinner(
            "RevenueIQ AI is investigating the leak..."
        ):

            result = investigate(
                leak["id"],
                merchant_id,
            )

        st.session_state.investigation = result

        st.rerun()


# =========================================================
# AI INVESTIGATION RESULT
# =========================================================

if st.session_state.investigation:

    result = st.session_state.investigation

    render_html(
        """
        <div class="section">

            <div class="section-title">
                AI investigation
            </div>

            <div class="section-subtitle">
                Evidence-based revenue recovery analysis
            </div>

        </div>
        """
    )


    # =====================================================
    # ERROR
    # =====================================================

    if "error" in result:

        render_html(
            f"""
            <div class="investigation-panel">

                <div class="ai-badge">
                    REVENUEIQ AI
                </div>

                <div class="investigation-title">
                    Investigation failed
                </div>

                <div class="finding-box">

                    <div class="finding-label">
                        Error
                    </div>

                    <div class="finding-text">
                        {result["error"]}
                    </div>

                </div>

            </div>
            """
        )


    # =====================================================
    # NORMAL RESULT
    # =====================================================

    else:

        summary = result.get(
            "summary",
            "Investigation completed."
        )

        finding = result.get(
            "finding",
            "No detailed finding available."
        )

        confidence = result.get(
            "confidence",
            0
        )

        risk = result.get(
            "risk",
            "UNKNOWN"
        )

        action = result.get(
            "recommended_action",
            "ESCALATE"
        )

        recovery = result.get(
            "recovery_amount",
            0
        )

        reason = result.get(
            "reason",
            ""
        )

        evidence_items = result.get(
            "evidence",
            []
        )

        evidence_html = ""

        for item in evidence_items:

            evidence_html += f"""
            <li>{item}</li>
            """


        render_html(
            f"""
            <div class="investigation-panel">

                <div class="ai-badge">
                    REVENUEIQ AI INVESTIGATOR
                </div>

                <div class="investigation-title">
                    {summary}
                </div>

                <div class="investigation-summary">

                    Confidence:
                    <strong>{confidence}%</strong>

                    &nbsp; · &nbsp;

                    Risk:
                    <strong>{risk}</strong>

                </div>

                <div class="finding-box">

                    <div class="finding-label">
                        What happened
                    </div>

                    <div class="finding-text">
                        {finding}
                    </div>

                </div>

                <br>

                <div class="finding-box">

                    <div class="finding-label">
                        Evidence
                    </div>

                    <ul class="evidence-list">
                        {evidence_html}
                    </ul>

                </div>

                <div class="action-box">

                    <div class="action-label">
                        Recommended action
                    </div>

                    <div class="action-value">
                        {action}
                    </div>

                    <div
                        class="finding-text"
                        style="margin-top:8px;"
                    >
                        {reason}
                    </div>

                    <div
                        style="
                            margin-top:14px;
                            color:#92ffbf;
                            font-size:12px;
                            font-weight:700;
                        "
                    >
                        Potential recovery:
                        ₹{recovery:,.0f}
                    </div>

                </div>

            </div>
            """
        )


# =========================================================
# FOOTER
# =========================================================

render_html(
    """
    <div class="footer">
        RevenueIQ · AI-powered revenue recovery intelligence
    </div>
    """
)