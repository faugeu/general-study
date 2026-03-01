import streamlit as st

# Page configuration
st.set_page_config(page_title="My Streamlit App", page_icon="🚀", layout="wide")

# Title
st.title("🚀 My First Streamlit App")

# Sidebar
st.sidebar.header("Settings")
name = st.sidebar.text_input("Enter your name")

# Main content
st.header("Welcome")

if name:
    st.success(f"Hello, {name}!")
else:
    st.info("Please enter your name in the sidebar.")

# Example widgets
st.subheader("Example Widgets")

age = st.slider("Select your age", 0, 100, 25)
st.write("Your age:", age)

if st.button("Click me"):
    st.write("Button clicked!")

# Example table
st.subheader("Sample Data")

data = {"Name": ["Alice", "Bob", "Charlie"], "Score": [85, 92, 78]}

st.table(data)

# Footer
st.divider()
st.caption("Built with Streamlit")
