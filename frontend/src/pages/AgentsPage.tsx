import React, { useState, useEffect } from "react";
import { Plus, Bot, Trash2, X, FileText, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface Agent {
  id: string;
  name: string;
  sector: string;
  scope: "sector" | "stock";
  stockName?: string;
  aim: string;
  created: string;
  status: "active" | "inactive";
  hasReport?: boolean;
  updateFrequency?: "daily" | "weekly";
}

const analysisScopes = [
  { value: "sector", label: "Specific Sector" },
  { value: "stock", label: "Individual Stock" },
];

const demoTemplates = [
  {
    name: "Tech Trend Analyzer",
    sector: "Technology",
    scope: "sector",
    aim: "Monitor emerging trends in cloud computing and AI adoption across major tech companies",
  },
  {
    name: "Apple Stock Analyzer",
    sector: "Technology",
    scope: "stock",
    stockName: "Apple Inc.",
    aim: "Track Apple stock performance and analyze impact of product launches",
  },
  {
    name: "Healthcare Innovation Monitor",
    sector: "Healthcare",
    scope: "sector",
    aim: "Analyze breakthrough medical technologies and their market impact",
  },
  {
    name: "Electric Vehicle Market Watch",
    sector: "Automotive",
    scope: "sector",
    aim: "Track market adoption of electric vehicles and assess the impact on traditional automotive companies",
  },
  {
    name: "Green Energy Investment Insights",
    sector: "Energy",
    scope: "sector",
    aim: "Analyze market trends in green energy technologies, with a focus on solar and wind power companies",
  },
  {
    name: "Tesla Stock Performance Tracker",
    sector: "Automotive",
    scope: "stock",
    stockName: "Tesla Inc.",
    aim: "Analyze Tesla's stock performance, factoring in production milestones, EV sales, and regulatory changes",
  },
  {
    name: "Financial Sector Health Monitor",
    sector: "Finance",
    scope: "sector",
    aim: "Monitor financial stability and investment opportunities within banks, fintech, and investment firms",
  },
  {
    name: "Pharmaceutical Stock Tracker",
    sector: "Healthcare",
    scope: "stock",
    stockName: "Pfizer Inc.",
    aim: "Track stock performance of pharmaceutical companies, focusing on drug pipeline developments and regulatory approvals",
  },
  {
    name: "Global Supply Chain Trends",
    sector: "Logistics",
    scope: "sector",
    aim: "Monitor global supply chain disruptions, with insights on key logistics players and market shifts",
  },
  {
    name: "Real Estate Market Sentiment Analysis",
    sector: "Real Estate",
    scope: "sector",
    aim: "Analyze trends in residential and commercial real estate markets based on macroeconomic indicators",
  },
  {
    name: "Financial Technology Disruptions",
    sector: "Finance",
    scope: "sector",
    aim: "Explore emerging fintech innovations and their potential to disrupt traditional banking and financial services",
  },
  {
    name: "Luxury Goods Market Watch",
    sector: "Retail",
    scope: "sector",
    aim: "Analyze trends in luxury goods consumption, focusing on market conditions and consumer behavior in high-end markets",
  },
  {
    name: "Cybersecurity Stock Analyzer",
    sector: "Technology",
    scope: "stock",
    stockName: "Palo Alto Networks",
    aim: "Track stock performance of cybersecurity companies based on global threats and regulatory changes",
  },
  {
    name: "AI-Powered Healthcare Trends",
    sector: "Healthcare",
    scope: "sector",
    aim: "Monitor the adoption of AI technologies in healthcare, with an emphasis on diagnostics and treatment advancements",
  },
  {
    name: "Blockchain and Cryptocurrency Tracker",
    sector: "Finance",
    scope: "sector",
    aim: "Analyze the impact of blockchain technology and cryptocurrency on traditional financial systems and investment trends",
  },
  {
    name: "Global Oil Price Watcher",
    sector: "Energy",
    scope: "sector",
    aim: "Track global oil price trends and analyze their impact on energy companies, supply chains, and the economy",
  },
];

const STORAGE_KEY = "market-analysis-agents";

const Modal = ({ isOpen, onClose, showTemplates, children }) => {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className={`bg-white rounded-lg w-full ${
              showTemplates ? "max-w-4xl" : "max-w-md"
            } relative`}
          >
            <button
              onClick={onClose}
              className="absolute right-4 top-4 text-gray-500 hover:text-gray-700"
            >
              <X size={20} />
            </button>
            {children}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

const AgentsPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [formData, setFormData] = useState({
    name: "",
    sector: "",
    scope: "",
    stockName: "",
    aim: "",
  });
  const [showTemplates, setShowTemplates] = useState(false);
  const [generatingReportFor, setGeneratingReportFor] = useState<string | null>(
    null
  );

  // Load agents from localStorage on component mount
  useEffect(() => {
    const savedAgents = localStorage.getItem(STORAGE_KEY);
    if (savedAgents) {
      try {
        setAgents(JSON.parse(savedAgents));
      } catch (error) {
        console.error("Error loading agents from localStorage:", error);
      }
    }
  }, []);

  // Save agents to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(agents));
  }, [agents]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const newAgent: Agent = {
      id: Date.now().toString(),
      ...formData,
      created: new Date().toISOString(),
      status: "active",
    };
    setAgents((prev) => [...prev, newAgent]);
    setFormData({ name: "", sector: "", scope: "", stockName: "", aim: "" });
    setIsModalOpen(false);
    setShowTemplates(false);
  };

  const handleDeleteAgent = (id: string) => {
    setAgents((prev) => prev.filter((agent) => agent.id !== id));
  };

  const loadTemplate = (template) => {
    setFormData({
      name: template.name,
      sector: template.sector,
      scope: template.scope,
      stockName: template.stockName || "",
      aim: template.aim,
    });
    setShowTemplates(false);
  };

  const handleAgentClick = (agent: Agent) => {
    // This would typically navigate to a detailed view
    console.log("Navigate to agent details:", agent);
    alert("Navigating to agent details page... (Implementation pending)");
  };

  const handleCreateReport = async (e: React.MouseEvent, agentId: string) => {
    e.stopPropagation();
    setGeneratingReportFor(agentId);

    // Simulate report generation
    try {
      await new Promise((resolve) => setTimeout(resolve, 2000));
      setAgents((prev) =>
        prev.map((agent) =>
          agent.id === agentId ? { ...agent, hasReport: true } : agent
        )
      );
    } finally {
      setGeneratingReportFor(null);
    }
  };

  const handleOpenReport = (e: React.MouseEvent, agent: Agent) => {
    e.stopPropagation();
    // This would typically open the report in a new view
    alert(`Opening report for ${agent.name}...`);
  };

  const handleUpdateFrequencyChange = (
    agentId: string,
    frequency: "daily" | "weekly"
  ) => {
    setAgents((prev) =>
      prev.map((agent) =>
        agent.id === agentId ? { ...agent, updateFrequency: frequency } : agent
      )
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex justify-between items-center mb-6"
        >
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Market Analysis Agents
            </h1>
            <p className="text-gray-600">
              Create and manage your AI market analysis agents
            </p>
          </div>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => {
              setIsModalOpen(true);
              setShowTemplates(false);
              setFormData({
                name: "",
                sector: "",
                scope: "",
                stockName: "",
                aim: "",
              });
            }}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 flex items-center gap-2"
          >
            <Plus size={20} />
            New Agent
          </motion.button>
        </motion.div>

        <motion.div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <AnimatePresence>
            {agents.map((agent) => (
              <motion.div
                key={agent.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                whileHover={{ y: -5 }}
                className="bg-white rounded-lg shadow-md p-6 cursor-pointer group"
                onClick={() => handleAgentClick(agent)}
              >
                <div className="flex justify-between items-start">
                  <div className="flex items-center gap-2">
                    <Bot className="text-primary-600" size={24} />
                    <h3 className="text-lg font-semibold text-gray-900">
                      {agent.name}
                    </h3>
                  </div>
                  <motion.button
                    whileHover={{ scale: 1.1, color: "#EF4444" }}
                    whileTap={{ scale: 0.9 }}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteAgent(agent.id);
                    }}
                    className="text-gray-400"
                  >
                    <Trash2 size={20} />
                  </motion.button>
                </div>
                <div className="mt-4">
                  <p className="text-sm text-gray-600 font-medium">Sector</p>
                  <p className="text-gray-900">{agent.sector}</p>
                </div>
                <div className="mt-4">
                  <p className="text-sm text-gray-600 font-medium">
                    Analysis Scope
                  </p>
                  <p className="text-gray-900">
                    {agent.scope.charAt(0).toUpperCase() + agent.scope.slice(1)}
                    {agent.stockName && ` - ${agent.stockName}`}
                  </p>
                </div>
                <div className="mt-4">
                  <p className="text-sm text-gray-600 font-medium">Aim</p>
                  <p className="text-gray-900">{agent.aim}</p>
                </div>
                <div className="mt-4 flex items-center justify-between">
                  <span className="text-sm text-gray-500">
                    Created {new Date(agent.created).toLocaleDateString()}
                  </span>
                  <div className="flex items-center gap-2">
                    <motion.span
                      whileHover={{ scale: 1.05 }}
                      className="px-2 py-1 bg-green-100 text-green-800 text-sm rounded-full"
                    >
                      Active
                    </motion.span>
                  </div>
                </div>

                <div className="mt-4 flex justify-center w-full relative">
                  <div className="inline-flex relative bg-gray-100 p-1 rounded-full">
                    <motion.div
                      className="absolute inset-0 h-full"
                      initial={false}
                      animate={{
                        x: agent.updateFrequency === "weekly" ? "100%" : "0%",
                        scale: 0.95,
                      }}
                      transition={{
                        type: "spring",
                        bounce: 0.2,
                        duration: 0.6,
                      }}
                    >
                      <div className="h-full bg-white rounded-full shadow-sm" />
                    </motion.div>
                    <motion.button
                      className={`relative px-4 py-1 rounded-full text-sm font-medium transition-colors ${
                        agent.updateFrequency === "daily"
                          ? "text-blue-600"
                          : "text-gray-500"
                      }`}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleUpdateFrequencyChange(agent.id, "daily");
                      }}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      Daily Update
                    </motion.button>
                    <motion.button
                      className={`relative px-4 py-1 rounded-full text-sm font-medium transition-colors ${
                        agent.updateFrequency === "weekly"
                          ? "text-blue-600"
                          : "text-gray-500"
                      }`}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleUpdateFrequencyChange(agent.id, "weekly");
                      }}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      Weekly Update
                    </motion.button>
                  </div>
                </div>

                {/* Report Actions */}
                <div className="mt-4 flex gap-2">
                  {agent.hasReport ? (
                    <button
                      onClick={(e) => handleOpenReport(e, agent)}
                      className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-green-50 text-green-700 rounded-md hover:bg-green-100 transition-colors"
                    >
                      <FileText size={16} />
                      Open Report
                    </button>
                  ) : (
                    <button
                      onClick={(e) => handleCreateReport(e, agent.id)}
                      disabled={generatingReportFor === agent.id}
                      className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-primary-50 text-primary-700 rounded-md hover:bg-primary-100 transition-colors disabled:bg-gray-50 disabled:text-gray-500"
                    >
                      {generatingReportFor === agent.id ? (
                        <>
                          <Loader2 size={16} className="animate-spin" />
                          Generating...
                        </>
                      ) : (
                        <>
                          <FileText size={16} />
                          Create Report
                        </>
                      )}
                    </button>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </motion.div>

        <Modal
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setShowTemplates(false);
          }}
          showTemplates={showTemplates}
        >
          {showTemplates ? (
            <div className="p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                Select Template
              </h2>
              <div className="grid grid-cols-4 gap-3">
                {demoTemplates.map((template, index) => (
                  <motion.button
                    key={index}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => loadTemplate(template)}
                    className="w-full p-4 text-left border rounded-lg hover:bg-gray-50"
                  >
                    <h3 className="font-medium text-gray-900">
                      {template.name}
                    </h3>
                    <p className="text-sm text-gray-500 mt-1">
                      {template.sector}
                    </p>
                  </motion.button>
                ))}
                <button
                  onClick={() => setShowTemplates(false)}
                  className="w-full p-3 text-center text-gray-600 hover:text-gray-900 col-span-4 border border-gray-200 rounded-lg hover:bg-gray-50 mt-3"
                >
                  Start from scratch instead
                </button>
              </div>
            </div>
          ) : (
            <div className="p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">
                Create New Agent
              </h2>
              <button
                onClick={() => setShowTemplates(true)}
                className="w-full p-3 mb-4 text-center text-primary-600 hover:text-primary-700 border border-primary-200 rounded-lg hover:bg-primary-50"
              >
                Load from template
              </button>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Agent Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="e.g., Tech Sector Analyzer"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Analysis Scope
                  </label>
                  <select
                    name="scope"
                    value={formData.scope}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    required
                  >
                    <option value="">Select analysis scope</option>
                    {analysisScopes.map((scope) => (
                      <option key={scope.value} value={scope.value}>
                        {scope.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Market Sector
                  </label>
                  <input
                    type="text"
                    name="sector"
                    value={formData.sector}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="e.g., Technology, Healthcare, Financial Services"
                    required
                  />
                </div>

                {formData.scope === "stock" && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Stock Name
                    </label>
                    <input
                      type="text"
                      name="stockName"
                      value={formData.stockName}
                      onChange={handleInputChange}
                      className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                      placeholder="e.g., Apple Inc., Microsoft Corporation"
                      required={formData.scope === "stock"}
                    />
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Analysis Aim
                  </label>
                  <textarea
                    name="aim"
                    value={formData.aim}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    rows={3}
                    placeholder="Describe what the agent should analyze..."
                    required
                  />
                </div>

                <div className="flex gap-3 mt-6">
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    type="button"
                    onClick={() => setIsModalOpen(false)}
                    className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                  >
                    Cancel
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    type="submit"
                    className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
                  >
                    Create Agent
                  </motion.button>
                </div>
              </form>
            </div>
          )}
        </Modal>
      </div>
    </div>
  );
};

export default AgentsPage;
