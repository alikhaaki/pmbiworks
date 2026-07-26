import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =====================================================================
# تنظیمات ماژولار — هر بخش رو با True (روشن) یا False (خاموش) کنترل کن
# =====================================================================
SECTIONS = {
    "topbar": True,
    "kpi": True,
    "budget_bar": True,
    "delay_pie": True,
    "s_curve": True,
    "checklist": True,
    "risk_matrix": True,
    "team_table": True,
}

st.set_page_config(page_title="داشبورد مدیریت پروژه", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    html, body, [class*="css"]  { direction: rtl; text-align: right; font-family: 'Tahoma', sans-serif; }
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .card {
        background: #ffffff; border: 1px solid #eceef2; border-radius: 14px;
        padding: 20px 22px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .kpi-label { font-size: 13px; color: #8a8f9c; margin-bottom: 8px; }
    .kpi-value { font-size: 28px; font-weight: 700; color: #1f2430; }
    .kpi-delta-good { display:inline-block; margin-top:8px; font-size:12px; background:#e6f6ec; color:#1c8a4b; padding:3px 10px; border-radius:6px; }
    .kpi-delta-warn { display:inline-block; margin-top:8px; font-size:12px; background:#fdf1e3; color:#b56a1a; padding:3px 10px; border-radius:6px; }
    .kpi-delta-bad { display:inline-block; margin-top:8px; font-size:12px; background:#fdecec; color:#c73434; padding:3px 10px; border-radius:6px; }
    .panel-title { font-size:16px; font-weight:700; margin-bottom:2px; }
    .panel-sub { font-size:12px; color:#8a8f9c; margin-bottom: 14px; }
    .check-card { display:flex; align-items:center; justify-content:space-between; padding:14px 16px; }
    .check-ok { color:#1c8a4b; }
    .check-bad { color:#c73434; }
    .risk-cell { height:40px; border-radius:6px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

COLOR_PLAN = "#2a5bd7"
COLOR_ACTUAL = "#eb6834"

# ---------- sample / placeholder data ----------
months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور"]
planned_cum = [15, 32, 50, 68, 85, 100]
actual_cum = [12, 28, 47, 72, 90, 103]

floors = ["طبقه ۱", "طبقه ۲", "طبقه ۳", "طبقه ۴"]
floor_planned = [75, 90, 60, 30]
floor_actual = [65, 95, 55, 34]

delay_labels = ["طبقه ۲", "طبقه ۱", "طبقه ۳", "طبقه ۴"]
delay_values = [33, 28, 22, 17]

checklist_items = [
    ("تکمیل کارهای اولیه", True),
    ("تامین تجهیزات", False),
    ("تامین نیروی انسانی", True),
    ("تست کیفی", True),
    ("تایید نقشه‌ها", False),
    ("تست نهایی", True),
]

risk_rows = ["زیاد", "متوسط", "کم"]
risk_cols = ["کم", "متوسط", "زیاد"]
risk_grid = [
    ["#f2b53a", "#e35d4f", "#e35d4f"],
    ["#7bc96f", "#f2b53a", "#e35d4f"],
    ["#7bc96f", "#7bc96f", "#f2b53a"],
]

tasks = pd.DataFrame({
    "فعالیت": ["نصب سقف کاذب", "لوله‌کشی تاسیسات", "نازک‌کاری دیوارها", "اجرای کف‌سازی"],
    "طبقه": ["طبقه ۲", "طبقه ۱", "طبقه ۳", "طبقه ۴"],
    "مسئول": ["واحد اجرا", "پیمانکار مکانیک", "واحد اجرا", "پیمانکار برق"],
    "پیشرفت": [45, 70, 90, 20],
    "وضعیت": ["تاخیر دارد", "در حال بررسی", "طبق برنامه", "تاخیر دارد"],
})


def panel_header(title, sub):
    st.markdown(f'<div class="panel-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-sub">{sub}</div>', unsafe_allow_html=True)


# ---------- top bar ----------
if SECTIONS["topbar"]:
    t1, t2, t3 = st.columns([3, 2, 1.2])
    with t1:
        st.markdown("### داشبورد مدیریت پروژه A")
    with t2:
        st.selectbox("پروژه", ["پروژه A", "پروژه B", "پروژه C"], label_visibility="collapsed")
    with t3:
        st.button("دانلود گزارش PDF", use_container_width=True)
    st.write("")

# ---------- KPI row ----------
if SECTIONS["kpi"]:
    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        (k1, "پیشرفت کلی پروژه", "۶۸٪", "▲ ۳٪ جلوتر از برنامه", "good"),
        (k2, "تاخیرات باز", "۱۸", "۵ مورد بحرانی", "warn"),
        (k3, "وضعیت بودجه", "۹۲٪", "در محدوده مصوب", "good"),
        (k4, "روزهای باقی‌مانده", "۴۲", "۶ روز کمتر از برنامه", "bad"),
    ]
    for col, label, value, delta, kind in kpis:
        with col:
            st.markdown(f"""
            <div class="card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-delta-{kind}">{delta}</div>
            </div>
            """, unsafe_allow_html=True)
    st.write("")

# ---------- budget bar + delay pie (side by side) ----------
if SECTIONS["budget_bar"] or SECTIONS["delay_pie"]:
    bc1, bc2 = st.columns(2)
    if SECTIONS["budget_bar"]:
        with bc1:
            with st.container(border=True):
                panel_header("پیشرفت برنامه‌ای و واقعی", "درصد پیشرفت به تفکیک طبقه")
                fig_bar = go.Figure()
                fig_bar.add_trace(go.Bar(x=floors, y=floor_planned, name="برنامه‌ای", marker_color=COLOR_PLAN))
                fig_bar.add_trace(go.Bar(x=floors, y=floor_actual, name="واقعی", marker_color=COLOR_ACTUAL))
                fig_bar.update_layout(
                    barmode="group", height=300, margin=dict(l=10, r=10, t=10, b=10),
                    plot_bgcolor="white", paper_bgcolor="white",
                    yaxis=dict(ticksuffix="٪", gridcolor="#f0f1f4"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    font=dict(family="Tahoma"),
                )
                st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    if SECTIONS["delay_pie"]:
        with bc2:
            with st.container(border=True):
                panel_header("تاخیرها بر اساس طبقه", "نسبت موارد باز")
                fig_donut = go.Figure(data=[go.Pie(
                    labels=delay_labels, values=delay_values, hole=0.55,
                    marker=dict(colors=[COLOR_PLAN, COLOR_ACTUAL, "#1c9e6e", "#d9a92a"]),
                    textinfo="label+percent",
                )])
                fig_donut.update_layout(
                    height=300, margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor="white", showlegend=False,
                    font=dict(family="Tahoma"),
                )
                st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
    st.write("")

# ---------- checklist + s-curve ----------
if SECTIONS["checklist"] or SECTIONS["s_curve"]:
    lc, rc = st.columns([1, 1.6])
    if SECTIONS["checklist"]:
        with lc:
            with st.container(border=True):
                panel_header("وضعیت مراحل کلیدی", "خلاصه‌ی مراحل اصلی پروژه")
                for i in range(0, len(checklist_items), 2):
                    cc1, cc2 = st.columns(2)
                    pair = checklist_items[i:i + 2]
                    for col, (label, ok) in zip([cc1, cc2], pair):
                        icon = "✅" if ok else "🔴"
                        cls = "check-ok" if ok else "check-bad"
                        with col:
                            st.markdown(f"""
                            <div class="card check-card">
                                <span>{label}</span>
                                <span class="{cls}">{icon}</span>
                            </div>
                            """, unsafe_allow_html=True)
    if SECTIONS["s_curve"]:
        with rc:
            with st.container(border=True):
                panel_header("منحنی S پیشرفت تجمعی", "برنامه‌ای در برابر واقعی")
                fig_s = go.Figure()
                fig_s.add_trace(go.Scatter(x=months, y=planned_cum, mode="lines+markers", name="برنامه‌ای",
                                            fill="tozeroy", fillcolor="rgba(42,91,215,0.08)",
                                            line=dict(color=COLOR_PLAN, width=3), marker=dict(size=6)))
                fig_s.add_trace(go.Scatter(x=months, y=actual_cum, mode="lines+markers", name="واقعی",
                                            line=dict(color=COLOR_ACTUAL, width=3), marker=dict(size=6)))
                fig_s.update_layout(
                    height=300, margin=dict(l=10, r=10, t=10, b=10),
                    plot_bgcolor="white", paper_bgcolor="white",
                    xaxis=dict(showgrid=False),
                    yaxis=dict(ticksuffix="٪", gridcolor="#f0f1f4"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    font=dict(family="Tahoma"),
                )
                st.plotly_chart(fig_s, use_container_width=True, config={"displayModeBar": False})
    st.write("")

# ---------- risk matrix + team table ----------
if SECTIONS["risk_matrix"] or SECTIONS["team_table"]:
    mc, tc = st.columns([1, 1.6])
    if SECTIONS["risk_matrix"]:
        with mc:
            with st.container(border=True):
                panel_header("ماتریس ریسک پروژه", "احتمال در برابر شدت اثر")
                grid_html = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;">'
                for r in range(3):
                    for c in range(3):
                        grid_html += f'<div class="risk-cell" style="background:{risk_grid[r][c]};"></div>'
                grid_html += '</div>'
                st.markdown(grid_html, unsafe_allow_html=True)
                st.markdown(
                    '<div style="display:flex;justify-content:space-between;font-size:12px;color:#8a8f9c;margin-top:8px;">'
                    '<span>کم</span><span>متوسط</span><span>زیاد</span></div>',
                    unsafe_allow_html=True,
                )
    if SECTIONS["team_table"]:
        with tc:
            with st.container(border=True):
                panel_header("آخرین فعالیت‌های بحرانی", "مواردی که نیاز به پیگیری فوری دارند")

                def status_badge(status):
                    colors = {"تاخیر دارد": "#c73434", "در حال بررسی": "#b56a1a", "طبق برنامه": "#1c8a4b"}
                    bg = {"تاخیر دارد": "#fdecec", "در حال بررسی": "#fdf1e3", "طبق برنامه": "#e6f6ec"}
                    return f'<span style="background:{bg[status]};color:{colors[status]};padding:4px 10px;border-radius:6px;font-size:12px;">{status}</span>'

                rows_html = ""
                for _, row in tasks.iterrows():
                    rows_html += f"""
                    <tr>
                        <td style="padding:10px 6px;border-bottom:1px solid #f2f3f6;">{row['فعالیت']}</td>
                        <td style="padding:10px 6px;border-bottom:1px solid #f2f3f6;">{row['طبقه']}</td>
                        <td style="padding:10px 6px;border-bottom:1px solid #f2f3f6;">{row['مسئول']}</td>
                        <td style="padding:10px 6px;border-bottom:1px solid #f2f3f6;">{row['پیشرفت']}٪</td>
                        <td style="padding:10px 6px;border-bottom:1px solid #f2f3f6;">{status_badge(row['وضعیت'])}</td>
                    </tr>
                    """
                table_html = f"""
                <table style="width:100%;border-collapse:collapse;font-size:13px;">
                    <tr>
                        <th style="text-align:right;color:#8a8f9c;font-weight:normal;padding:8px 6px;border-bottom:1px solid #eceef2;">فعالیت</th>
                        <th style="text-align:right;color:#8a8f9c;font-weight:normal;padding:8px 6px;border-bottom:1px solid #eceef2;">طبقه</th>
                        <th style="text-align:right;color:#8a8f9c;font-weight:normal;padding:8px 6px;border-bottom:1px solid #eceef2;">مسئول</th>
                        <th style="text-align:right;color:#8a8f9c;font-weight:normal;padding:8px 6px;border-bottom:1px solid #eceef2;">پیشرفت</th>
                        <th style="text-align:right;color:#8a8f9c;font-weight:normal;padding:8px 6px;border-bottom:1px solid #eceef2;">وضعیت</th>
                    </tr>
                    {rows_html}
                </table>
                """
                st.markdown(table_html, unsafe_allow_html=True)
