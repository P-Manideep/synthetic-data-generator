import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from generator import ScenarioDataGenerator
from scenarios import (
    create_ecommerce_scenario,
    create_fraud_detection_scenario,
    create_sensor_data_scenario,
    create_customer_churn_scenario
)

st.set_page_config(
    page_title="Synthetic Data Generator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    section[data-testid="stSidebar"] {
        background-color: #1a1d26;
        border-right: 1px solid #2e3347;
    }
    div[data-testid="metric-container"] {
        background-color: #1a1d26;
        border: 1px solid #2e3347;
        border-radius: 10px;
        padding: 15px;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 0;
        font-size: 16px;
        font-weight: 700;
    }
    .stButton > button:hover { opacity: 0.85; color: white; }
    .stDownloadButton > button {
        width: 100%;
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 0;
        font-size: 16px;
        font-weight: 700;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1d26;
        border-radius: 10px;
        padding: 4px;
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] { color: #aaa; border-radius: 6px; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: #667eea !important; color: white !important; }
    .info-box {
        background-color: #1a1d26;
        border: 1px solid #2e3347;
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 8px 0;
        color: #ccc;
    }
    .success-box {
        background-color: #1a2e1a;
        border: 1px solid #2e4a2e;
        border-left: 4px solid #38ef7d;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 8px 0;
        color: #ccc;
    }
</style>
""", unsafe_allow_html=True)

SCENARIO_INFO = {
    "E-commerce Orders": {
        "func": create_ecommerce_scenario,
        "key": "ecommerce",
        "icon": "🛒",
        "description": "Online shopping orders with customer segments, discounts and shipping",
        "color": "#667eea"
    },
    "Fraud Detection": {
        "func": create_fraud_detection_scenario,
        "key": "fraud_detection",
        "icon": "🔍",
        "description": "Transaction data with fraud indicators for testing detection systems",
        "color": "#ef4444"
    },
    "IoT Sensor Data": {
        "func": create_sensor_data_scenario,
        "key": "sensor_data",
        "icon": "📡",
        "description": "Temperature, humidity and pressure readings from 50 sensors",
        "color": "#f59e0b"
    },
    "Customer Churn": {
        "func": create_customer_churn_scenario,
        "key": "customer_churn",
        "icon": "👥",
        "description": "Customer subscription data with churn predictions based on tenure",
        "color": "#10b981"
    }
}

def generate_data(scenario_name, num_records):
    info = SCENARIO_INFO[scenario_name]
    scenario = info["func"]()
    generator = ScenarioDataGenerator(scenario)
    df = generator.generate_dataset(num_records=num_records)
    if info["key"] == "ecommerce":
        df['total'] = df['order_value'] - df['discount'] + df['shipping_cost']
    elif info["key"] == "customer_churn":
        df['total_charges'] = df['tenure_months'] * df['monthly_charges']
    return df

with st.sidebar:
    st.markdown("## 🧪 Synthetic Data Generator")
    st.markdown("---")
    st.markdown("### 📋 Select Scenario")
    selected_scenario = st.selectbox(
        label="Scenario",
        options=list(SCENARIO_INFO.keys()),
        format_func=lambda x: f"{SCENARIO_INFO[x]['icon']}  {x}",
        label_visibility="collapsed"
    )
    info = SCENARIO_INFO[selected_scenario]
    st.markdown(f"""
    <div class="info-box">
        <strong>{info['icon']} {selected_scenario}</strong><br>
        <small>{info['description']}</small>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🔢 Number of Records")
    num_records = st.slider(
        label="Records",
        min_value=100,
        max_value=10000,
        value=500,
        step=100,
        label_visibility="collapsed"
    )
    st.caption(f"Will generate **{num_records:,}** records")
    st.markdown("---")
    generate_clicked = st.button("Generate Data", use_container_width=True)
    st.markdown("---")
    st.markdown("""
    <small style='color:#666;'>
    Project 1 - Synthetic Data Generator<br>
    Built with Python, Pandas and Streamlit
    </small>
    """, unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center; font-size:42px; margin-bottom:0;'>
    🧪 Synthetic Data Generator
</h1>
<p style='text-align:center; color:#aaa; font-size:16px; margin-top:8px;'>
    Generate realistic scenario-driven datasets for testing and development
</p>
""", unsafe_allow_html=True)

st.markdown("---")

if 'df' not in st.session_state:
    st.markdown("### 🎯 Choose a Scenario to Get Started")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    cols = [col1, col2, col3, col4]
    for idx, (name, details) in enumerate(SCENARIO_INFO.items()):
        with cols[idx]:
            st.markdown(f"""
            <div style='
                background-color:#1a1d26;
                border:1px solid #2e3347;
                border-top: 4px solid {details["color"]};
                border-radius:10px;
                padding:20px;
                text-align:center;
                height:160px;
            '>
                <div style='font-size:36px'>{details["icon"]}</div>
                <div style='font-size:16px; font-weight:700; color:#fff; margin:8px 0 6px 0;'>{name}</div>
                <div style='font-size:12px; color:#888;'>{details["description"]}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("Select a scenario from the sidebar and click Generate Data to begin!")

if generate_clicked:
    with st.spinner(f"Generating {num_records:,} records..."):
        try:
            df = generate_data(selected_scenario, num_records)
            st.session_state['df'] = df
            st.session_state['scenario'] = selected_scenario
            st.success(f"Successfully generated {len(df):,} records!")
        except Exception as e:
            st.error(f"Error: {e}")

if 'df' in st.session_state:
    df = st.session_state['df']
    scenario_name = st.session_state['scenario']
    info = SCENARIO_INFO[scenario_name]

    st.markdown(f"### {info['icon']} {scenario_name} Overview")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Records", f"{len(df):,}")
    with m2:
        st.metric("Total Columns", f"{len(df.columns)}")
    with m3:
        st.metric("Scenario", scenario_name)
    with m4:
        st.metric("Missing Values", f"{df.isnull().sum().sum()}")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Data Table",
        "Charts",
        "Statistics",
        "Download"
    ])

    with tab1:
        st.markdown("#### Generated Data")
        rows_to_show = st.slider("Rows to display", 5, min(500, len(df)), 20)
        st.dataframe(df.head(rows_to_show), use_container_width=True, height=400)
        st.caption(f"Showing {rows_to_show} of {len(df):,} total records")

    with tab2:
        st.markdown("#### Visual Analysis")

        if info['key'] == 'ecommerce':
            c1, c2 = st.columns(2)
            with c1:
                seg_counts = df['customer_segment'].value_counts().reset_index()
                seg_counts.columns = ['Segment', 'Count']
                fig = px.pie(seg_counts, values='Count', names='Segment',
                    title='Customer Segment Distribution',
                    color_discrete_sequence=['#667eea', '#764ba2', '#a855f7'], hole=0.4)
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig = px.histogram(df, x='order_value', nbins=30,
                    title='Order Value Distribution',
                    color_discrete_sequence=['#667eea'])
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            c3, c4 = st.columns(2)
            with c3:
                seg_rev = df.groupby('customer_segment')['order_value'].sum().reset_index()
                fig = px.bar(seg_rev, x='customer_segment', y='order_value',
                    title='Total Revenue by Segment', color='customer_segment',
                    color_discrete_sequence=['#667eea', '#764ba2', '#a855f7'])
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white', showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            with c4:
                fig = px.scatter(df.sample(min(300, len(df))),
                    x='order_value', y='discount',
                    title='Discount vs Order Value', color='customer_segment',
                    color_discrete_sequence=['#667eea', '#764ba2', '#a855f7'], opacity=0.7)
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)

        elif info['key'] == 'fraud_detection':
            c1, c2 = st.columns(2)
            with c1:
                fraud_counts = df['is_fraud'].value_counts().reset_index()
                fraud_counts.columns = ['Status', 'Count']
                fraud_counts['Status'] = fraud_counts['Status'].map({True: 'Fraud', False: 'Legitimate'})
                fig = px.pie(fraud_counts, values='Count', names='Status',
                    title='Fraud vs Legitimate Transactions',
                    color_discrete_sequence=['#ef4444', '#10b981'], hole=0.4)
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                type_counts = df['transaction_type'].value_counts().reset_index()
                type_counts.columns = ['Type', 'Count']
                fig = px.bar(type_counts, x='Type', y='Count',
                    title='Transaction Type Distribution', color='Type',
                    color_discrete_sequence=['#ef4444', '#f97316', '#eab308', '#10b981'])
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white', showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            c3, c4 = st.columns(2)
            with c3:
                fig = px.histogram(df, x='amount', nbins=40,
                    title='Transaction Amount Distribution',
                    color_discrete_sequence=['#ef4444'])
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            with c4:
                device_counts = df['device_type'].value_counts().reset_index()
                device_counts.columns = ['Device', 'Count']
                fig = px.pie(device_counts, values='Count', names='Device',
                    title='Device Type Distribution',
                    color_discrete_sequence=['#ef4444', '#f97316', '#eab308'], hole=0.4)
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)

        elif info['key'] == 'sensor_data':
            c1, c2 = st.columns(2)
            with c1:
                fig = px.histogram(df, x='temperature', nbins=30,
                    title='Temperature Distribution (C)',
                    color_discrete_sequence=['#f59e0b'])
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                status_counts = df['status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                fig = px.pie(status_counts, values='Count', names='Status',
                    title='Sensor Status Distribution',
                    color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444'], hole=0.4)
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            c3, c4 = st.columns(2)
            with c3:
                fig = px.scatter(df.sample(min(300, len(df))),
                    x='temperature', y='humidity', color='status',
                    title='Temperature vs Humidity',
                    color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444'], opacity=0.7)
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            with c4:
                fig = px.histogram(df, x='humidity', nbins=30,
                    title='Humidity Distribution (%)',
                    color_discrete_sequence=['#3b82f6'])
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)

        elif info['key'] == 'customer_churn':
            c1, c2 = st.columns(2)
            with c1:
                churn_counts = df['has_churned'].value_counts().reset_index()
                churn_counts.columns = ['Status', 'Count']
                churn_counts['Status'] = churn_counts['Status'].map({True: 'Churned', False: 'Retained'})
                fig = px.pie(churn_counts, values='Count', names='Status',
                    title='Churn vs Retained Customers',
                    color_discrete_sequence=['#ef4444', '#10b981'], hole=0.4)
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                contract_counts = df['contract_type'].value_counts().reset_index()
                contract_counts.columns = ['Contract', 'Count']
                fig = px.bar(contract_counts, x='Contract', y='Count',
                    title='Contract Type Distribution', color='Contract',
                    color_discrete_sequence=['#10b981', '#3b82f6', '#8b5cf6'])
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white', showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            c3, c4 = st.columns(2)
            with c3:
                fig = px.histogram(df, x='tenure_months', nbins=30,
                    title='Tenure Distribution (months)',
                    color_discrete_sequence=['#10b981'])
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)
            with c4:
                fig = px.histogram(df, x='monthly_charges', nbins=30,
                    title='Monthly Charges Distribution ($)',
                    color_discrete_sequence=['#8b5cf6'])
                fig.update_layout(paper_bgcolor='#1a1d26', plot_bgcolor='#1a1d26',
                    font_color='white', title_font_color='white')
                st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("#### Statistical Summary")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Numeric Columns**")
            st.dataframe(df.describe().round(2), use_container_width=True)
        with c2:
            st.markdown("**Column Info**")
            info_data = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.values.astype(str),
                'Non-Null': df.count().values,
                'Nulls': df.isnull().sum().values,
                'Unique': df.nunique().values
            })
            st.dataframe(info_data, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("**Key Insights**")
        kc1, kc2, kc3, kc4 = st.columns(4)

        if info['key'] == 'ecommerce':
            with kc1:
                st.metric("Total Revenue", f"${df['order_value'].sum():,.0f}")
            with kc2:
                st.metric("Avg Order Value", f"${df['order_value'].mean():,.2f}")
            with kc3:
                st.metric("Total Discounts", f"${df['discount'].sum():,.0f}")
            with kc4:
                st.metric("Avg Shipping", f"${df['shipping_cost'].mean():,.2f}")
        elif info['key'] == 'fraud_detection':
            with kc1:
                st.metric("Total Transactions", f"{len(df):,}")
            with kc2:
                st.metric("Fraud Cases", f"{df['is_fraud'].sum()}")
            with kc3:
                st.metric("Fraud Rate", f"{df['is_fraud'].mean()*100:.2f}%")
            with kc4:
                st.metric("Avg Amount", f"${df['amount'].mean():,.2f}")
        elif info['key'] == 'sensor_data':
            with kc1:
                st.metric("Avg Temperature", f"{df['temperature'].mean():.1f}C")
            with kc2:
                st.metric("Avg Humidity", f"{df['humidity'].mean():.1f}%")
            with kc3:
                st.metric("Critical Alerts", f"{(df['status']=='critical').sum()}")
            with kc4:
                st.metric("Unique Sensors", f"{df['sensor_id'].nunique()}")
        elif info['key'] == 'customer_churn':
            with kc1:
                st.metric("Total Customers", f"{len(df):,}")
            with kc2:
                st.metric("Churn Rate", f"{df['has_churned'].mean()*100:.1f}%")
            with kc3:
                st.metric("Avg Tenure", f"{df['tenure_months'].mean():.1f} mo")
            with kc4:
                st.metric("Avg Monthly Bill", f"${df['monthly_charges'].mean():.2f}")

    with tab4:
        st.markdown("#### Download Your Dataset")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="success-box">
                Ready to Download!<br><br>
                Records: {len(df):,}<br>
                Columns: {len(df.columns)}<br>
                Scenario: {scenario_name}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"{info['key']}_synthetic_data.csv",
                mime='text/csv',
                use_container_width=True
            )
            st.caption(f"File size: ~{len(csv) / 1024:.1f} KB")