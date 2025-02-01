import React, { useState, useEffect } from "react";
import {
  Target,
  DollarSign,
  SquareActivity,
  Receipt,
  Plus,
  Trash2,
  X,
  Edit2,
  LucideIcon,
  ChevronRight,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import StockHoldingsForm from "../forms/StockHoldingsForm";
import BondsForm from "../forms/BondsForm";

interface Goal {
  id: string;
  name: string;
  icon: LucideIcon;
  target: string;
  current: string;
}

// Stocks

interface StockHolding {
  stockName: string;
  tickerSymbol: string;
  numberOfShares: number;
  purchasePrice: number;
  purchaseDate: string;
  currentPrice?: number;
  dividendYield?: number;
  unrealizedGainsLosses?: number;
}

// Bonds

interface BondHolding {
  bondType: string;
  maturityDate: string;
  couponRate: number;
  principal: number;
  yieldToMaturity: number;
  interestEarned: number;
}

type IconType = keyof typeof availableIcons;

const availableIcons = {
  SquareActivity,
  Receipt,
} as const;

const iconDisplayNames: Record<keyof typeof availableIcons, string> = {
  SquareActivity: "Stock Holdings",
  Receipt: "Bonds",
};

export const HoldingsTab = () => {
  const [selectedAsset, setSelectedAsset] = useState<string | null>(null);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    icon: "SquareActivity" as IconType,
  });
  const [stockFormData, setStockFormData] = useState<StockHolding>({
    stockName: "TCS",
    tickerSymbol: "TCS.NS",
    numberOfShares: 50,
    purchasePrice: 3200,
    purchaseDate: "",
  });
  const [bondFormData, setBondFormData] = useState<BondHolding>({
    bondType: "Government",
    maturityDate: "2030-12-31",
    couponRate: 6.5,
    principal: 50000,
    yieldToMaturity: 0,
    interestEarned: 0,
  });
  const [portfolioData, setPortfolioData] = useState<{
    stocks: StockHolding[];
    bonds: BondHolding[];
  }>({ stocks: [], bonds: [] });

  const [selectedAssetType, setSelectedAssetType] = useState<
    "stock" | "bond" | null
  >(null);

  useEffect(() => {
    const fetchStocksData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/portfolio_data");
        if (!response.ok) {
          throw new Error(`Failed to fetch stocks data: ${response.status}`);
        }
        const data = await response.json();
        setPortfolioData(data);
      } catch (error) {
        console.error("Error fetching stocks data:", error);
      }
    };
    fetchStocksData();
  }, []);

  const handleAddGoal = () => {
    setIsEditing(false);
    setFormData({
      icon: "SquareActivity" as IconType,
    });
    setIsModalOpen(true);
  };

  const getAssetDetails = () => {
    if (!portfolioData || !selectedAsset || !selectedAssetType) {
      return undefined;
    }
    if (selectedAssetType === "stock") {
      return portfolioData?.stocks?.find(
        (stock) => stock.tickerSymbol === selectedAsset
      );
    } else if (selectedAssetType === "bond") {
      const [, bondType, ...bondMaturityParts] = selectedAsset.split("-");
      const bondMaturity = bondMaturityParts.join("-");
      return portfolioData?.bonds?.find(
        (bond) =>
          bond.bondType === bondType && bond.maturityDate === bondMaturity
      );
    }
    return undefined;
  };

  const getIconForGoal = (goalIcon: LucideIcon): IconType => {
    const iconEntry = Object.entries(availableIcons).find(
      ([_, icon]) => icon === goalIcon
    );
    return (iconEntry?.[0] as IconType) || "SquareActivity";
  };

  const handleEditGoal = () => {
    if (!selectedAsset) return;
    const goal = goals.find((g) => g.id === selectedAsset);
    if (!goal) return;

    setIsEditing(true);
    setFormData({
      icon: getIconForGoal(goal.icon),
    });
    setIsModalOpen(true);
  };

  const handleDeleteGoal = () => {
    if (!selectedAsset) return;
    setGoals(goals.filter((goal) => goal.id !== selectedAsset));
    setSelectedAsset(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsModalOpen(false);
    let apiUrl = "";
    let dataToSubmit = {};

    if (formData.icon === "SquareActivity") {
      apiUrl = "http://127.0.0.1:5000/stocks";
      dataToSubmit = stockFormData;
    } else if (formData.icon === "Receipt") {
      apiUrl = "http://127.0.0.1:5000/bonds";
      dataToSubmit = bondFormData;
    }

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataToSubmit),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`Failed to submit data : ${JSON.stringify(errorData)}`);
      }
      console.log("Data submitted successfully:", await response.json());
      if (formData.icon === "SquareActivity") {
        setStockFormData({
          stockName: "",
          tickerSymbol: "",
          numberOfShares: 0,
          purchasePrice: 0,
          purchaseDate: "",
        });
      } else if (formData.icon === "Receipt") {
        setBondFormData({
          bondType: "",
          maturityDate: "",
          couponRate: 0,
          principal: 0,
          yieldToMaturity: 0,
          interestEarned: 0,
        });
      }
    } catch (error) {
      console.error("Error submitting data:", error);
    }

    setFormData({ icon: "SquareActivity" as IconType });
  };

  const fillDemoData = () => {
    const demoGoals = [
      {
        name: "Stock Holdings",
        icon: "SquareActivity" as IconType,
        target: "5000000",
        current: "2000000",
      },
      {
        name: "Bonds",
        icon: "Receipt" as IconType,
        target: "1000000",
        current: "300000",
      },
    ];

    const randomGoal = demoGoals[Math.floor(Math.random() * demoGoals.length)];
    setFormData(randomGoal);
  };

  const renderFormContent = () => {
    switch (formData?.icon) {
      case "SquareActivity":
        return (
          <StockHoldingsForm
            formData={stockFormData}
            setFormData={setStockFormData}
          />
        );
      case "Receipt":
        return (
          <BondsForm formData={bondFormData} setFormData={setBondFormData} />
        );
      default:
        return null;
    }
  };

  const selectedAssetData = getAssetDetails();

  console.log(selectedAssetData);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-8"
    >
      {/* Header Section */}
      <div className="bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl p-8 text-white shadow-xl">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold">
              Holdings & Investment Breakdown
            </h2>
            <p className="mt-2 text-primary-100">
              Track and manage your assets and stocks
            </p>
          </div>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleAddGoal}
            className="inline-flex items-center px-6 py-3 bg-white text-primary-600 rounded-xl shadow-md hover:shadow-lg transition-all duration-200 font-medium"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add New Asset
          </motion.button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-1">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
            <div className="p-6 border-b border-gray-100 dark:border-gray-700">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                Your Assets
              </h3>
            </div>
            <div className="divide-y divide-gray-100 dark:divide-gray-700">
              <AnimatePresence>
                {!portfolioData.stocks?.length &&
                !portfolioData.bonds?.length ? (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="p-8 text-center"
                  >
                    <div className="w-16 h-16 bg-primary-50 dark:bg-primary-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Target className="h-8 w-8 text-primary-600 dark:text-primary-400" />
                    </div>
                    <p className="text-gray-500 dark:text-gray-400">
                      No assets added yet.
                    </p>
                    <p className="text-sm text-gray-400 dark:text-gray-500 mt-1">
                      Click "Add New Asset" to get started.
                    </p>
                  </motion.div>
                ) : (
                  <>
                    {portfolioData?.stocks?.map((stock) => (
                      <motion.button
                        key={stock.tickerSymbol}
                        layout
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        onClick={() => {
                          setSelectedAsset(stock.tickerSymbol);
                          setSelectedAssetType("stock");
                        }}
                        className={`w-full flex items-center p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors ${
                          selectedAsset === stock.tickerSymbol
                            ? "bg-primary-50 dark:bg-primary-900/20"
                            : ""
                        }`}
                      >
                        <div className="p-3 rounded-xl bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
                          <SquareActivity className="h-6 w-6" />
                        </div>
                        <div className="ml-4 flex-1 text-left">
                          <h3 className="font-medium text-gray-900 dark:text-white">
                            {stock.stockName} ({stock.tickerSymbol})
                          </h3>
                          <p className="text-sm text-gray-500 dark:text-gray-400">
                            ${stock?.currentPrice}
                          </p>
                        </div>
                        <ChevronRight
                          className={`h-5 w-5 text-gray-400 transition-transform ${
                            selectedAsset === stock.tickerSymbol
                              ? "rotate-90"
                              : ""
                          }`}
                        />
                      </motion.button>
                    ))}

                    {portfolioData?.bonds?.map((bond) => (
                      <motion.button
                        key={`${bond.bondType}-${bond.maturityDate}`}
                        layout
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        onClick={() => {
                          setSelectedAsset(
                            `bond-${bond?.bondType}-${bond?.maturityDate}`
                          );
                          setSelectedAssetType("bond");
                        }}
                        className={`w-full flex items-center p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors ${
                          selectedAsset ===
                          `bond-${bond.bondType}-${bond.maturityDate}`
                            ? "bg-primary-50 dark:bg-primary-900/20"
                            : ""
                        }`}
                      >
                        <div className="p-3 rounded-xl bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
                          <Receipt className="h-6 w-6" />
                        </div>
                        <div className="ml-4 flex-1 text-left">
                          <h3 className="font-medium text-gray-900 dark:text-white">
                            {bond.bondType} Bond
                          </h3>
                          <p className="text-sm text-gray-500 dark:text-gray-400">
                            {bond.couponRate}% Interest
                          </p>
                        </div>
                        <ChevronRight
                          className={`h-5 w-5 text-gray-400 transition-transform ${
                            selectedAsset ===
                            `bond-${bond.bondType}-${bond.maturityDate}`
                              ? "rotate-90"
                              : ""
                          }`}
                        />
                      </motion.button>
                    ))}
                  </>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>

        <AnimatePresence mode="wait">
          {selectedAsset && selectedAssetData && (
            <motion.div
              key={selectedAsset}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="lg:col-span-2"
            >
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl overflow-hidden">
                <div className="p-6 border-b border-gray-100 dark:border-gray-700 flex items-center justify-between">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    Asset Details
                  </h3>
                  <div className="flex space-x-2">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleEditGoal}
                      className="inline-flex items-center px-4 py-2 bg-primary-50 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-xl hover:bg-primary-100 dark:hover:bg-primary-900/50 transition-colors"
                    >
                      <Edit2 className="h-4 w-4 mr-2" />
                      Edit
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={handleDeleteGoal}
                      className="inline-flex items-center px-4 py-2 bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-xl hover:bg-red-100 dark:hover:bg-red-900/50 transition-colors"
                    >
                      <Trash2 className="h-4 w-4 mr-2" />
                      Delete
                    </motion.button>
                  </div>
                </div>

                <div className="p-6 space-y-8">
                  {selectedAssetType === "stock" && selectedAssetData && (
                    <>
                      {/* Stock Stats */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-900/30 rounded-xl p-6">
                          <p className="text-sm font-medium text-green-600 dark:text-green-400">
                            Current Value
                          </p>
                          <div className="mt-2 flex items-center">
                            <DollarSign className="h-5 w-5 text-green-500" />
                            <span className="text-2xl font-bold text-gray-900 dark:text-white ml-1">
                              {selectedAssetData?.currentPrice *
                                selectedAssetData?.numberOfShares}
                            </span>
                          </div>
                        </div>

                        <div className="bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/20 dark:to-primary-900/30 rounded-xl p-6">
                          <p className="text-sm font-medium text-primary-600 dark:text-primary-400">
                            Purchase Value
                          </p>
                          <div className="mt-2 flex items-center">
                            <Target className="h-5 w-5 text-primary-500" />
                            <span className="text-2xl font-bold text-gray-900 dark:text-white ml-1">
                              {selectedAssetData?.purchasePrice *
                                selectedAssetData?.numberOfShares}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="space-y-4">
                        <h4 className="text-lg font-medium text-gray-900 dark:text-white">
                          Smart Recommendations
                        </h4>
                        <div className="grid gap-4">
                          {[
                            "Increase the number of shares to lower your average purchase price.",
                            "Consider selling and booking profits.",
                            "Review and rebalance portfolio quarterly",
                          ].map((recommendation, index) => (
                            <motion.div
                              key={index}
                              initial={{ opacity: 0, x: -20 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: index * 0.1 }}
                              className="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl flex items-start space-x-3"
                            >
                              <div className="flex-shrink-0">
                                <div className="w-2 h-2 mt-2 rounded-full bg-primary-500"></div>
                              </div>
                              <p className="text-gray-600 dark:text-gray-300">
                                {recommendation}
                              </p>
                            </motion.div>
                          ))}
                        </div>
                      </div>
                    </>
                  )}
                  {selectedAssetType === "bond" && selectedAssetData && (
                    <>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-900/30 rounded-xl p-6">
                          <p className="text-sm font-medium text-green-600 dark:text-green-400">
                            Principal
                          </p>
                          <div className="mt-2 flex items-center">
                            <DollarSign className="h-5 w-5 text-green-500" />
                            <span className="text-2xl font-bold text-gray-900 dark:text-white ml-1">
                              {selectedAssetData?.principal}
                            </span>
                          </div>
                        </div>
                        <div className="bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/20 dark:to-primary-900/30 rounded-xl p-6">
                          <p className="text-sm font-medium text-primary-600 dark:text-primary-400">
                            Interest Earned
                          </p>
                          <div className="mt-2 flex items-center">
                            <Target className="h-5 w-5 text-primary-500" />
                            <span className="text-2xl font-bold text-gray-900 dark:text-white ml-1">
                              {selectedAssetData?.interestEarned}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="space-y-4">
                        <h4 className="text-lg font-medium text-gray-900 dark:text-white">
                          Smart Recommendations
                        </h4>
                        <div className="grid gap-4">
                          {[
                            `Reinvest when the bond matures.`,
                            "Compare similar bonds for better returns.",
                            "Review and rebalance portfolio annually.",
                          ].map((recommendation, index) => (
                            <motion.div
                              key={index}
                              initial={{ opacity: 0, x: -20 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: index * 0.1 }}
                              className="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-xl flex items-start space-x-3"
                            >
                              <div className="flex-shrink-0">
                                <div className="w-2 h-2 mt-2 rounded-full bg-primary-500"></div>
                              </div>
                              <p className="text-gray-600 dark:text-gray-300">
                                {recommendation}
                              </p>
                            </motion.div>
                          ))}
                        </div>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <AnimatePresence>
        {isModalOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white dark:bg-gray-800 rounded-2xl max-w-2xl w-full shadow-2xl"
            >
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white">
                      {isEditing ? "Edit Financial Asset" : "Create New Asset"}
                    </h3>
                    <p className="mt-2 text-gray-500 dark:text-gray-400">
                      {isEditing
                        ? "Update your financial asset details below"
                        : "Create your financial asset below"}
                    </p>
                  </div>
                  <motion.button
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => setIsModalOpen(false)}
                    className="text-gray-400 hover:text-gray-500 transition-colors"
                  >
                    <X className="h-6 w-6" />
                  </motion.button>
                </div>
              </div>

              <form onSubmit={handleSubmit} className="p-6 space-y-6">
                <div className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Choose an Investment option
                    </label>
                    <div className="grid grid-cols-2 gap-4">
                      {Object.entries(availableIcons).map(([name, Icon]) => (
                        <motion.button
                          key={name}
                          type="button"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                          onClick={() =>
                            setFormData({ ...formData, icon: name as IconType })
                          }
                          className={`p-4 rounded-xl flex flex-col items-center gap-2 transition-all ${
                            formData.icon === name
                              ? "bg-primary-100 dark:bg-primary-900/30 ring-2 ring-primary-500 dark:ring-primary-400"
                              : "bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600"
                          }`}
                        >
                          <Icon
                            className={`h-6 w-6 ${
                              formData.icon === name
                                ? "text-primary-600 dark:text-primary-400"
                                : "text-gray-500 dark:text-gray-400"
                            }`}
                          />

                          <span className="text-xs font-medium text-gray-600 dark:text-gray-300">
                            {
                              iconDisplayNames[
                                name as keyof typeof availableIcons
                              ]
                            }
                          </span>
                        </motion.button>
                      ))}
                    </div>
                  </div>

                  {renderFormContent()}
                </div>

                {/* Action Buttons */}
                <div className="flex justify-end space-x-4 mt-8">
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    type="button"
                    onClick={fillDemoData}
                    className="px-4 py-2 rounded-xl bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-sm font-medium"
                  >
                    Demo Data
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    type="button"
                    onClick={() => setIsModalOpen(false)}
                    className="px-6 py-3 rounded-xl border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                  >
                    Cancel
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    type="submit"
                    className="px-6 py-3 rounded-xl bg-gradient-to-r from-primary-500 to-primary-600 text-white hover:from-primary-600 hover:to-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-all"
                  >
                    {isEditing ? "Save Changes" : "Create Asset"}
                  </motion.button>
                </div>
              </form>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};
