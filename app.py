import streamlit as st
import math
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Software Project Cost Estimator")

# Custom CSS for RGB and Black theme
st.markdown("""
<style>
    .main {{ background-color: #000000; color: #FFFFFF; }}
    .stButton>button {{ background-color: #FF00FF; color: #FFFFFF; border-radius: 5px; border: 1px solid #FF00FF; }}
    .stButton>button:hover {{ background-color: #00FFFF; border: 1px solid #00FFFF; }}
    .stTextInput>div>div>input {{ background-color: #333333; color: #00FF00; border: 1px solid #00FF00; }}
    .stSelectbox>div>div>div {{ background-color: #333333; color: #00FF00; border: 1px solid #00FF00; }}
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{ font-size:1.2rem; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 24px; }}
    .stTabs [data-baseweb="tab"] {{ height: 50px; background: #333333; border-radius: 4px 4px 0 0; gap: 10px; padding-top: 10px; padding-bottom: 10px; }}
    .stTabs [aria-selected="true"] {{ background: #000000; border-bottom: 2px solid #FF00FF; }}
    h1, h2, h3, h4, h5, h6 {{ color: #00FFFF; }}
    .stMarkdown {{ color: #FFFFFF; }}
</style>
""", unsafe_allow_html=True)

st.title("Automated Software Project Cost Estimation Tool")

# --- COCOMO Estimation --- #
def cocomo_estimation():
    st.header("COCOMO Estimation Module")

    st.markdown("""
    The Constructive Cost Model (COCOMO) is a procedural software cost estimation model. It uses a regression formula derived from historical project data and is primarily used to estimate effort, cost, and schedule for software projects. The model uses the size of the software in KLOC (Thousands of Lines of Code) and the project type (Organic, Semi-Detached, Embedded) to determine the coefficients for its calculations.
    
    **Formulas Used:**
    *   **Effort (Person-Months):** `E = a * (KLOC ^ b)`
    *   **Duration (Months):** `D = c * (E ^ d)`
    *   **Average Staffing:** `S = E / D`
    
    Where `a, b, c, d` are coefficients based on the project type.
    """)

    col1, col2 = st.columns(2)
    with col1:
        kloc_input = st.text_input("Project Size (KLOC)", value="10.0")
    with col2:
        project_type = st.selectbox("Project Type", ["Organic", "Semi-Detached", "Embedded"])

    if st.button("Calculate COCOMO"):
        try:
            kloc = float(kloc_input)
            if kloc <= 0:
                st.error("KLOC must be a positive number.")
                return
        except ValueError:
            st.error("Invalid input for KLOC. Please enter a number.")
            return

        coefficients = {
            "Organic": {"a": 2.4, "b": 1.05, "c": 2.5, "d": 0.38},
            "Semi-Detached": {"a": 3.0, "b": 1.12, "c": 2.5, "d": 0.35},
            "Embedded": {"a": 3.6, "b": 1.20, "c": 2.5, "d": 0.32}
        }

        params = coefficients[project_type]
        effort = params["a"] * (kloc ** params["b"])
        duration = params["c"] * (effort ** params["d"])
        staffing = effort / duration

        st.subheader("COCOMO Results")
        st.write(f"**Effort (Person-Months):** {effort:.2f}")
        st.write(f"**Duration (Months):** {duration:.2f}")
        st.write(f"**Average Staffing:** {math.ceil(staffing)}")

        # Chart for COCOMO
        data = {"Metric": ["Effort", "Duration", "Staffing"],
                "Value": [effort, duration, staffing]}
        df = pd.DataFrame(data)
        fig = px.bar(df, x="Metric", y="Value", title="COCOMO Estimation Breakdown",
                     color_discrete_sequence=["#FF00FF", "#00FFFF", "#00FF00"])
        st.plotly_chart(fig)

