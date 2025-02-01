import os
from dotenv import load_dotenv
from orchestrator import OrchestratorAgent

load_dotenv()

def main():
    """
    Main function to run the market research system.
    """
    agent_type = input("Enter agent type (Sector or Stock): ")
    agent_name = input("Enter agent name (e.g., GreenEnergyAnalyst): ")
    sector_stock_name = input("Enter sector/stock name (e.g., Green Energy): ")
    brief_aim = input("Enter brief aim: ")

    orchestrator = OrchestratorAgent()
    final_report = orchestrator.create_and_run_agents(
        agent_type, agent_name, sector_stock_name, brief_aim
    )
    print(final_report)

if __name__ == "__main__":
    main()