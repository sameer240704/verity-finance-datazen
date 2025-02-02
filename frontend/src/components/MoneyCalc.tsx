import React, { useState, useEffect } from "react";
import axios from "axios";
import { TrendingUp, Plus, X } from "lucide-react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import DemoReport from "../components/DemoReport";

interface IncomeStatement {
  EBITDA: number;
  currency: string;
  date: string;
  day: number;
  earnings_per_share: number;
  effective_task_rate_percent: number;
  month: number;
  net_income: number;
  net_profit_margin: number;
  operating_expense: number;
  revenue: number;
  year: number;
}

interface CompanyInfo {
  income_statement: IncomeStatement[];
  period: string;
  symbol: string;
  type: string;
}

interface StockData {
  currentPrice: number;
  dividendYield: number;
  numberOfShares: number;
  purchaseDate: string;
  purchasePrice: number;
  stockName: string;
  tickerSymbol: string;
  unrealizedGainsLosses: number;
  weightageInPortfolio: number;
}

interface Asset {
  id: number;
  name: string;
  currentValue: number;
  expectedReturn: number;
  quantity: number;
}

interface CalculatorProps {
  title: string;
  children: React.ReactNode;
}

const CalculatorCard: React.FC<CalculatorProps> = ({ title, children }) => (
  <div className="bg-gradient-to-br from-white to-gray-50 dark:from-gray-800 dark:to-gray-900 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 p-6 mb-6">
    <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white flex items-center">
      {title}
    </h3>
    {children}
  </div>
);

const formatRupees = (value: number) => {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
};

const Modal = ({
  isOpen,
  onClose,
  children,
}: {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-md w-full p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-500 dark:hover:text-gray-300"
        >
          <X className="h-5 w-5" />
        </button>
        {children}
      </div>
    </div>
  );
};

