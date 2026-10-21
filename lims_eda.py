import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from datetime import datetime,timedelta
import random
import warnings
warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('Blues_d')
print('Libraries imported successfully')

random.seed(42)   
np.random.seed(42)
n = 500   
departments = ['Haematology', 'Biochemistry', 'Microbiology',
               'Blood Banking', 'Histopathology']

tests = {
    'Haematology':    ['CBC', 'Haemoglobin', 'Platelet Count', 'ESR', 'PT'],
    'Biochemistry':   ['Glucose', 'Creatinine', 'Urea', 'SGOT', 'SGPT', 'LFT'],
    'Microbiology':   ['Culture', 'Gram Stain', 'WIDAL', 'VDRL'],
    'Blood Banking':  ['ABO Grouping', 'Cross Match', 'DAT'],
    'Histopathology': ['H&E Stain', 'Frozen Section', 'Cytology'],
}

technicians= ['Tech A', 'Tech B', 'Tech C', 'Tech D', 'Tech E']
priorities   = ['Normal', 'Urgent', 'STAT']
priorities_wt  = [0.70, 0.20, 0.10]
tat_target = {
    'Haematology': 4, 'Biochemistry': 3,
    'Microbiology': 24, 'Blood Banking': 2, 'Histopathology': 48
}
records = []
start_date = datetime(2026, 1, 1)
for i in range(n):
    dept     = random.choice(departments)
    test     = random.choice(tests[dept])
    tech     = random.choice(technicians)
    priority = random.choices(priorities, priorities_wt)[0]
    target   = tat_target[dept]
    if priority == 'STAT':
        tat = max(0.5, np.random.normal(target * 0.6, target * 0.2))
    elif priority == 'Urgent':
        tat = max(0.5, np.random.normal(target * 0.8, target * 0.3))
    else:
        tat = max(0.5, np.random.normal(target * 1.2, target * 0.5))

    delayed = 1 if tat > target else 0
    status  = 'Delayed' if delayed else 'Completed'
    coll_date = start_date + timedelta(days=random.randint(0, 179),
                                       hours=random.randint(7, 16))

    records.append({
        'SampleID':       f'S{10001 + i}',
        'Department':     dept,
        'TestName':       test,
        'TechnicianName': tech,
        'Priority':       priority,
        'TAT_Hours':      round(tat, 2),
        'TAT_Target':     target,
        'Status':         status,
        'Delayed':        delayed,
        'CollectionDate': coll_date,
        'Month':          coll_date.strftime('%b'),
        'DayOfWeek':      coll_date.strftime('%A'),
    })

df = pd.DataFrame(records)
df.to_csv('lims_data.csv', index=False)
print(f'✅ Dataset generated: {len(df)} samples')
print(df.head())
print(df.dtypes)
print('\n=== DATASET SUMMARY ===')
print(df.describe())

print('\n=== MISSING VALUES ===')
print(df.isnull().sum())

print('\n=== DEPARTMENT COUNTS ===')
print(df['Department'].value_counts())

print('\n=== STATUS DISTRIBUTION ===')
print(df['Status'].value_counts(normalize=True).round(3) * 100)

print('\n=== AVG TAT BY DEPARTMENT ===')
print(df.groupby('Department')['TAT_Hours']
        .agg(['mean','std','min','max']).round(2))

fig, ax = plt.subplots(figsize=(12, 6))
dept_order = df.groupby('Department')['TAT_Hours'].median().sort_values().index
sns.boxplot(data=df, x='Department', y='TAT_Hours',
            order=dept_order, palette='Blues', ax=ax)
ax.set_title('TAT Distribution by Department', fontsize=14, fontweight='bold')
ax.set_xlabel('Department', fontsize=12)
ax.set_ylabel('TAT Hours', fontsize=12)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('fig1_tat_boxplot.png', dpi=150)
plt.show()
delay_rate = (df.groupby('Department')['Delayed']
               .mean() * 100).sort_values(ascending=False).reset_index()
