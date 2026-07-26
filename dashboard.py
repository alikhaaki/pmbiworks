import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Analytics Performance Hub", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

PAGE_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing:border-box; margin:0; padding:0; }
  body { font-family: -apple-system, "Segoe UI", Arial, sans-serif; background:#f4f5f8; color:#1f2430; }
  .shell { display:flex; min-height:100vh; }
  .sidebar { width:230px; background:#12172b; color:#e3e6f0; padding:22px 18px; flex-shrink:0; }
  .brand { display:flex; align-items:center; gap:10px; margin-bottom:26px; }
  .brand .logo { width:38px; height:38px; border-radius:10px; background:#2a5bd7; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:18px; }
  .brand .txt div:first-child { font-size:14px; font-weight:700; letter-spacing:0.5px; }
  .brand .txt div:last-child { font-size:11px; color:#9aa0b4; }
  .nav-item { display:flex; align-items:center; gap:10px; padding:10px 12px; border-radius:8px; font-size:13px; color:#c3c7d6; margin-bottom:2px; }
  .nav-item.active { background:#2a5bd7; color:#fff; }
  .side-section { font-size:11px; color:#7d8296; text-transform:uppercase; margin:20px 0 10px; letter-spacing:0.5px; }
  .side-field { margin-bottom:14px; }
  .side-field label { display:block; font-size:11px; color:#9aa0b4; margin-bottom:5px; }
  .side-field .box { background:#1c2338; border-radius:7px; padding:8px 10px; font-size:12px; color:#dfe2ee; }
  .profile { display:flex; align-items:center; gap:8px; margin-top:24px; padding-top:16px; border-top:1px solid #232a42; }
  .profile .av { width:30px; height:30px; border-radius:50%; background:#2a5bd7; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:bold; }
  .profile div div:first-child { font-size:12px; font-weight:600; }
  .profile div div:last-child { font-size:11px; color:#8a8f9c; }
  .main { flex:1; padding:26px 30px; }
  .head { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:20px; }
  .head h1 { font-size:22px; }
  .head p { font-size:13px; color:#8a8f9c; margin-top:4px; }
  .head-right { font-size:12px; color:#8a8f9c; display:flex; align-items:center; gap:14px; }
  .bell { position:relative; }
  .bell .dot { position:absolute; top:-4px; right:-4px; background:#e35d4f; color:#fff; font-size:9px; border-radius:50%; width:14px; height:14px; display:flex; align-items:center; justify-content:center; }
  .kpi-row { display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin-bottom:18px; }
  .kpi-card { background:#fff; border:1px solid #eceef2; border-radius:12px; padding:16px 16px 10px; }
  .kpi-top { display:flex; justify-content:space-between; align-items:flex-start; }
  .kpi-icon { width:32px; height:32px; border-radius:9px; display:flex; align-items:center; justify-content:center; font-size:14px; }
  .kpi-label { font-size:12px; color:#8a8f9c; margin-top:10px; }
  .kpi-value { font-size:19px; font-weight:700; margin-top:2px; }
  .kpi-delta { font-size:11px; color:#1c8a4b; margin-top:4px; }
  .kpi-vs { font-size:10px; color:#b3b7c2; }
  .spark { margin-top:8px; }
  .measure-row { display:flex; align-items:center; gap:10px; margin-bottom:18px; font-size:13px; }
  .measure-row .lbl { font-weight:600; margin-right:4px; }
  .pill { padding:6px 16px; border-radius:20px; border:1px solid #e1e3ea; color:#5b6070; font-size:12px; }
  .pill.active { background:#2a5bd7; color:#fff; border-color:#2a5bd7; }
  .row3 { display:grid; grid-template-columns:1.05fr 1.5fr 0.95fr; gap:16px; margin-bottom:18px; }
  .panel { background:#fff; border:1px solid #eceef2; border-radius:12px; padding:16px 18px; }
  .panel-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
  .panel-title { font-size:14px; font-weight:700; }
  .panel-sub { font-size:11px; color:#8a8f9c; margin-top:1px; }
  .chip { font-size:11px; color:#5b6070; border:1px solid #e1e3ea; border-radius:6px; padding:4px 8px; }
  .activity-row { display:flex; align-items:flex-start; gap:8px; padding:9px 0; border-bottom:1px solid #f2f3f6; }
  .activity-title { font-size:12px; font-weight:600; }
  .activity-sub { font-size:11px; color:#8a8f9c; }
  .activity-time { font-size:10px; color:#b3b7c2; margin-right:auto; white-space:nowrap; }
  .row2 { display:grid; grid-template-columns:1.3fr 1fr; gap:16px; }
  table.simple { width:100%; border-collapse:collapse; font-size:12px; }
  table.simple th { text-align:left; color:#8a8f9c; font-weight:500; padding:7px 6px; border-bottom:1px solid #eceef2; }
  table.simple td { padding:8px 6px; border-bottom:1px solid #f2f3f6; }
  .insight-box { background:#eef4ff; border-radius:10px; padding:12px 14px; font-size:12px; line-height:1.7; margin-top:10px; }
  .state-row { display:flex; align-items:center; gap:8px; font-size:12px; margin-bottom:10px; }
  .state-name { width:70px; color:#5b6070; }
  .state-bar-track { flex:1; background:#f0f1f4; border-radius:5px; height:9px; overflow:hidden; }
  .state-bar-fill { background:#2a5bd7; height:100%; border-radius:5px; }
  .state-val { width:55px; text-align:left; color:#5b6070; font-size:11px; }
</style>
</head>
<body>
<div class="shell">
  <div class="sidebar">
    <div class="brand">
      <div class="logo">A</div>
      <div class="txt"><div>ANALYTICS</div><div>PERFORMANCE HUB</div></div>
    </div>
    <div class="nav-item active">&#9635; Overview</div>
    <div class="nav-item">&#128196; Reports</div>
    <div class="nav-item">&#128101; Customers</div>
    <div class="nav-item">&#128230; Products</div>
    <div class="nav-item">&#128179; Orders</div>
    <div class="nav-item">&#128226; Marketing</div>
    <div class="nav-item">&#9881; Settings</div>
    <div class="side-section">Filters</div>
    <div class="side-field"><label>Date Range</label><div class="box">&#128197; Jan 1, 2026 &ndash; Dec 31, 2026</div></div>
    <div class="side-field"><label>Region</label><div class="box">All Regions &#9662;</div></div>
    <div class="side-field"><label>Channel</label><div class="box">All Channels &#9662;</div></div>
    <div class="profile">
      <div class="av">JD</div>
      <div><div>Jane Doe</div><div>Administrator</div></div>
    </div>
  </div>
  <div class="main">
    <div class="head">
      <div>
        <h1>Overview</h1>
        <p>Real-time performance insights and key metrics</p>
      </div>
      <div class="head-right">
        <span>&#8635; Last updated: 5m ago</span>
        <span class="bell">&#128276;<span class="dot">3</span></span>
      </div>
    </div>
    <div class="kpi-row">
      <div class="kpi-card">
        <div class="kpi-top"><div class="kpi-icon" style="background:#2a5bd722;color:#2a5bd7;">$</div><span style="color:#c7cbd6;">&#8942;</span></div>
        <div class="kpi-label">Total Revenue</div>
        <div class="kpi-value">$842,450</div>
        <div class="kpi-delta">&#9650; 18.6%</div>
        <div class="kpi-vs">vs last year $711,024</div>
        <svg class="spark" width="100%" height="24" viewBox="0 0 140 24" preserveAspectRatio="none"><polyline points="0,18 20,15 40,19 60,10 80,14 100,6 120,9 140,3" fill="none" stroke="#2a5bd7" stroke-width="2"/></svg>
      </div>
      <div class="kpi-card">
        <div class="kpi-top"><div class="kpi-icon" style="background:#7b5cf022;color:#7b5cf0;">&#8599;</div><span style="color:#c7cbd6;">&#8942;</span></div>
        <div class="kpi-label">Gross Profit</div>
        <div class="kpi-value">$152,860</div>
        <div class="kpi-delta">&#9650; 14.2%</div>
        <div class="kpi-vs">vs last year $133,668</div>
        <svg class="spark" width="100%" height="24" viewBox="0 0 140 24" preserveAspectRatio="none"><polyline points="0,20 20,17 40,14 60,16 80,9 100,12 120,6 140,4" fill="none" stroke="#7b5cf0" stroke-width="2"/></svg>
      </div>
      <div class="kpi-card">
        <div class="kpi-top"><div class="kpi-icon" style="background:#12b3a622;color:#12b3a6;">&#128722;</div><span style="color:#c7cbd6;">&#8942;</span></div>
        <div class="kpi-label">Orders</div>
        <div class="kpi-value">12,846</div>
        <div class="kpi-delta">&#9650; 9.7%</div>
        <div class="kpi-vs">vs last year 11,704</div>
        <svg class="spark" width="100%" height="24" viewBox="0 0 140 24" preserveAspectRatio="none"><polyline points="0,16 20,18 40,12 60,15 80,10 100,13 120,8 140,7" fill="none" stroke="#12b3a6" stroke-width="2"/></svg>
      </div>
      <div class="kpi-card">
        <div class="kpi-top"><div class="kpi-icon" style="background:#12b3a622;color:#12b3a6;">&#128101;</div><span style="color:#c7cbd6;">&#8942;</span></div>
        <div class="kpi-label">Customers</div>
        <div class="kpi-value">6,294</div>
        <div class="kpi-delta">&#9650; 11.3%</div>
        <div class="kpi-vs">vs last year 5,655</div>
        <svg class="spark" width="100%" height="24" viewBox="0 0 140 24" preserveAspectRatio="none"><polyline points="0,19 20,14 40,17 60,11 80,15 100,8 120,10 140,5" fill="none" stroke="#12b3a6" stroke-width="2"/></svg>
      </div>
      <div class="kpi-card">
        <div class="kpi-top"><div class="kpi-icon" style="background:#eb683422;color:#eb6834;">&#127991;</div><span style="color:#c7cbd6;">&#8942;</span></div>
        <div class="kpi-label">Avg Order Value</div>
        <div class="kpi-value">$65.54</div>
        <div class="kpi-delta">&#9650; 7.3%</div>
        <div class="kpi-vs">vs last year $61.07</div>
        <svg class="spark" width="100%" height="24" viewBox="0 0 140 24" preserveAspectRatio="none"><polyline points="0,10 20,14 40,9 60,16 80,11 100,15 120,7 140,12" fill="none" stroke="#eb6834" stroke-width="2"/></svg>
      </div>
    </div>
    <div class="measure-row">
      <span class="lbl">Select Measure</span>
      <span class="pill active">Revenue</span>
      <span class="pill">Profit</span>
      <span class="pill">Orders</span>
      <span class="pill">Quantity</span>
    </div>
    <div class="row3">
      <div class="panel">
        <div class="panel-head">
          <div><div class="panel-title">Performance Flow</div></div>
          <span class="chip">Segment: All &#9662;</span>
        </div>
        <svg viewBox="0 0 320 260" width="100%" height="260">
          <rect x="8" y="20" width="18" height="220" fill="#2a5bd7"/>
          <rect x="140" y="10" width="18" height="70" fill="#7b5cf0"/>
          <rect x="140" y="95" width="18" height="60" fill="#eb6834"/>
          <rect x="140" y="170" width="18" height="70" fill="#12b3a6"/>
          <rect x="290" y="10" width="18" height="60" fill="#9aa4c9"/>
          <rect x="290" y="80" width="18" height="55" fill="#9aa4c9"/>
          <rect x="290" y="145" width="18" height="50" fill="#9aa4c9"/>
          <rect x="290" y="205" width="18" height="45" fill="#9aa4c9"/>
          <path d="M26,30 C90,30 90,45 140,45 L140,80 C90,80 90,30 26,30 Z" fill="#2a5bd7" opacity="0.12"/>
          <path d="M26,90 C90,90 90,125 140,125 L140,155 C90,155 90,90 26,90 Z" fill="#eb6834" opacity="0.15"/>
          <path d="M26,150 C90,150 90,205 140,205 L140,240 C90,240 90,150 26,150 Z" fill="#12b3a6" opacity="0.15"/>
          <text x="30" y="135" font-size="11" fill="#1f2430" transform="rotate(-90 30 135)">Total Revenue</text>
          <text x="164" y="40" font-size="10" fill="#1f2430">Corporate</text>
          <text x="164" y="120" font-size="10" fill="#1f2430">Home Office</text>
          <text x="164" y="200" font-size="10" fill="#1f2430">Consumer</text>
          <text x="230" y="40" font-size="9" fill="#8a8f9c">Furniture</text>
          <text x="230" y="105" font-size="9" fill="#8a8f9c">Tech</text>
          <text x="230" y="170" font-size="9" fill="#8a8f9c">Office Sup.</text>
          <text x="230" y="225" font-size="9" fill="#8a8f9c">Accessories</text>
        </svg>
      </div>
      <div class="panel">
        <div class="panel-head">
          <div><div class="panel-title">Revenue Trend</div></div>
          <span class="chip" style="background:#2a5bd7;color:#fff;border-color:#2a5bd7;">Monthly</span>
        </div>
        <svg viewBox="0 0 560 240" width="100%" height="240">
          <line x1="40" y1="10" x2="40" y2="200" stroke="#e4e6ea"/>
          <line x1="40" y1="200" x2="540" y2="200" stroke="#c7cbd6"/>
          <text x="30" y="15" font-size="10" fill="#8a8f9c" text-anchor="end">$150K</text>
          <text x="30" y="105" font-size="10" fill="#8a8f9c" text-anchor="end">$100K</text>
          <text x="30" y="200" font-size="10" fill="#8a8f9c" text-anchor="end">$0</text>
          <line x1="40" y1="105" x2="540" y2="105" stroke="#f0f1f4"/>
          <path d="M60,150 L110,190 L160,175 L210,165 L260,140 L310,145 L360,105 L410,120 L460,45 L510,80"
                fill="none" stroke="#2a5bd7" stroke-width="2.5"/>
          <circle cx="60" cy="150" r="3.5" fill="#2a5bd7"/><circle cx="110" cy="190" r="3.5" fill="#2a5bd7"/>
          <circle cx="160" cy="175" r="3.5" fill="#2a5bd7"/><circle cx="210" cy="165" r="3.5" fill="#2a5bd7"/>
          <circle cx="260" cy="140" r="3.5" fill="#2a5bd7"/><circle cx="310" cy="145" r="3.5" fill="#2a5bd7"/>
          <circle cx="360" cy="105" r="3.5" fill="#2a5bd7"/><circle cx="410" cy="120" r="3.5" fill="#2a5bd7"/>
          <circle cx="460" cy="45" r="3.5" fill="#2a5bd7"/><circle cx="510" cy="80" r="3.5" fill="#2a5bd7"/>
          <text x="60" y="215" font-size="9" fill="#8a8f9c" text-anchor="middle">Jan</text>
          <text x="160" y="215" font-size="9" fill="#8a8f9c" text-anchor="middle">Mar</text>
          <text x="260" y="215" font-size="9" fill="#8a8f9c" text-anchor="middle">May</text>
          <text x="360" y="215" font-size="9" fill="#8a8f9c" text-anchor="middle">Jul</text>
          <text x="460" y="215" font-size="9" fill="#8a8f9c" text-anchor="middle">Sep</text>
          <text x="510" y="215" font-size="9" fill="#8a8f9c" text-anchor="middle">Nov</text>
        </svg>
      </div>
      <div class="panel">
        <div class="panel-title" style="margin-bottom:10px;">Recent Activity</div>
        <div class="activity-row"><span>&#128200;</span><div><div class="activity-title">Revenue increased</div><div class="activity-sub">18.6% vs last month</div></div><div class="activity-time">5m ago</div></div>
        <div class="activity-row"><span>&#128200;</span><div><div class="activity-title">Top selling category</div><div class="activity-sub">Technology</div></div><div class="activity-time">1h ago</div></div>
        <div class="activity-row"><span>&#128100;</span><div><div class="activity-title">New customer</div><div class="activity-sub">Acme Corp. joined</div></div><div class="activity-time">3h ago</div></div>
        <div class="activity-row"><span>&#127919;</span><div><div class="activity-title">Target achieved</div><div class="activity-sub">Q1 revenue goal met</div></div><div class="activity-time">1d ago</div></div>
        <div class="activity-row"><span>&#128230;</span><div><div class="activity-title">Inventory alert</div><div class="activity-sub">4 items low in stock</div></div><div class="activity-time">2d ago</div></div>
      </div>
    </div>
    <div class="row2">
      <div class="panel">
        <div class="panel-title" style="margin-bottom:12px;">Revenue by Region and Category</div>
        <table class="simple">
          <tr><th>Region</th><th>Furniture</th><th>Office Supplies</th><th>Technology</th><th>Total</th></tr>
          <tr><td>West</td><td>$97,125</td><td>$105,441</td><td>$115,892</td><td>$318,458</td></tr>
          <tr><td>South</td><td>$63,884</td><td>$71,220</td><td>$93,374</td><td>$228,478</td></tr>
          <tr><td>East</td><td>$68,775</td><td>$82,451</td><td>$111,798</td><td>$263,024</td></tr>
          <tr><td>Central</td><td>$41,056</td><td>$54,873</td><td>$63,595</td><td>$159,524</td></tr>
          <tr><td><b>Total</b></td><td><b>$270,840</b></td><td><b>$314,985</b></td><td><b>$384,659</b></td><td><b>$970,484</b></td></tr>
        </table>
      </div>
      <div class="panel">
        <div class="panel-title" style="margin-bottom:12px;">Revenue by State</div>
        <div class="state-row"><span class="state-name">California</span><div class="state-bar-track"><div class="state-bar-fill" style="width:100%"></div></div><span class="state-val">$128.9K</span></div>
        <div class="state-row"><span class="state-name">New York</span><div class="state-bar-track"><div class="state-bar-fill" style="width:64%"></div></div><span class="state-val">$82.4K</span></div>
        <div class="state-row"><span class="state-name">Texas</span><div class="state-bar-track"><div class="state-bar-fill" style="width:43%"></div></div><span class="state-val">$55.7K</span></div>
        <div class="state-row"><span class="state-name">Florida</span><div class="state-bar-track"><div class="state-bar-fill" style="width:32%"></div></div><span class="state-val">$41.3K</span></div>
        <div class="state-row"><span class="state-name">Illinois</span><div class="state-bar-track"><div class="state-bar-fill" style="width:27%"></div></div><span class="state-val">$34.8K</span></div>
        <div class="insight-box">&#128161; Technology sales are up 24% compared to last month. Consider increasing inventory.</div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

components.html(PAGE_HTML, height=1600, scrolling=False)