const MoneyCalc = () => {
  const [timeframe, setTimeframe] = useState<number>(1);
  const [isGeneratingReport, setIsGeneratingReport] = useState<boolean>(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [imagePaths, setImagePaths] = useState<string[]>([]);
  const [newAsset, setNewAsset] = useState<Partial<Asset>>({
    name: "",
    currentValue: 0,
    expectedReturn: 0,
    quantity: 0,
  });

  useEffect(() => {
    const fetchStockData = async () => {
      setLoading(true);
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/portfolio_data"
        );
        console.log(response.data);

        const stocksData: StockData[] = response.data.stocks;

        const mappedAssets = stocksData.map((stock, index) => ({
          id: index + 1,
          name: stock.stockName,
          currentValue: stock.currentPrice,
          expectedReturn: 10,
          quantity: stock.numberOfShares,
        }));

        setAssets(mappedAssets);
        setError(null);
      } catch (err: any) {
        setError(err.message || "Failed to load stock data");
      } finally {
        setLoading(false);
      }
    };

    const fetchProphetImages = async () => {
      setIsGeneratingReport(true);
      try {
        const response = await axios.post<{ prophet_images: string[] }>(
          "http://127.0.0.1:5000/prophet_stock",
          { years: timeframe }
        );
        setImagePaths(response.data.prophet_images);
        console.log(response.data.prophet_images);
      } catch (error) {
        console.error("Error fetching prophet stock data:", error);
      } finally {
        setIsGeneratingReport(false);
      }
    };

    fetchStockData();
    fetchProphetImages();
  }, [timeframe]);

  const calculateFutureValue = (
    currentValue: number,
    expectedReturn: number,
    years: number
  ) => {
    const annualRate = expectedReturn / 100;
    return currentValue * Math.pow(1 + annualRate, years);
  };

  const generateGraphData = () => {
    const data = [];
    for (let year = 0; year <= timeframe; year++) {
      const yearData: any = { year };
      let totalValue = 0;

      assets.forEach((asset) => {
        const futureValue = calculateFutureValue(
          asset.currentValue * asset.quantity,
          asset.expectedReturn,
          year
        );
        yearData[asset.name] = futureValue;
        totalValue += futureValue;
      });

      yearData.Total = totalValue;
      data.push(yearData);
    }
    return data;
  };

  const addAsset = () => {
    if (
      newAsset.name &&
      newAsset.currentValue &&
      newAsset.expectedReturn &&
      newAsset.quantity
    ) {
      setAssets([
        ...assets,
        {
          id: assets.length + 1,
          name: newAsset.name,
          currentValue: newAsset.currentValue,
          expectedReturn: newAsset.expectedReturn,
          quantity: newAsset.quantity,
        },
      ]);
      setNewAsset({
        name: "",
        currentValue: 0,
        expectedReturn: 0,
        quantity: 0,
      });
    }
  };

  const colors = ["#6366f1", "#ec4899", "#f59e0b", "#10b981", "#8b5cf6"];

  if (loading) {
    return (
      <div className="text-center text-gray-700 dark:text-gray-300">
        Loading asset data...
      </div>
    );
  }

  if (error) {
    return <div className="text-center text-red-500">Error: {error}</div>;
  }

  const sliderSettings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: false,
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h2 className="text-2xl font-bold mb-6 text-gray-900 dark:text-white flex items-center">
        <TrendingUp className="h-6 w-6 mr-2 text-indigo-500" />
        Asset Growth Calculator
      </h2>

      {/* Time Control and Add Asset Button */}
      <div className="bg-gradient-to-br from-white to-gray-50 dark:from-gray-800 dark:to-gray-900 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 p-6 mb-6">
        <div className="flex flex-col md:flex-row md:items-center gap-4">
          <div className="flex-grow">
            <div className="flex justify-between items-center mb-4">
              <label className="text-base font-medium text-gray-700 dark:text-gray-300">
                Projection Timeframe
              </label>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setTimeframe(Math.max(0, timeframe - 1))}
                  className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-500 dark:text-gray-400"
                >
                  <span className="font-bold">-</span>
                </button>
                <span className="text-sm font-bold bg-indigo-100 dark:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400 px-4 py-1.5 rounded-full min-w-[80px] text-center">
                  {timeframe} year{timeframe !== 1 ? "s" : ""}
                </span>
                <button
                  onClick={() => setTimeframe(Math.min(5, timeframe + 1))}
                  className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-500 dark:text-gray-400"
                >
                  <span className="font-bold">+</span>
                </button>
              </div>
            </div>
            <div className="relative">
              <div className="absolute -top-2 left-0 w-full">
                <div className="relative">
                  {[0, 25, 50, 75, 100].map((mark) => (
                    <div
                      key={mark}
                      className="absolute top-0 w-px h-2 bg-gray-300 dark:bg-gray-600"
                      style={{ left: `${mark}%` }}
                    />
                  ))}
                </div>
              </div>
              <input
                type="range"
                min="0"
                max="5"
                value={timeframe}
                onChange={(e) => setTimeframe(Number(e.target.value))}
                className="w-full h-2 appearance-none cursor-pointer bg-transparent focus:outline-none"
                style={{
                  WebkitAppearance: "none",
                  background: `linear-gradient(to right, rgb(79, 70, 229) ${
                    (timeframe / 5) * 100
                  }%, rgb(229, 231, 235) ${(timeframe / 5) * 100}%)`,
                  borderRadius: "9999px",
                }}
              />
              <style>{`
                input[type='range']::-webkit-slider-thumb {
                  -webkit-appearance: none;
                  appearance: none;
                  width: 20px;
                  height: 20px;
                  background: #fff;
                  border: 2px solid rgb(79, 70, 229);
                  border-radius: 50%;
                  cursor: pointer;
                  transition: all 0.15s ease-in-out;
                  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                }
                input[type='range']::-webkit-slider-thumb:hover {
                  transform: scale(1.1);
                  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
                }
                input[type='range']::-webkit-slider-thumb:active {
                  transform: scale(0.9);
                  background: rgb(79, 70, 229);
                }
                input[type='range']::-moz-range-thumb {
                  width: 20px;
                  height: 20px;
                  background: #fff;
                  border: 2px solid rgb(79, 70, 229);
                  border-radius: 50%;
                  cursor: pointer;
                  transition: all 0.15s ease-in-out;
                  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                }
                input[type='range']::-moz-range-thumb:hover {
                  transform: scale(1.1);
                  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
                }
                input[type='range']::-moz-range-thumb:active {
                  transform: scale(0.9);
                  background: rgb(79, 70, 229);
                }
              `}</style>
            </div>
            <div className="flex justify-between text-xs font-medium text-gray-500 dark:text-gray-400 mt-2">
              {[0, 1, 2, 3, 4, 5].map((year) => (
                <button
                  key={year}
                  onClick={() => setTimeframe(year)}
                  className={`px-2 py-1 rounded transition-colors ${
                    timeframe === year
                      ? "text-indigo-600 dark:text-indigo-400 font-semibold"
                      : "hover:text-gray-700 dark:hover:text-gray-300"
                  }`}
                >
                  {year} {year === 1 ? "year" : "years"}
                </button>
              ))}
            </div>
          </div>
          <button
            onClick={() => setIsModalOpen(true)}
            className="flex items-center justify-center bg-indigo-600 text-white py-2.5 px-4 rounded-lg hover:bg-indigo-700 transition-colors font-medium min-w-[160px] hover:shadow-lg active:transform active:scale-95"
          >
            <Plus className="h-5 w-5 mr-2" />
            Add Asset
          </button>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* Assets Table */}
        <CalculatorCard title="Your Assets">
          <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead className="bg-gray-50 dark:bg-gray-800">
                <tr>
                  <th className="px-4 py-3.5 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Asset
                  </th>
                  <th className="px-4 py-3.5 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Quantity
                  </th>
                  <th className="px-4 py-3.5 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Current Value (₹)
                  </th>
                  <th className="px-4 py-3.5 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Expected Return (%)
                  </th>
                  <th className="px-4 py-3.5 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Future Value ({timeframe} year{timeframe !== 1 ? "s" : ""})
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                {assets.map((asset, index) => {
                  const futureValue = calculateFutureValue(
                    asset.currentValue * asset.quantity,
                    asset.expectedReturn,
                    timeframe
                  );
                  return (
                    <tr
                      key={asset.id}
                      className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                    >
                      <td className="px-4 py-3 text-sm font-medium text-gray-900 dark:text-white">
                        {asset.name}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                        {asset.quantity.toLocaleString()}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                        {formatRupees(asset.currentValue * asset.quantity)}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                        {asset.expectedReturn}%
                      </td>
                      <td className="px-4 py-3 text-sm font-semibold text-indigo-600 dark:text-indigo-400">
                        {formatRupees(futureValue)}
                      </td>
                    </tr>
                  );
                })}
                <tr className="bg-indigo-50 dark:bg-indigo-900/20 font-medium">
                  <td className="px-4 py-3 text-sm font-bold text-gray-900 dark:text-white">
                    Total Portfolio
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                    -
                  </td>
                  <td className="px-4 py-3 text-sm font-bold text-gray-900 dark:text-white">
                    {formatRupees(
                      assets.reduce(
                        (sum, asset) =>
                          sum + asset.currentValue * asset.quantity,
                        0
                      )
                    )}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                    -
                  </td>
                  <td className="px-4 py-3 text-sm font-bold text-indigo-600 dark:text-indigo-400">
                    {formatRupees(
                      assets.reduce(
                        (sum, asset) =>
                          sum +
                          calculateFutureValue(
                            asset.currentValue * asset.quantity,
                            asset.expectedReturn,
                            timeframe
                          ),
                        0
                      )
                    )}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </CalculatorCard>

        <CalculatorCard title="Portfolio Growth Projection">
          <div className="h-[400px] relative">
            {!isGeneratingReport ? (
              <Slider {...sliderSettings}>
                {imagePaths.map((imagePath, index) => (
                  <div
                    key={index}
                    className="h-full flex items-center justify-center"
                  >
                    <img
                      src={`data:image/png;base64,${imagePath}`}
                      alt={`Stock Prediction ${index}`}
                      className="max-h-96 max-w-full object-contain"
                    />
                  </div>
                ))}
              </Slider>
            ) : (
              <div className="h-full flex items-center justify-center">
                <img
                  src="https://blogs.sas.com/content/graphicallyspeaking/files/2017/09/Stock_Plot_Discrete_Group.png"
                  alt="Placeholder"
                  className="h-96"
                />
              </div>
            )}
          </div>
        </CalculatorCard>
      </div>

      {/* Add New Asset Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <h3 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
          Add New Asset
        </h3>
        <div className="grid grid-cols-2 gap-4">
          <div className="col-span-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Asset Name
            </label>
            <input
              type="text"
              value={newAsset.name}
              onChange={(e) =>
                setNewAsset({ ...newAsset, name: e.target.value })
              }
              className="w-full p-2.5 border rounded-lg focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-transparent dark:bg-gray-700 dark:border-gray-600"
              placeholder="Enter asset name"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Quantity
            </label>
            <input
              type="number"
              value={newAsset.quantity || ""}
              onChange={(e) =>
                setNewAsset({ ...newAsset, quantity: Number(e.target.value) })
              }
              className="w-full p-2.5 border rounded-lg focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-transparent dark:bg-gray-700 dark:border-gray-600"
              placeholder="Enter quantity"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Current Value (₹)
            </label>
            <input
              type="number"
              value={newAsset.currentValue || ""}
              onChange={(e) =>
                setNewAsset({
                  ...newAsset,
                  currentValue: Number(e.target.value),
                })
              }
              className="w-full p-2.5 border rounded-lg focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-transparent dark:bg-gray-700 dark:border-gray-600"
              placeholder="Enter current value"
            />
          </div>
          <div className="col-span-2">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Expected Annual Return (%)
            </label>
            <div className="relative">
              <input
                type="number"
                value={newAsset.expectedReturn || ""}
                onChange={(e) =>
                  setNewAsset({
                    ...newAsset,
                    expectedReturn: Number(e.target.value),
                  })
                }
                className="w-full p-2.5 border rounded-lg focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 focus:border-transparent dark:bg-gray-700 dark:border-gray-600"
                placeholder="Enter expected return"
              />
              <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <span className="text-gray-500">%</span>
              </div>
            </div>
          </div>
        </div>
        <button
          onClick={() => {
            addAsset();
            setIsModalOpen(false);
          }}
          className="mt-6 w-full bg-indigo-600 text-white py-2.5 px-4 rounded-lg hover:bg-indigo-700 transition-colors font-medium"
        >
          Add Asset
        </button>
      </Modal>
    </div>
  );
};

export default MoneyCalc;
