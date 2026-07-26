import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="داشبورد مدیریت پروژه", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    html, body, [class*="css"]  { direction: rtl; text-align: right; font-family: 'Tahoma', sans-serif; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .kpi-card {
        background: #ffffff; border: 1px solid #eceef2; border-radius: 14px;
        padding: 20px 22px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .kpi-label { font-size: 13px; color: #8a8f9c; margin-bottom: 8px; }
    .kpi-value { font-size: 30px; font-weight: 700; color: #1f2430; }
    .kpi-delta-good { display:inline-block; margin-top:8px; font-size:12px; background:#e6f6ec; color:#1c8a4b; padding:3px 10px; border-radius:6px; }
    .kpi-delta-warn { display:inline-block; margin-top:8px; font-size:12px; background:#fdf1e3; color:#b56a1a; padding:3px 10px; border-radius:6px; }
    .kpi-delta-bad { display:inline-block; margin-top:8px; font-size:12px; background:#fdecec; color:#c73434; padding:3px 10px; border-radius:6px; }
    .panel-title { font-size:16px; font-weight:700; margin-bottom:2px; }
    .panel-sub { font-size:12px; color:#8a8f9c; margin-bottom: 14px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور"]
planned_cum = [15, 32, 50, 68, 85, 100]
actual_cum = [12, 28, 47, 72, 90, 103]

floors = ["طبقه ۱", "طبقه ۲", "طبقه ۳", "طبقه ۴"]
floor_planned = [75, 90, 60, 30]
floor_actual = [65, 95, 55, 34]

delay_labels = ["طبقه ۲", "طبقه ۱", "طبقه ۳", "طبقه ۴"]
delay_values = [33, 28, 22, 17]

tasks = pd.DataFrame({
    "فعالیت": ["نصب سقف کاذب", "لوله‌کشی تاسیسات", "نازک‌کاری دیوارها", "اجرای کف‌سازی"],
    "طبقه": ["طبقه ۲", "طبقه ۱", "طبقه ۳", "طبقه ۴"],
    "مسئول": ["واحد اجرا", "پیمانکار مکانیک", "واحد اجرا", "پیمانکار برق"],
    "پیشرفت": [45, 70, 90, 20],
    "وضعیت": ["تاخیر دارد", "در حال بررسی", "طبق برنامه", "تاخیر دارد"],
})

COLOR_PLAN = "#2a5bd7"
COLOR_ACTUAL = "#eb6834"

col_title, col_select, col_btn = st.columns([3, 1.2, 1])
with col_title:
    st.markdown("### داشبورد مدیریت پروژه A")
    st.caption("به‌روزرسانی خودکار بر اساس آخرین داده‌های ثبت‌شده")
with col_select:
    st.selectbox("پروژه", ["پروژه A", "پروژه B", "پروژه C"], label_visibility="collapsed")
with col_btn:
    st.button("دانلود گزارش PDF", use_container_width=True)

st.write("")

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
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta-{kind}">{delta}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

st.markdown('<div class="panel-title">منحنی S پیشرفت پروژه</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-sub">مقایسه پیشرفت تجمعی برنامه‌ای و واقعی</div>', unsafe_allow_html=True)

fig_s = go.Figure()
fig_s.add_trace(go.Scatter(x=months, y=planned_cum, mode="lines+markers", name="برنامه‌ای",
                            line=dict(color=COLOR_PLAN, width=3), marker=dict(size=7)))
fig_s.add_trace(go.Scatter(x=months, y=actual_cum, mode="lines+markers", name="واقعی",
                            line=dict(color=COLOR_ACTUAL, width=3), marker=dict(size=7)))
fig_s.update_layout(
    height=340, margin=dict(l=10, r=10, t=10, b=10),
    plot_bgcolor="white", paper_bgcolor="white",
    xaxis=dict(showgrid=False),
    yaxis=dict(title="درصد پیشرفت تجمعی", ticksuffix="٪", gridcolor="#f0f1f4"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    font=dict(family="Tahoma"),
)
st.plotly_chart(fig_s, use_container_width=True, config={"displayModeBar": False})

st.write("")

c1, c2 = st.columns([1.4, 1])

with c1:
    st.markdown('<div class="panel-title">پیشرفت به تفکیک طبقه</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-sub">درصد پیشرفت واقعی نسبت به برنامه</div>', unsafe_allow_html=True)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=floors, y=floor_planned, name="برنامه‌ای", marker_color=COLOR_PLAN))
    fig_bar.add_trace(go.Bar(x=floors, y=floor_actual, name="واقعی", marker_color=COLOR_ACTUAL))
    fig_bar.update_layout(
        barmode="group", height=320, margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white", paper_bgcolor="white",
        yaxis=dict(ticksuffix="٪", gridcolor="#f0f1f4"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(family="Tahoma"),
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

with c2:
    st.markdown('<div class="panel-title">نسبت تاخیرات</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel-sub">بر اساس تعداد موارد باز</div>', unsafe_allow_html=True)
    fig_donut = go.Figure(data=[go.Pie(
        labels=delay_labels, values=delay_values, hole=0.6,
        marker=dict(colors=[COLOR_PLAN, COLOR_ACTUAL, "#1c9e6e", "#d9a92a"]),
        textinfo="label+percent",
    )])
    fig_donut.update_layout(
        height=320, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white", showlegend=False,
        font=dict(family="Tahoma"),
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

st.write("")

st.markdown('<div class="panel-title">آخرین فعالیت‌های بحرانی</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-sub">مواردی که نیاز به پیگیری فوری دارند</div>', unsafe_allow_html=True)


def status_badge(status):
    colors = {"تاخیر دارد": "#c73434", "در حال بررسی": "#b56a1a", "طبق برنامه": "#1c8a4b"}
    bg = {"تاخیر دارد": "#fdecec", "در حال بررسی": "#fdf1e3", "طبق برنامه": "#e6f6ec"}
    return f'<span style="background:{bg[status]};color:{colors[status]};padding:4px 10px;border-radius:6px;font-size:12px;">{status}</span>'


rows_html = ""
for _, row in tasks.iterrows():
    rows_html += f"""
    <tr>
        <td style="padding:12px 8px;border-bottom:1px solid #f2f3f6;">{row['فعالیت']}</td>
        <td style="padding:12px 8px;border-bottom:1px solid #f2f3f6;">{row['طبقه']}</td>
        <td style="padding:12px 8px;border-bottom:1px solid #f2f3f6;">{row['مسئول']}</td>
        <td style="padding:12px 8px;border-bottom:1px solid #f2f3f6;">{row['پیشرفت']}٪</td>
        <td style="padding:12px 8px;border-bottom:1px solid #f2f3f6;">{status_badge(row['وضعیت'])}</td>
    </tr>
    """

table_html = f"""
<table style="width:100%;border-collapse:collapse;font-size:13px;">
    <tr>
        <th style="text-align:right;color:#8a8f9c;font-weight:normal;padding:10px 8px;border-bottom:1px solid #eceef2;">فعالیت</th>
        <th style="text-align:right;color:#8a8f9c;font-weight:normal;padding:10px 8px;border-bottom:1px solid #eceef2;">طبقه</th>
        <th style="text-align:right;color:#8a8f9c;font-weight:normal;padding:10px 8px;border-bottom:1px solid #eceef2;">مسئول</th>
        <th style="text-align:right;color:#8a8f9c;font-weight:normal;padding:10px 8px;border-bottom:1px solid #eceef2;">پیشرفت</th>
        <th style="text-align:right;color:#8a8f9c;font-weight:normal;padding:10px 8px;border-bottom:1px solid #eceef2;">وضعیت</th>
    </tr>
    {rows_html}
</table>
"""
st.markdown(table_html, unsafe_allow_html=True)
