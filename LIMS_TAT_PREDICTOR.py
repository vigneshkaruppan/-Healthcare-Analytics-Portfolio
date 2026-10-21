# ============================================================
# PROJECT 4: LIMS TAT PREDICTOR — STREAMLIT WEB APP
# Author: Vignesh Karuppan
# Run command: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble       import RandomForestClassifier
from sklearn.preprocessing  import LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# ── Page config ──────────────────────────────────────
st.set_page_config(
    page_title='Clinical LIMS Analytics',
    page_icon='🏥',
    layout='wide'
)

# ── Custom CSS ───────────────────────────────────────
st.markdown('''<style>
.metric-card {
    background:#1F4E79; color:white;
    padding:1rem; border-radius:8px; text-align:center;
}
.stMetric label { font-size:13px !important; }
</style>''', unsafe_allow_html=True)

# ── Load & train model ───────────────────────────────
@st.cache_data
def load_and_train():
    import random
    from datetime import datetime, timedelta
    random.seed(42); np.random.seed(42)
    n = 500
    departments = ['Haematology','Biochemistry','Microbiology',
                   'Blood Banking','Histopathology']
    tat_targets = {'Haematology':4,'Biochemistry':3,
                   'Microbiology':24,'Blood Banking':2,'Histopathology':48}
    technicians = ['Tech A','Tech B','Tech C','Tech D','Tech E']
    priorities  = ['Normal','Urgent','STAT']
    records = []
    for _ in range(n):
        dept  = random.choice(departments)
        tech  = random.choice(technicians)
        prior = random.choices(priorities,[0.7,0.2,0.1])[0]
        tgt   = tat_targets[dept]
        mult  = {'STAT':0.6,'Urgent':0.8,'Normal':1.2}[prior]
        tat   = max(0.5, np.random.normal(tgt*mult, tgt*0.4))
        records.append({'Department':dept,'TechnicianName':tech,
                         'Priority':prior,'TAT_Target':tgt,
                         'TAT_Hours':round(tat,2),'Delayed':int(tat>tgt)})
    df = pd.DataFrame(records)
    le_d = LabelEncoder(); le_t = LabelEncoder(); le_p = LabelEncoder()
    df['D'] = le_d.fit_transform(df['Department'])
    df['T'] = le_t.fit_transform(df['TechnicianName'])
    df['P'] = le_p.fit_transform(df['Priority'])
    X = df[['D','T','P','TAT_Target']]
    y = df['Delayed']
    Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=0.2,random_state=42)
    model = RandomForestClassifier(n_estimators=100,random_state=42)
    model.fit(Xtr,ytr)
    acc = model.score(Xte,yte)
    return df, model, le_d, le_t, le_p, acc

df, model, le_d, le_t, le_p, acc = load_and_train()

# ── Sidebar ──────────────────────────────────────────
st.sidebar.image('https://img.icons8.com/color/96/hospital.png', width=80)
st.sidebar.title('🏥 LIMS Analytics')
st.sidebar.markdown('---')
page = st.sidebar.radio('Navigation',
    ['📊 Dashboard', '🤖 TAT Predictor', '📈 Department Analysis', '👤 About'])

# ── PAGE 1: DASHBOARD ────────────────────────────────
if page == '📊 Dashboard':
    st.title('🏥 Clinical LIMS Quality Dashboard')
    st.markdown('*Built by Vignesh Karuppan | B.Sc. MLT | KMCH Intern*')
    st.markdown('---')

    # KPI cards
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric('Total Samples',  len(df))
    c2.metric('Avg TAT (hrs)',   f"{df['TAT_Hours'].mean():.1f}")
    c3.metric('Delay Rate',     f"{df['Delayed'].mean()*100:.1f}%")
    c4.metric('On Time',        f"{(1-df['Delayed'].mean())*100:.1f}%")
    c5.metric('Model Accuracy', f"{acc*100:.1f}%")

    st.markdown('---')
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Delay Rate by Department')
        delay = df.groupby('Department')['Delayed'].mean()*100
        fig,ax = plt.subplots(figsize=(6,4))
        delay.sort_values().plot(kind='barh', ax=ax, color='#2E75B6')
        ax.set_xlabel('Delay Rate (%)')
        ax.axvline(30, color='red', linestyle='--', label='30% limit')
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader('Status Distribution')
        status_ct = df['Delayed'].value_counts()
        fig,ax = plt.subplots(figsize=(6,4))
        ax.pie(status_ct, labels=status_ct.index,
               colors=['#1D6B48','#C00000'],
               autopct='%1.1f%%', startangle=90)
        plt.tight_layout()
        st.pyplot(fig)

