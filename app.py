import streamlit as st

# Define imperial-metric conversion ratios
pound_kilo_ratio = 0.45359237
feet_meters_ratio = 0.3048
inch_meters_ratio = 0.0254

average_emissions_per_capita = 4.7 * 1000 #kgCO2e/year

def calculate_co2_captured(diameter: float, height: float, tree_age: float) -> float:
    """
    Calculate the amount of CO2 captured by a tree over its lifetime.

    Parameters:
    - diameter (float): The diameter of the tree trunk in centimetres.
    - height (float): The height of the tree in metres.
    - tree_age (float): The age of the tree in years.

    Returns:
    - float: The amount of CO2 captured per year for all tiny forests.

    The function calculates the amount of CO2 captured by a tree based on its diameter, height, and age.
    It follows a series of steps to estimate the CO2 captured, including calculating the green weight above ground,
    the green weight total, the dry weight, the carbon content, and the CO2 captured per year.
    Finally, it calculates the CO2 captured per year for one tiny forest and for all tiny forests.

    Note: The function assumes certain conversion ratios and metrics, which are not provided in the code snippet.
    """
    # Step 1: Calculate green weight above ground
    height = height / feet_meters_ratio
    diameter = diameter / 100 / inch_meters_ratio

    if diameter < 11:
        coefficient = 0.25
    else:
        coefficient = 0.15

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
    all_tiny_forests_co2_captured = metrics["num_tiny_forests"] * tiny_forest_co2_captured

    return all_tiny_forests_co2_captured

def calculate_employee_emissions(num_employees: int, average_emissions_per_capita: float) -> float:
    """
    Calculates the total emissions produced by a given number of employees.

    Args:
        num_employees (int): The number of employees.
        average_emissions_per_capita (float): The average emissions per capita.

    Returns:
        float: The total emissions produced by the employees.

    """
    employee_emissions = num_employees * average_emissions_per_capita
    return employee_emissions

def format_large_number(number: float) -> str:
    """
    Formats a large number by converting it to kilotons and returning a formatted string.

    Args:
        number (float): The number to be formatted.

    Returns:
        str: The formatted number as a string.
    """
    number = number/1000 # convert to kilotons
    return "{:,.0f}".format(number)

st.set_page_config(layout="wide", page_title="Tiny Forests Carbon Capture Calculator")
st.image(["logo.png"], output_format="png", width=300)
st.title("Tiny Forests Carbon Capture Calculator")

col1, col2 = st.columns(2, gap="large")

st.markdown("""
<style>
    button.step-up {display: none;}
    button.step-down {display: none;}
    div[data-baseweb] {border-radius: 4px;}
</style>""",
unsafe_allow_html=True)

def update(name: str):
    """
    Update the session state variable based on the given name.

    Parameters:
        name (str): The name of the session state variable.

    Returns:
        None
    """
    st.session_state[name + "_slider"] = st.session_state[name + "_number"]

def create_input(name, text, initial_value, min_value, max_value, step):
    """
    Create an input widget consisting of a number input and a slider.

    Parameters:
    - name (str): The name of the input widget.
    - text (str): The text to display above the input widget.
    - initial_value (float/int): The initial value of the input widget.
    - min_value (float/int): The minimum value of the input widget.
    - max_value (float/int): The maximum value of the input widget.
    - step (float/int): The step size of the input widget.

    Returns:
    None
    """
    st.write(text)
    columns[name + "_number"], columns[name + "_slider"] = st.columns([0.3, 0.7]) # Create two columns
    # Create a number input widget
    with columns[name + "_number"]:
        st.number_input("Number", label_visibility="collapsed", value=initial_value, min_value=min_value, max_value=max_value, step=step, key=name+"_number", args=(name,), on_change=update)
    # Create a slider widget
    with columns[name + "_slider"]:
        metrics[name] = st.slider("Slider", label_visibility="collapsed", value=initial_value, min_value=min_value, max_value=max_value, step=step, key=name+"_slider")

with col1:
    metrics = {}
    columns = {}
    create_input("diameter", "Enter the diameter of the tree (in centimetres):", 40, 0, 100, 1)
    create_input("height", "Enter the height of the tree (in metres):", 15.0, 0.0, 50.0, 0.1)
    create_input("tree_age", "Enter the age of the tree (in years):", 10.0, 0.0, 100.0, 1.0)
    create_input("num_tiny_forests", "Enter the number of tiny forests (each has 600 trees):", 10, 0, 1000, 1)
    create_input("num_employees", "Enter the number of employees:", 100, 0, 1000, 1)
    

if metrics["tree_age"] == 0:
    # Display a warning if the tree age is zero
    with col2:
        st.warning("Please enter a non-zero age for the tree.")
else:
    # Calculate the CO2 captured and employee emissions
    co2_captured = calculate_co2_captured(metrics["diameter"], metrics["height"], metrics["tree_age"])
    employee_emissions = calculate_employee_emissions(metrics["num_employees"], average_emissions_per_capita)
    proportion_captured = co2_captured / employee_emissions
    proportion_captured_percentage = proportion_captured * 100

    # Display data as a table
    table_data = {
        'Metrics': ['Total carbon emissions captured', 'Total carbon emissions by employees', 'Proportion of carbon emissions captured'],
        'Values': [format_large_number(co2_captured) + ' tCO2/year', format_large_number(employee_emissions) + ' tCO2e/year', "{:.2f}%".format(proportion_captured_percentage)]
    }
    # Create a bar chart to compare CO2 captured and employee emissions
    chart_data = {'Emissions captured': co2_captured, 'Emissions created': employee_emissions}

    with col2:
        table_data = st.dataframe(table_data, hide_index=True)
        st.bar_chart(chart_data)

# References

# Import README.md into a string
with open("README.md", "r") as file:
    explanation = file.read()

# Create an expander and display the README.md content
with st.expander("See details of the project and calculation methodology"):
    st.markdown(explanation)