delay_rate.columns = ['Department', 'DelayRate']

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(delay_rate['Department'], delay_rate['DelayRate'],
              color=['#C00000' if x > 40 else '#2E75B6'
                     for x in delay_rate['DelayRate']])
ax.axhline(y=30, color='orange', linestyle='--', label='30% Target')
ax.set_title('Delay Rate % by Department', fontsize=14, fontweight='bold')
ax.set_ylabel('Delay Rate (%)')
ax.legend()
for bar, val in zip(bars, delay_rate['DelayRate']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('fig2_delay_rate.png', dpi=150)
plt.show()
month_order = ['Jan','Feb','Mar','Apr','May','Jun']
monthly = df.groupby(['Month','Status']).size().unstack(fill_value=0)
monthly = monthly.reindex(month_order)

fig, ax = plt.subplots(figsize=(12, 5))
monthly.plot(kind='bar', ax=ax, color=['#2E75B6','#C00000'],
             edgecolor='white', width=0.7)
ax.set_title('Monthly Sample Volume — Completed vs Delayed',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('Number of Samples')
ax.legend(['Completed','Delayed'])
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('fig3_monthly_trend.png', dpi=150)
plt.show()
tech_dept = df.pivot_table(values='TAT_Hours', index='TechnicianName',
                            columns='Department', aggfunc='mean')
fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(tech_dept, annot=True, fmt='.1f', cmap='RdYlGn_r',
            linewidths=0.5, ax=ax, cbar_kws={'label':'Avg TAT Hours'})
ax.set_title('Technician × Department TAT Heatmap',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('fig4_heatmap.png', dpi=150)
plt.show()
fig, ax = plt.subplots(figsize=(10, 5))
sns.violinplot(data=df, x='Priority', y='TAT_Hours',
               order=['STAT','Urgent','Normal'],
               palette=['#1D6B48','#2E75B6','#854F0B'], ax=ax)
ax.set_title('TAT Distribution by Priority Level',
             fontsize=14, fontweight='bold')
ax.set_ylabel('TAT Hours')
plt.tight_layout()
plt.savefig('fig5_priority_violin.png', dpi=150)
plt.show()
print('✅ All 5 charts saved to /data folder')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model  import LogisticRegression
from sklearn.ensemble       import RandomForestClassifier
from sklearn.preprocessing  import LabelEncoder, StandardScaler
from sklearn.metrics        import (accuracy_score, classification_report,
                                    confusion_matrix, roc_auc_score,
                                    roc_curve)
from sklearn.pipeline       import Pipeline
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv('lims_data.csv')
print(f'Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model  import LogisticRegression
from sklearn.ensemble       import RandomForestClassifier
from sklearn.preprocessing  import LabelEncoder, StandardScaler
from sklearn.metrics        import (accuracy_score, classification_report,
                                    confusion_matrix, roc_auc_score,
                                    roc_curve)
from sklearn.pipeline       import Pipeline
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv('lims_data.csv')
print(f'Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model  import LogisticRegression
from sklearn.ensemble       import RandomForestClassifier
from sklearn.preprocessing  import LabelEncoder, StandardScaler
from sklearn.metrics        import (accuracy_score, classification_report,
                                    confusion_matrix, roc_auc_score,
                                    roc_curve)
from sklearn.pipeline       import Pipeline
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv('lims_data.csv')
print(f'Dataset loaded: {df.shape[0]} rows x {df.shape[1]} columns')
le_dept  = LabelEncoder()
le_tech  = LabelEncoder()
le_prior = LabelEncoder()

df['Dept_Encoded']     = le_dept.fit_transform(df['Department'])
df['Tech_Encoded']     = le_tech.fit_transform(df['TechnicianName'])
df['Priority_Encoded'] = le_prior.fit_transform(df['Priority'])
features = ['Dept_Encoded', 'Tech_Encoded', 'Priority_Encoded', 'TAT_Target']
X = df[features]
y = df['Delayed']   

print(f'Features shape: {X.shape}')
print(f'Target distribution:')
print(y.value_counts(normalize=True).round(3))
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f'Train: {X_train.shape[0]} | Test: {X_test.shape[0]}')
lr_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model',  LogisticRegression(random_state=42, max_iter=1000))
])

lr_pipeline.fit(X_train, y_train)
lr_pred  = lr_pipeline.predict(X_test)
lr_proba = lr_pipeline.predict_proba(X_test)[:, 1]
lr_acc   = accuracy_score(y_test, lr_pred)
lr_auc   = roc_auc_score(y_test, lr_proba)

print(f'\n=== LOGISTIC REGRESSION ===')
print(f'Accuracy : {lr_acc:.4f} ({lr_acc*100:.1f}%)')
print(f'AUC-ROC  : {lr_auc:.4f}')
print(classification_report(y_test, lr_pred,
      target_names=['On Time', 'Delayed']))
lr_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model',  LogisticRegression(random_state=42, max_iter=1000))
])

