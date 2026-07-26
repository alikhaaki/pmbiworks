from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'Name': ['ستون', 'سقف', 'دیوار', 'سفت‌کاری', 'نازک‌کاری'],
    'Planned': [80, 60, 40, 20, 10],
    'Actual': [75, 50, 35, 25, 5]
})

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='main-graph', figure=px.bar(df, x='Name', y='Actual', title="روی میله‌ها کلیک کن (بدون ناپدید شدن)"),
              clickData=None, selectedData=None),
    dcc.Graph(id='sub-graph')
])

@app.callback(
    Output('sub-graph', 'figure'),
    Input('main-graph', 'selectedData')
)
def update_highlight(selected_data):
    # اگر چیزی انتخاب نشده بود، کل نمودار را نشان بده
    if not selected_data or not selected_data['points']:
        return px.line(df, x='Name', y='Planned', title="نمودار کلی")
    
    # استخراج نام‌های انتخاب شده
    selected_names = [p['x'] for p in selected_data['points']]
    
    # ایجاد هایلایت: رنگ همه را خاکستری کن، انتخاب شده‌ها را رنگی
    colors = ['blue' if name in selected_names else 'lightgrey' for name in df['Name']]
    
    fig = px.bar(df, x='Name', y='Planned', title="حالت هایلایت")
    fig.update_traces(marker_color=colors)
    return fig

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)