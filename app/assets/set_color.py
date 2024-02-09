import streamlit as st

# Set the background color
st.markdown(
    """
    <style>
        body {
            background-color: #f0f0f0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Set the text color
st.markdown(
    """
    <style>
        .css-1aumxhk {
            color: #3366ff; /* This class targets the primary text color */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display content
st.title("Streamlit App")
st.write("This is an example Streamlit application with custom colors.")