lr_pipeline.fit(X_train, y_train)
lr_pred  = lr_pipeline.predict(X_test)
lr_proba = lr_pipeline.predict_proba(X_test)[:, 1]
lr_acc   = accuracy_score(y_test, lr_pred)
lr_auc   = roc_auc_score(y_test, lr_proba)

print(f'\n=== LOGISTIC REGRESSION ===')
print(f'Accuracy : {lr_acc:.4f} ({lr_acc*100:.1f}%)')
print(f'AUC-ROC  : {lr_auc:.4f}')
print(classification_report(y_test, lr_pred,
      target_names=['On Time', 'Delayed']))
rf_model = RandomForestClassifier(
    n_estimators=100, max_depth=10,
    random_state=42, n_jobs=-1
)
rf_model.fit(X_train, y_train)
rf_pred  = rf_model.predict(X_test)
rf_proba = rf_model.predict_proba(X_test)[:, 1]
rf_acc   = accuracy_score(y_test, rf_pred)
rf_auc   = roc_auc_score(y_test, rf_proba)

print(f'\n=== RANDOM FOREST ===')
print(f'Accuracy : {rf_acc:.4f} ({rf_acc*100:.1f}%)')
print(f'AUC-ROC  : {rf_auc:.4f}')
print(classification_report(y_test, rf_pred,
      target_names=['On Time', 'Delayed']))
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for ax, pred, title in zip(
    axes,
    [lr_pred, rf_pred],
    ['Logistic Regression', 'Random Forest']
):
    cm = confusion_matrix(y_test, pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['On Time','Delayed'],
                yticklabels=['On Time','Delayed'])
    ax.set_title(f'{title}\nAccuracy: {accuracy_score(y_test,pred)*100:.1f}%',
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')

plt.suptitle('Confusion Matrix Comparison', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('fig6_confusion_matrix.png', dpi=150)
plt.show()
fig, ax = plt.subplots(figsize=(8, 6))
for proba, label, color in [
    (lr_proba, f'Logistic Regression (AUC={lr_auc:.2f})', '#2E75B6'),
    (rf_proba, f'Random Forest       (AUC={rf_auc:.2f})', '#1D6B48'),
]:
    fpr, tpr, _ = roc_curve(y_test, proba)
    ax.plot(fpr, tpr, label=label, color=color, linewidth=2)

ax.plot([0,1],[0,1],'--', color='gray', label='Random Classifier')
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate (Recall)')
ax.set_title('ROC Curve — Model Comparison', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig('fig7_roc_curve.png', dpi=150)
plt.show()
importances = pd.DataFrame({
    'Feature':   features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=True)

fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(importances['Feature'], importances['Importance'],
        color='#2E75B6', edgecolor='white')
ax.set_title('Feature Importance — Random Forest',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Importance Score')
plt.tight_layout()
plt.savefig('fig8_feature_importance.png', dpi=150)
plt.show()
cv_lr = cross_val_score(lr_pipeline, X, y, cv=5, scoring='accuracy')
cv_rf = cross_val_score(rf_model,    X, y, cv=5, scoring='accuracy')

print('\n=== 5-FOLD CROSS VALIDATION ===')
print(f'Logistic Regression: {cv_lr.mean():.4f} ± {cv_lr.std():.4f}')
print(f'Random Forest:       {cv_rf.mean():.4f} ± {cv_rf.std():.4f}')

print('\n=== LIVE PREDICTION DEMO ===')
demo_cases = [
    {'Department':'Biochemistry','Tech':'Tech A','Priority':'STAT','Target':3},
    {'Department':'Microbiology','Tech':'Tech C','Priority':'Normal','Target':24},
    {'Department':'Haematology', 'Tech':'Tech B','Priority':'Urgent','Target':4},
]

for case in demo_cases:
    dept_e  = le_dept.transform([case['Department']])[0]
    tech_e  = le_tech.transform([case['Tech']])[0]
    prior_e = le_prior.transform([case['Priority']])[0]
    X_new   = [[dept_e, tech_e, prior_e, case['Target']]]
    pred    = rf_model.predict(X_new)[0]
    prob    = rf_model.predict_proba(X_new)[0][1]
    status  = '⚠️  DELAYED' if pred else '✅ ON TIME'
    print(f"{case['Department']:15} | {case['Priority']:6} | {status} | Delay prob: {prob:.1%}")





import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import date, timedelta

np.random.seed(42)
target_mean = 100.0
target_sd   = 3.0
days        = 30

dates  = [date(2026, 6, 1) + timedelta(days=i) for i in range(days)]

values = np.random.normal(target_mean, target_sd, days)
values[7]  = target_mean + 3.5 * target_sd   
values[14] = target_mean + 2.2 * target_sd   
values[15] = target_mean + 2.4 * target_sd   
values[22] = target_mean - 3.1 * target_sd  

qc_df = pd.DataFrame({
    'Date':    dates,
    'Value':   values.round(2),
    'Mean':    target_mean,
    'SD':      target_sd,
    'Plus1SD': target_mean + target_sd,
    'Plus2SD': target_mean + 2*target_sd,
    'Plus3SD': target_mean + 3*target_sd,
    'Min1SD':  target_mean - target_sd,
    'Min2SD':  target_mean - 2*target_sd,
    'Min3SD':  target_mean - 3*target_sd,
})
def check_westgard_rules(df):
    violations = []
    values = df['Value'].values
    mean   = df['Mean'].values[0]
    sd     = df['SD'].values[0]
    rules_violated = []
    for i, val in enumerate(values):
        z = (val - mean) / sd 
        rules_violated = []  
        if abs(z) > 3:
            rules_violated.append('1:3s REJECT')
        elif abs(z) > 2:
            rules_violated.append('1:2s WARNING')
        if i >= 1:
            z_prev = (values[i-1] - mean) / sd
            if abs(z) > 2 and abs(z_prev) > 2 and (z * z_prev > 0):
                rules_violated.append('2:2s REJECT')
        if i >= 1:
            if abs(val - values[i-1]) > 4 * sd:
                rules_violated.append('R:4s REJECT')
        if i >= 9:
            last10_z = [(v - mean)/sd for v in values[i-9:i+1]]
            if all(z > 0 for z in last10_z) or all(z < 0 for z in last10_z):
                rules_violated.append('10x REJECT')
        violations.append('; '.join(rules_violated) if rules_violated else 'In Control')
    df['WestgardStatus'] = violations    
    df['ZScore'] = [(v - mean)/sd for v in values]
    return df
qc_df = check_westgard_rules(qc_df)
print('\n=== WESTGARD RULE VIOLATIONS ===')
violations = qc_df[qc_df['WestgardStatus'] != 'In Control']
print(violations[['Date','Value','ZScore','WestgardStatus']].to_string())
fig, ax = plt.subplots(figsize=(16, 7))
ax.axhspan(target_mean - target_sd,   target_mean + target_sd,
           alpha=0.08, color='green',  label='±1 SD zone')
ax.axhspan(target_mean + target_sd,   target_mean + 2*target_sd,
           alpha=0.08, color='yellow', label='±2 SD zone')
ax.axhspan(target_mean - 2*target_sd, target_mean - target_sd,
           alpha=0.08, color='yellow')
ax.axhspan(target_mean + 2*target_sd, target_mean + 3*target_sd,
           alpha=0.10, color='red',    label='±3 SD zone')
ax.axhspan(target_mean - 3*target_sd, target_mean - 2*target_sd,
           alpha=0.10, color='red')

for level, color, style in [
    (target_mean,            'black',  '-'),
    (target_mean + target_sd,'green',  '--'),
    (target_mean - target_sd,'green',  '--'),
    (target_mean + 2*target_sd,'orange','--'),
    (target_mean - 2*target_sd,'orange','--'),
    (target_mean + 3*target_sd,'red',   '--'),
    (target_mean - 3*target_sd,'red',   '--'),
]:
     ax.axhline(y=level, color=color, linestyle=style, linewidth=1.2, alpha=0.8)
ax.plot(range(days), qc_df['Value'], 'b-o', linewidth=2,
        markersize=6, label='QC Value', zorder=5)

for i, row in qc_df.iterrows():
    if '3s' in row['WestgardStatus'] or 'R:4s' in row['WestgardStatus']:
        ax.plot(i, row['Value'], 'r*', markersize=18, zorder=6)
        ax.annotate(row['WestgardStatus'], (i, row['Value']),
                    textcoords='offset points', xytext=(8,8),
                    fontsize=8, color='red', fontweight='bold')
    elif 'WARNING' in row['WestgardStatus']:
        ax.plot(i, row['Value'], 'y^', markersize=12, zorder=6)

ax.set_title('Levey-Jennings QC Chart — Glucose Control (Level 1)\n'
             'Target Mean: 100 mg/dL  |  SD: 3.0  |  30 Days',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Day', fontsize=12)
ax.set_ylabel('Glucose Control Value (mg/dL)', fontsize=12)
ax.set_xticks(range(0, days, 2))
ax.set_xticklabels([str(i+1) for i in range(0, days, 2)])
ax.set_yticks([target_mean + i*target_sd for i in range(-3,4)])
ax.set_yticklabels([f'{target_mean+i*target_sd:.0f}\n({["-3SD","-2SD","-1SD","Mean","+1SD","+2SD","+3SD"][i+3]})'
                    for i in range(-3,4)])

ax.legend(loc='upper right', fontsize=9)
plt.tight_layout()
plt.savefig('fig9_levey_jennings.png', dpi=150, bbox_inches='tight')
plt.show()
print('✅ Levey-Jennings chart saved')

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
st.set_page_config(
    page_title='Clinical LIMS Analytics',
    page_icon='🏥',
    layout='wide'
)
st.markdown('''<style>
.metric-card {
    background:#1F4E79; color:white;
    padding:1rem; border-radius:8px; text-align:center;
}
.stMetric label { font-size:13px !important; }
</style>''', unsafe_allow_html=True)
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
st.sidebar.image('https://img.icons8.com/color/96/hospital.png', width=80)
st.sidebar.title('🏥 LIMS Analytics')
st.sidebar.markdown('---')
page = st.sidebar.radio('Navigation',
    ['📊 Dashboard', '🤖 TAT Predictor', '📈 Department Analysis', '👤 About'])

if page == '📊 Dashboard':
    st.title('🏥 Clinical LIMS Quality Dashboard')
    st.markdown('*Built by Vignesh Karuppan | B.Sc. MLT | KMCH Intern*')
    st.markdown('---')

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
            Total=('SampleID','count'),
            AvgTAT=('TAT_Hours','mean'),
            DelayRate=('Delayed','mean')
        ).round(2)
        kpi['DelayRate'] = (kpi['DelayRate']*100).map('{:.1f}%'.format)
        st.dataframe(kpi, use_container_width=True)
    st.subheader('Raw Data')
    st.dataframe(filtered.head(50), use_container_width=True)

                    
             




      
        


            
               



