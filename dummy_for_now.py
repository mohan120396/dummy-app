import streamlit as st

def main():
    st.set_page_config(page_title="My First Streamlit App", layout="centered")

    st.title("Hello, Streamlit Cloud! 👋")

    st.write(
        """
        This is a super simple Streamlit app. 
        You can use it as a starting point for your own projects.
        """
    )

    st.header("What can you do with Streamlit?")
    st.markdown(
        """
        Streamlit lets you turn data scripts into shareable web apps in minutes.
        Some common uses include:
        *   **Data Dashboards:** Displaying key metrics and trends.
        *   **Machine Learning Apps:** Showcasing model predictions and interactions.
        *   **Data Exploration Tools:** Allowing users to filter and visualize data.
        *   **Interactive Demos:** Presenting concepts and ideas.
        """
    )

    name = st.text_input("What's your name?", "Guest")
    
    if st.button("Say Hello"):
        st.success(f"Hello, {name}! Welcome to Streamlit!")

    st.subheader("Random Number Generator")
    import random
    if st.button("Generate a random number"):
        st.write(f"Your random number is: **{random.randint(1, 100)}**")

    st.sidebar.header("About This App")
    st.sidebar.info(
        "This app was created using Streamlit. It's a great tool for building "
        "interactive data applications with Python."
    )
    st.sidebar.write("---")
    st.sidebar.write("Developed by Your Name/Company")

if __name__ == "__main__":
    main()