# ── PAGE 2: PREDICTOR ────────────────────────────────
elif page == '🤖 TAT Predictor':
    st.title('🤖 TAT Delay Predictor')
    st.markdown('Predict whether a lab sample will be delayed before processing.')
    st.markdown('---')

    col1, col2 = st.columns(2)
    with col1:
        dept  = st.selectbox('Department',
                   ['Haematology','Biochemistry','Microbiology',
                    'Blood Banking','Histopathology'])
        tech  = st.selectbox('Technician',
                   ['Tech A','Tech B','Tech C','Tech D','Tech E'])
    with col2:
        prior = st.selectbox('Priority', ['Normal','Urgent','STAT'])
        tat_t = st.slider('TAT Target (hours)', 1, 48, 4)

    if st.button('🔍 Predict TAT Status', type='primary'):
        X_new = [[le_d.transform([dept])[0],
                  le_t.transform([tech])[0],
                  le_p.transform([prior])[0],
                  tat_t]]
        pred = model.predict(X_new)[0]
        prob = model.predict_proba(X_new)[0][1]
        if pred:
            st.error(f'⚠️ DELAYED — Delay probability: {prob:.1%}')
            st.warning('Recommend: Escalate to senior technician or change priority to STAT')
        else:
            st.success(f'✅ ON TIME — Delay probability: {prob:.1%}')
            st.info('Sample is likely to be completed within TAT target')
        st.progress(float(prob))

# ── PAGE 3: DEPARTMENT ANALYSIS ──────────────────────
elif page == '📈 Department Analysis':
    st.title('📈 Department-wise Analysis')
    dept_sel = st.multiselect('Select Departments',
                  df['Department'].unique().tolist(),
                  default=df['Department'].unique().tolist())
    filtered = df[df['Department'].isin(dept_sel)]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('TAT Box Plot')
        fig,ax = plt.subplots(figsize=(6,4))
        sns.boxplot(data=filtered, x='Department',
                    y='TAT_Hours', palette='Blues', ax=ax)
        plt.xticks(rotation=20)
        plt.tight_layout()
        st.pyplot(fig)
    with col2:
        st.subheader('Technician KPI')
        
        kpi = filtered.groupby('TechnicianName').agg(
            Total=("TechnicianName",'count'),
            AvgTAT=('TAT_Hours','mean'),
            DelayRate=('Delayed','mean')
        ).round(2)
        kpi['DelayRate'] = (kpi['DelayRate']*100).map('{:.1f}%'.format)
        st.dataframe(kpi, use_container_width=True)

    st.subheader('Raw Data')
    st.dataframe(filtered.head(50), use_container_width=True)

# ── PAGE 4: ABOUT ────────────────────────────────────
elif page == '👤 About':
    st.title('👤 About This Project')
    st.markdown('''
    ### Vignesh Karuppan
    **B.Sc. Medical Laboratory Technology** | KMCH, Coimbatore

    #### Technical Stack
    - **Python 3.12** — pandas, numpy, matplotlib, seaborn
    - **Machine Learning** — scikit-learn RandomForestClassifier
    - **Web Framework** — Streamlit
    - **Database** — SQL Server 2022 (LIMS_Practice)
    - **Visualization** — Power BI (separate dashboard)

    #### Clinical Domain Knowledge
    - 1 year internship at KMCH across 5 departments
    - GLP / GDP / NABL / ALCOA+ documentation
    - Levey-Jennings QC + Westgard rules

    #### Contact
    📧 vigneshkaruppan911@gmail.com  |  📍 Coimbatore, Tamil Nadu
    ''')