# --- Function Point Analysis --- #
def fpa_estimation():
    st.header("Function Point Analysis Module")

    st.markdown("""
    Function Point Analysis (FPA) is a method used to measure the functional size of an information system. It quantifies the functionality provided to the user based on logical design. The calculation involves counting five user function types and applying a Value Adjustment Factor (VAF) to account for general system characteristics.
    
    **Formulas Used:**
    *   **Unadjusted Function Points (UFP):** Sum of (count * weight) for each function type.
    *   **Adjusted Function Points (AFP):** `AFP = UFP * VAF`
    *   **Estimated Effort (Person-Months):** `Effort = AFP / Productivity Rate`
    """)

    st.subheader("Input Function Point Counts")
    col1, col2, col3 = st.columns(3)
    with col1:
        ei = st.number_input("External Inputs (EI)", min_value=0, value=10)
        eo = st.number_input("External Outputs (EO)", min_value=0, value=10)
    with col2:
        eq = st.number_input("External Inquiries (EQ)", min_value=0, value=10)
        ilf = st.number_input("Internal Logical Files (ILF)", min_value=0, value=10)
    with col3:
        eif = st.number_input("External Interface Files (EIF)", min_value=0, value=10)

    st.subheader("Adjustment Factors")
    vaf = st.slider("Value Adjustment Factor (VAF)", min_value=0.5, max_value=1.5, value=1.0, step=0.01)
    productivity_rate = st.number_input("Productivity Rate (AFP/Person-Month)", min_value=0.1, value=10.0, step=0.1)

    if st.button("Calculate FPA"):
        if productivity_rate <= 0:
            st.error("Productivity Rate must be a positive number.")
            return

        weights = {"EI": 4, "EO": 5, "EQ": 4, "ILF": 10, "EIF": 7}
        
        ufp = (ei * weights["EI"]) + (eo * weights["EO"]) + (eq * weights["EQ"]) + \
              (ilf * weights["ILF"]) + (eif * weights["EIF"])
        
        afp = ufp * vaf
        effort = afp / productivity_rate

        st.subheader("FPA Results")
        st.write(f"**Unadjusted Function Points (UFP):** {ufp:.2f}")
        st.write(f"**Adjusted Function Points (AFP):** {afp:.2f}")
        st.write(f"**Estimated Effort (Person-Months):** {effort:.2f}")

        # Chart for FPA
        data = {"Metric": ["UFP", "AFP", "Effort"],
                "Value": [ufp, afp, effort]}
        df = pd.DataFrame(data)
        fig = px.bar(df, x="Metric", y="Value", title="Function Point Analysis Breakdown",
                     color_discrete_sequence=["#FF00FF", "#00FFFF", "#00FF00"])
        st.plotly_chart(fig)

# --- Financial Tracking --- #
def financial_tracking():
    st.header("Financial Tracking and Labor Costs")

    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    st.subheader("Add New Task")
    with st.form("new_task_form", clear_on_submit=True):
        task_name = st.text_input("Task Name")
        labor_cost_per_hour = st.number_input("Labor Cost per Hour ($)", min_value=0.0, value=50.0, step=0.1)
        estimated_hours = st.number_input("Estimated Hours", min_value=0.0, value=10.0, step=0.1)
        
        if st.form_submit_button("Add Task"):
            if not task_name:
                st.error("Task Name cannot be empty.")
            elif labor_cost_per_hour <= 0 or estimated_hours <= 0:
                st.error("Labor Cost per Hour and Estimated Hours must be positive numbers.")
            else:
                st.session_state.tasks.append({
                    "Task Name": task_name,
                    "Labor Cost/Hour": labor_cost_per_hour,
                    "Estimated Hours": estimated_hours,
                    "Total Cost": labor_cost_per_hour * estimated_hours
                })
                st.success(f"Task \'{task_name}\' added.")

    st.subheader("Current Tasks and Costs")
    if st.session_state.tasks:
        df_tasks = pd.DataFrame(st.session_state.tasks)
        st.dataframe(df_tasks)

        total_project_cost = df_tasks["Total Cost"].sum()
        st.markdown(f"### Total Estimated Project Cost: ${total_project_cost:,.2f}")

        # Chart for tasks
        fig = px.pie(df_tasks, values='Total Cost', names='Task Name', title='Cost Distribution by Task',
                     color_discrete_sequence=px.colors.sequential.Plasma)
        st.plotly_chart(fig)
    else:
        st.info("No tasks added yet.")

# --- Navigation Tabs --- #
tab1, tab2, tab3 = st.tabs(["COCOMO Estimation", "Function Point Analysis", "Financial Tracking"])

with tab1:
    cocomo_estimation()

with tab2:
    fpa_estimation()

with tab3:
    financial_tracking()