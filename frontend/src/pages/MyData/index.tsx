import { useState, useEffect } from "react";
import { IndianRupee, Wallet } from "lucide-react";
import TopLoadingBar from "react-top-loading-bar";

import { HoldingsTab } from "./tabs/HoldingsTab";
import { IncomeTab } from "./tabs/IncomeTab";

type TabType = "holdings" | "transactions";

const MyData = () => {
  const [activeTab, setActiveTab] = useState<TabType>("holdings");
  const [progress, setProgress] = useState(0);

  const tabs = [
    {
      id: "holdings" as TabType,
      label: "Holdings & Investment Breakdown",
      icon: IndianRupee,
      activeColor: "text-purple-600",
      hoverColor: "hover:text-purple-500",
    },
    {
      id: "transactions" as TabType,
      label: "Transactions & Activity History",
      icon: Wallet,
      activeColor: "text-green-600",
      hoverColor: "hover:text-green-500",
    },
  ];

  useEffect(() => {
    const currentIndex = tabs.findIndex((tab) => tab.id === activeTab);
    const newProgress = ((currentIndex + 1) / tabs.length) * 100;
    setProgress(newProgress);
  }, [activeTab]);

  const renderTabContent = () => {
    switch (activeTab) {
      case "holdings":
        return <HoldingsTab />;
      case "transactions":
        return <IncomeTab />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
      <TopLoadingBar progress={progress} color="#4f46e5" height={4} />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Tabs */}
        <div className="flex space-x-1 rounded-xl bg-gray-200 dark:bg-gray-700 p-1 mb-8">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex justify-center items-center space-x-2 flex-1 py-2.5 px-3 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? `bg-white dark:bg-gray-800 ${tab.activeColor} shadow-sm`
                    : `text-gray-500 dark:text-gray-400 ${tab.hoverColor}`
                }`}
              >
                <Icon
                  className={`h-5 w-5 ${isActive ? tab.activeColor : ""}`}
                />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Tab Content */}
        {renderTabContent()}
      </div>
    </div>
  );
};

export default MyData;
