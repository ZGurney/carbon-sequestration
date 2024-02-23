import streamlit as st

pound_kilo_ratio = 0.45359237
feet_meters_ratio = 0.3048
inch_meters_ratio = 0.0254

average_emissions_per_capita = 11.7 * 1000 #kgCO2e/year

def calculate_co2_captured(diameter, height, tree_age):
    # Step 1: Calculate green weight above ground
    if diameter < 11:
        coefficient = 0.25
    else:
        coefficient = 0.15

    height = height / feet_meters_ratio
    diameter = diameter / inch_meters_ratio

    green_weight_above_ground = coefficient * height * diameter**2
    green_weight_above_ground = pound_kilo_ratio * green_weight_above_ground

    # Step 2: Calculate green weight total
    green_weight_total = 1.2 * green_weight_above_ground

    # Step 3: Calculate dry weight
    dry_weight = 0.725 * green_weight_total

    # Step 4: Calculate carbon content
    carbon_content = 0.5 * dry_weight

    # Step 5: Calculate CO2 captured
    carbon_atomic_weight = 12.00
    oxygen_atomic_weight = 16.00
    co2_weight = carbon_atomic_weight + 2 * oxygen_atomic_weight
    co2_carbon_ratio = co2_weight / carbon_atomic_weight

    co2_captured = co2_carbon_ratio * carbon_content

    # Step 6: Calculate CO2 captured per year
    annual_co2_captured = co2_captured / tree_age

    # Step 7: Calculate CO2 captured per year for one tiny forest
    tiny_forest_co2_captured = 600 * annual_co2_captured

    # Step 8: Calculate CO2 captured per year for all tiny forests
    all_tiny_forests_co2_captured = num_tiny_forests * tiny_forest_co2_captured

    return all_tiny_forests_co2_captured

def calculate_employee_emissions(num_employees, average_emissions_per_capita):
    employee_emissions = num_employees * average_emissions_per_capita
    return employee_emissions

def format_large_number(number):
    number = number/1000 # convert to kilotons
    return "{:,.0f}".format(number)

st.set_page_config(layout="wide", page_title="Tiny Forests Carbon Capture Calculator")
st.title("Tiny Forests Carbon Capture Calculator")

col1, col2 = st.columns(2, gap="large")

with col1:
    diameter = st.slider("Enter the diameter of the tree (in metres):", min_value=0.0, max_value=1.0, value=0.4)
    height = st.slider("Enter the height of the tree (in metres):", min_value=0.0, max_value=100.0, value=20.0)
    tree_age = st.slider("Enter the age of the tree (in years):", min_value=0, max_value=1000, value=200, step=1)
    num_tiny_forests = st.slider("Enter the number of tiny forests:", min_value=0, max_value=200, value=10, step=1)
    num_employees = st.slider("Enter the number of employees:", min_value=0, max_value=10000, value=10, step=1)
    

if tree_age == 0:
    # Display a warning if the tree age is zero
    with col2:
        st.warning("Please enter a non-zero age for the tree.")
else:
    co2_captured = calculate_co2_captured(diameter, height, tree_age)
    employee_emissions = calculate_employee_emissions(num_employees, average_emissions_per_capita)
    proportion_captured = co2_captured / employee_emissions
    proportion_captured_percentage = proportion_captured * 100

    # Display data as a table
    table_data = {
        'Metrics': ['Total carbon emissions captured', 'Total carbon emissions by employees', 'Proportion of carbon emissions captured'],
        'Values': [format_large_number(co2_captured) + ' tCO2/year', format_large_number(employee_emissions) + ' tCO2e/year', "{:.2f}%".format(proportion_captured_percentage)]
    }
    # Create a bar chart to compare CO2 captured and employee emissions
    chart_data = {'Tiny forests': co2_captured, 'Employees': employee_emissions}

    with col2:
        table_data = st.dataframe(table_data, hide_index=True)
        #st.table(table_data)
        st.bar_chart(chart_data)

# References

# Import README.md into a string
with open("README.md", "r") as file:
    explanation = file.read()

with st.expander("See details of the project"):
    st.markdown(explanation)