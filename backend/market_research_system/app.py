import streamlit as st
from orchestrator import OrchestratorAgent
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    st.title("Market Research System")

    agent_type = st.selectbox("Select Agent Type", ["Sector", "Stock"])
    agent_name = st.text_input("Enter Agent Name")
    sector_stock_name = st.text_input("Enter Sector/Stock Name")
    brief_aim = st.text_area("Enter Brief Aim")

    if st.button("Run Analysis"):
        if not agent_name or not sector_stock_name or not brief_aim:
            st.error("Please fill in all the fields.")
            return

        orchestrator = OrchestratorAgent()

        with st.spinner("Running analysis..."):
            try:
                final_report = orchestrator.create_and_run_agents(
                    agent_type, agent_name, sector_stock_name, brief_aim
                )
                st.success("Analysis complete!")

                if agent_type.lower() == "stock":
                    st.subheader("Stock Analysis Report")
                    final_report = final_report.replace("{", "{{").replace("}", "}}") # Double escape
                    st.write(final_report)

                elif agent_type.lower() == "stock":
                    st.subheader("Stock Analysis Report")
                    st.write(final_report)  # Assuming final_report is a string or JSON

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()