import streamlit as st
import pandas as pd
import plotly.graph_objects as go

SECTIONS = {
    "sidebar": True,
    "kpi_row": True,
    "measure_tabs": True,
    "performance_flow": True,
    "revenue_trend": True,
    "recent_activity": True,
    "region_table": True,
    "state_revenue": True,
    "insights": True,
}

st.set_page_config(page_title="داشبورد مدیریت پروژه", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    html, body, [class*="css"]  { direction: rtl; text-align: right; font-family: 'Tahoma', sans-serif; }
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
    section[data-testid="stSidebar"] { background: #12172b; }
    section[data-testid="stSidebar"] * { color: #e3e6f0 !important; }
    section[data-testid="stSidebar"] .stButton button { background: transparent; border: none; text-align: right; width: 100%; }
    .card { background: #ffffff; border: 1px solid #eceef2; border-radius: 14px; padding: 18px 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
    .kpi-icon { width:34px; height:34px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:16px; margin-bottom:10px; }
    .kpi-label { font-size: 12px; color: #8a8f9c; margin-bottom: 4px; }
    .kpi-value { font-size: 22px; font-weight: 700; color: #1f2430; }
    .kpi-delta { font-size: 11px; color: #1c8a4b; margin-top: 4px; }
    .kpi-vs { font-size: 11px; color: #b3b7c2; }
    .panel-title { font-size:15px; font-weight:700; margin-bottom:2px; }
    .panel-sub { font-size:12px; color:#8a8f9c; margin-bottom: 14px; }
    .activity-row { display:flex; align-items:flex-start; gap:10px; padding:10px 0; border-bottom:1px solid #f2f3f6; }
    .activity-title { font-size:13px; font-weight:600; }
    .activity-sub { font-size:12px; color:#8a8f9c; }
    .activity-time { font-size:11px; color:#b3b7c2; margin-right:auto; }
    .insight-box { background:#eef4ff; border-radius:10px; padding:14px 16px; font-size:13px; color:#1f2430; line-height:1.8; }
    table.simple { width:100%; border-collapse:collapse; font-size:13px; }
    table.simple th { text-align:right; color:#8a8f9c; font-weight:normal; padding:8px 6px; border-bottom:1px solid #eceef2; }
    table.simple td { padding:9px 6px; border-bottom:1px solid #f2f3f6; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

COLOR_BLUE = "#2a5bd7"
COLOR_PURPLE = "#7b5cf0"
COLOR_TEAL = "#12b3a6"
COLOR_ORANGE = "#eb6834"

if SECTIONS["sidebar"]:
    with st.sidebar:
        st.markdown("### 🅐 مرکز عملکرد تحلیلی")
        st.caption("PMBI Works")
        st.write("")
        st.button("📊  نمای کلی", use_container_width=True)
        st.button("📄  گزارش‌ها", use_container_width=True)
        st.button("👥  مشتریان", use_container_width=True)
        st.button("📦  محصولات", use_container_width=True)
        st.button("🧾  سفارش‌ها", use_container_width=True)
        st.button("📣  بازاریابی", use_container_width=True)
        st.button("⚙️  تنظیمات", use_container_width=True)
        st.write("---")
        st.markdown("**فیلترها**")
        st.date_input("بازه‌ی تاریخ")
        st.selectbox("منطقه", ["همه‌ی مناطق", "شمال", "جنوب", "مرکز"])
        st.selectbox("کانال", ["همه‌ی کانال‌ها", "حضوری", "آنلاین"])
        st.write("---")
        st.markdown("👤 **علی خاکی**  \nمدیر سیستم")

h1, h2 = st.columns([3, 1])
with h1:
    st.markdown("## نمای کلی")
    st.caption("بینش عملکرد و شاخص‌های کلیدی به‌صورت لحظه‌ای")
with h2:
    st.markdown(
        '<div style="text-align:left;font-size:12px;color:#8a8f9c;">آخرین به‌روزرسانی: ۵ دقیقه پیش &nbsp; 🔔</div>',
        unsafe_allow_html=True,
    )
st.write("")

if SECTIONS["kpi_row"]:
    kpi_data = [
        ("💰", COLOR_BLUE, "درآمد کل", "۸۴۲,۴۵۰,۰۰۰ تومان", "▲ ۱۸.۶٪", "سال قبل: ۷۱۱,۰۲۴,۰۰۰"),
        ("📈", COLOR_PURPLE, "سود ناخالص", "۱۵۲,۸۶۰,۰۰۰ تومان", "▲ ۱۴.۲٪", "سال قبل: ۱۳۳,۶۶۸,۰۰۰"),
        ("🛒", COLOR_TEAL, "سفارش‌ها", "۱۲,۸۴۶", "▲ ۹.۷٪", "سال قبل: ۱۱,۷۰۴"),
        ("👥", COLOR_TEAL, "مشتریان", "۶,۲۹۴", "▲ ۱۱.۳٪", "سال قبل: ۵,۶۵۵"),
        ("🏷️", COLOR_ORANGE, "میانگین ارزش سفارش", "۶۵۵,۴۰۰ تومان", "▲ ۷.۳٪", "سال قبل: ۶۱۰,۷۰۰"),
    ]
    cols = st.columns(5)
    for col, (icon, color, label, value, delta, vs) in zip(cols, kpi_data):
        with col:
            st.markdown(f"""
            <div class="card">
                <div class="kpi-icon" style="background:{color}22;color:{color};">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-delta">{delta}</div>
                <div class="kpi-vs">{vs}</div>
            </div>
            """, unsafe_allow_html=True)
    st.write("")

if SECTIONS["measure_tabs"]:
    st.radio("انتخاب شاخص", ["درآمد", "سود", "سفارش‌ها", "تعداد"], horizontal=True, label_visibility="collapsed")
    st.write("")

if SECTIONS["performance_flow"] or SECTIONS["revenue_trend"] or SECTIONS["recent_activity"]:
    fc, tc, ac = st.columns([1.1, 1.4, 0.9])

    if SECTIONS["performance_flow"]:
        with fc:
            with st.container(border=True):
                st.markdown('<div class="panel-title">نمودار جریان عملکرد</div>', unsafe_allow_html=True)
                st.markdown('<div class="panel-sub">تفکیک درآمد کل بر اساس دسته‌بندی</div>', unsafe_allow_html=True)
                labels = ["درآمد کل", "مصرف‌کننده", "شرکتی", "خانگی", "لوازم اداری", "مبلمان", "فناوری"]
                sankey_fig = go.Figure(go.Sankey(
                    node=dict(
                        pad=15, thickness=16,
                        label=labels,
                        color=[COLOR_BLUE, COLOR_TEAL, COLOR_PURPLE, COLOR_ORANGE, "#9aa4c9", "#9aa4c9", "#9aa4c9"],
                    ),
                    link=dict(
                        source=[0, 0, 0, 1, 2, 3],
                        target=[1, 2, 3, 4, 5, 6],
                        value=[421, 256, 163, 240, 318, 283],
                        color="rgba(42,91,215,0.15)",
                    ),
                ))
                sankey_fig.update_layout(height=320, margin=dict(l=0, r=0, t=0, b=0), font=dict(family="Tahoma", size=11))
                st.plotly_chart(sankey_fig, use_container_width=True, config={"displayModeBar": False})

    if SECTIONS["revenue_trend"]:
        with tc:
            with st.container(border=True):
                st.markdown('<div class="panel-title">روند درآمد</div>', unsafe_allow_html=True)
                st.markdown('<div class="panel-sub">درآمد ماهانه بر حسب تومان</div>', unsafe_allow_html=True)
                months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر"]
                revenue = [55, 40, 62, 58, 70, 65, 78, 105, 90]
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=months, y=revenue, mode="lines+markers", fill="tozeroy",
                    line=dict(color=COLOR_BLUE, width=3), fillcolor="rgba(42,91,215,0.08)",
                ))
                fig_trend.update_layout(
                    height=320, margin=dict(l=10, r=10, t=10, b=10),
                    plot_bgcolor="white", paper_bgcolor="white",
                    yaxis=dict(ticksuffix=" م", gridcolor="#f0f1f4"),
                    xaxis=dict(showgrid=False),
                    font=dict(family="Tahoma"),
                )
                st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})

    if SECTIONS["recent_activity"]:
        with ac:
            with st.container(border=True):
                st.markdown('<div class="panel-title">فعالیت‌های اخیر</div>', unsafe_allow_html=True)
                st.write("")
                activities = [
                    ("📈", "افزایش درآمد", "۱۸.۶٪ نسبت به ماه قبل", "۵ دقیقه پیش"),
                    ("🏷️", "پرفروش‌ترین دسته", "فناوری اطلاعات", "۱ ساعت پیش"),
                    ("👤", "مشتری جدید", "شرکت آرمان به لیست اضافه شد", "۳ ساعت پیش"),
                    ("🎯", "تحقق هدف", "هدف فصلی درآمد محقق شد", "۱ روز پیش"),
                    ("📦", "هشدار موجودی", "۴ قلم کالا رو به اتمام", "۲ روز پیش"),
                ]
                for icon, title, sub, time in activities:
                    st.markdown(f"""
                    <div class="activity-row">
                        <span>{icon}</span>
                        <div>
                            <div class="activity-title">{title}</div>
                            <div class="activity-sub">{sub}</div>
                        </div>
                        <div class="activity-time">{time}</div>
                    </div>
                    """, unsafe_allow_html=True)
    st.write("")

if SECTIONS["region_table"] or SECTIONS["state_revenue"] or SECTIONS["insights"]:
    rt, sv, ins = st.columns([1.3, 1, 0.9])

    if SECTIONS["region_table"]:
        with rt:
            with st.container(border=True):
                st.markdown('<div class="panel-title">درآمد بر اساس منطقه و دسته</div>', unsafe_allow_html=True)
                st.write("")
                region_df = pd.DataFrame({
                    "منطقه": ["غرب", "جنوب", "شرق", "مرکز"],
                    "لوازم اداری": ["۹۷,۱۲۵", "۶۳,۸۸۴", "۶۸,۷۷۵", "۴۱,۰۵۶"],
                    "مبلمان": ["۱۰۵,۴۴۱", "۷۱,۲۲۰", "۸۲,۴۵۱", "۵۴,۸۷۳"],
                    "فناوری": ["۱۱۵,۸۹۲", "۹۳,۳۷۴", "۱۱۱,۷۹۸", "۶۳,۵۹۵"],
                    "جمع": ["۳۱۸,۴۵۸", "۲۲۸,۴۷۸", "۲۶۳,۰۲۴", "۱۵۹,۵۲۴"],
                })
                st.markdown(region_df.to_html(index=False, classes="simple", border=0), unsafe_allow_html=True)

    if SECTIONS["state_revenue"]:
        with sv:
            with st.container(border=True):
                st.markdown('<div class="panel-title">درآمد بر اساس استان</div>', unsafe_allow_html=True)
                st.write("")
                states = ["تهران", "اصفهان", "فارس", "خراسان", "آذربایجان"]
                values = [128.9, 82.4, 55.7, 41.3, 34.8]
                fig_state = go.Figure(go.Bar(
                    x=values, y=states, orientation="h", marker_color=COLOR_BLUE,
                    text=[f"{v} م" for v in values], textposition="outside",
                ))
                fig_state.update_layout(
                    height=280, margin=dict(l=10, r=10, t=10, b=10),
                    plot_bgcolor="white", paper_bgcolor="white",
                    xaxis=dict(showgrid=False, visible=False),
                    yaxis=dict(autorange="reversed"),
                    font=dict(family="Tahoma"),
                )
                st.plotly_chart(fig_state, use_container_width=True, config={"displayModeBar": False})

    if SECTIONS["insights"]:
        with ins:
            with st.container(border=True):
                st.markdown('<div class="panel-title">بینش‌ها</div>', unsafe_allow_html=True)
                st.write("")
                st.markdown(
                    '<div class="insight-box">💡 فروش دسته‌ی فناوری نسبت به ماه قبل ۲۴٪ رشد داشته. '
                    'پیشنهاد می‌شه سطح موجودی این دسته افزایش پیدا کنه.</div>',
                    unsafe_allow_html=True,
                )
