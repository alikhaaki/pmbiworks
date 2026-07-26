import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# دیتاست تستی
df = pd.DataFrame({
    'Name': ['ستون', 'سقف', 'دیوار', 'سفت‌کاری', 'نازک‌کاری'],
    'Planned': [80, 60, 40, 20, 10],
    'Actual': [75, 50, 35, 25, 5],
    'Delay': [5, 10, 5, 0, 5]
})

st.set_page_config(layout="wide")
st.title("📊 داشبورد با استفاده از Graph Objects")

# ایجاد یک کانتینر واحد که همه نمودارها در آن هستند
fig = make_subplots(
    rows=1, cols=3,
    specs=[[{"type": "bar"}, {"type": "pie"}, {"type": "scatter"}]],
    subplot_titles=("مقایسه پیشرفت", "سهم تاخیر", "نمودار S-Curve")
)

# تعریف Traceها
fig.add_trace(go.Bar(x=df['Name'], y=df['Actual'], name='واقعی'), row=1, col=1)
fig.add_trace(go.Pie(labels=df['Name'], values=df['Delay'], name='تاخیر'), row=1, col=2)
fig.add_trace(go.Scatter(x=df['Name'], y=df['Planned'], mode='lines+markers', name='برنامه'), row=1, col=3)

# تنظیمات تعاملی
fig.update_layout(
    height=500,
    clickmode='event+select',
    selectionrevision=True,
    showlegend=False
)

# نمایش
st.plotly_chart(fig, use_container_width=True)