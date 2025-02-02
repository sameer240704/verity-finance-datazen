import React, { useState } from "react";
import axios from "axios";
import DemoReport from "../components/DemoReport";
import { FileText } from "lucide-react";

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

interface BondData {
  bondType: string;
  couponRate: number;
  interestEarned: number;
  maturityDate: string;
  principal: number;
  weightageInPortfolio: number;
  yieldToMaturity: number;
}

interface Stock {
  company_info: CompanyInfo;
  stock_data: StockData;
}

interface ReportData {
  json_data?: {
    bonds: BondData[];
    stocks: { [ticker: string]: Stock };
  };
  text_data?: {
    summary: string;
    recommendations: string;
    conclusion: string;
  };
}

const FinancialDashboard: React.FC = () => {
  const [isGeneratingReport, setIsGeneratingReport] = useState<boolean>(false);
  const [report, setReport] = useState<ReportData | null>(null);

  const generateReport = async () => {
    setIsGeneratingReport(true);

    try {
      const response = await axios.get<ReportData>(
        "http://127.0.0.1:5000/portfolio_generation"
      );
      setReport(response?.data?.portfolio_data);
    } catch (error) {
      console.error("Error fetching report:", error);
    } finally {
      setIsGeneratingReport(false);
    }
  };

  const formatText = (text: string | undefined): React.ReactNode => {
    if (!text) return null;
    const parts = text.split(/(\*\*.*?\*\*|\*)/g).filter(Boolean);
    return parts.map((part, index) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <span key={index} className="font-bold">
            {part.slice(2, -2)}
          </span>
        );
      } else if (part === "*") {
        return <br key={index} />;
      } else {
        return part;
      }
    });
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto p-6 space-y-6">
        {/* Header Section */}
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Smart Reports Dashboard
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              Key insights and recommendations for your portfolio
            </p>
          </div>

          {/* Generate Report Button */}
          <button
            onClick={generateReport}
            disabled={isGeneratingReport}
            className="flex items-center gap-2 bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 disabled:bg-gray-400"
          >
            <FileText className="w-4 h-4" />
            {isGeneratingReport ? "Generating Report..." : "Generate Report"}
          </button>
        </div>

        {!report ? (
          <DemoReport />
        ) : (
          <div className="bg-white p-6 shadow rounded-lg space-y-4">
            {/* Text Report */}
            {report?.text_data && (
              <section className="space-y-6">
                <div className="text-gray-900">
                  <h2 className="text-3xl font-bold mb-2">
                    Portfolio Analysis
                  </h2>
                </div>

                <div className="space-y-4">
                  <div className="border p-4 rounded-md mb-4 bg-gray-50">
                    <h3 className="text-2xl font-semibold text-gray-700">
                      <span className="font-bold text-gray-900 text-xl">
                        Portfolio Summary:
                      </span>
                    </h3>
                    <p className="text-gray-600">
                      {formatText(report?.text_data?.summary)}
                    </p>
                  </div>
                  <div className="border p-4 rounded-md mb-4 bg-gray-50">
                    <h3 className="text-2xl font-semibold text-gray-700">
                      <span className="font-bold text-gray-900 text-xl">
                        Recommended Stocks:
                      </span>
                    </h3>
                    <p className="text-gray-600">
                      {formatText(report?.text_data?.recommendations)}
                    </p>
                  </div>
                  <div className="border p-4 rounded-md mb-4 bg-gray-50">
                    <h3 className="text-2xl font-semibold text-gray-700">
                      <span className="font-bold text-gray-900 text-xl">
                        Conclusion:
                      </span>
                    </h3>
                    <p className="text-gray-600">
                      {formatText(report?.text_data?.conclusion)}
                    </p>
                  </div>
                </div>
              </section>
            )}

            {/* JSON Data Report */}
            {report?.json_data?.stocks && (
              <section>
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  Stocks
                </h2>
                {Object.entries(report.json_data.stocks).map(
                  ([ticker, stock]) => (
                    <div
                      key={ticker}
                      className="border p-6 rounded-md mb-6 bg-gray-50"
                    >
                      <h3 className="text-2xl font-semibold text-gray-700 mb-4">
                        {stock?.stock_data?.stockName} ({ticker})
                      </h3>
                      <div className="flex flex-wrap gap-4 mb-4">
                        <div className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
                          <span className="font-medium text-gray-700">
                            Current Price:
                          </span>{" "}
                          <span className="text-gray-600">
                            ${stock?.stock_data?.currentPrice}
                          </span>
                        </div>
                        <div className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
                          <span className="font-medium text-gray-700">
                            Dividend Yield:
                          </span>{" "}
                          <span className="text-gray-600">
                            {stock?.stock_data?.dividendYield}%
                          </span>
                        </div>
                        <div className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
                          <span className="font-medium text-gray-700">
                            Number of Shares:
                          </span>{" "}
                          <span className="text-gray-600">
                            {stock?.stock_data?.numberOfShares}
                          </span>
                        </div>
                        <div className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
                          <span className="font-medium text-gray-700">
                            Purchase Date:
                          </span>{" "}
                          <span className="text-gray-600">
                            {stock?.stock_data?.purchaseDate}
                          </span>
                        </div>
                        <div className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
                          <span className="font-medium text-gray-700">
                            Purchase Price:
                          </span>{" "}
                          <span className="text-gray-600">
                            ${stock?.stock_data?.purchasePrice}
                          </span>
                        </div>
                        <div className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
                          <span className="font-medium text-gray-700">
                            Unrealized Gains/Losses:
                          </span>{" "}
                          <span className="text-gray-600">
                            ${stock?.stock_data?.unrealizedGainsLosses}
                          </span>
                        </div>
                        <div className="w-full sm:w-1/2 md:w-1/3 lg:w-1/4">
                          <span className="font-medium text-gray-700">
                            Weightage in Portfolio:
                          </span>{" "}
                          <span className="text-gray-600">
                            {stock?.stock_data?.weightageInPortfolio}%
                          </span>
                        </div>
                      </div>
                      <h4 className="text-xl font-semibold text-gray-700 mt-2 mb-4">
                        Income Statements
                      </h4>
                      <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                          <thead>
                            <tr>
                              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Date
                              </th>
                              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Revenue
                              </th>
                              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Net Income
                              </th>
                              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Net Profit Margin
                              </th>
                              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Earnings Per Share
                              </th>
                              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                EBITDA
                              </th>
                            </tr>
                          </thead>
                          <tbody className="bg-white divide-y divide-gray-200">
                            {stock?.company_info?.income_statement?.map(
                              (statement, index) => (
                                <tr key={index}>
                                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                                    {statement.date}
                                  </td>
                                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                                    ${statement.revenue}
                                  </td>
                                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                                    ${statement.net_income}
                                  </td>
                                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                                    {statement.net_profit_margin}%
                                  </td>
                                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                                    {statement.earnings_per_share}
                                  </td>
                                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                                    ${statement.EBITDA}
                                  </td>
                                </tr>
                              )
                            )}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )
                )}
              </section>
            )}
            {report?.json_data?.bonds && (
              <section>
                <h2 className="text-3xl font-bold text-gray-900 mb-4">Bonds</h2>
                {report.json_data.bonds.map((bond, index) => (
                  <div
                    key={index}
                    className="border p-4 rounded-md mb-4 bg-gray-50"
                  >
                    <h3 className="text-2xl font-semibold text-gray-700 mb-4">
                      {bond.bondType}
                    </h3>
                    <div className="mb-2">
                      <span className="font-medium text-gray-700">
                        Coupon Rate:
                      </span>{" "}
                      <span className="text-gray-600">{bond.couponRate}%</span>
                    </div>
                    <div className="mb-2">
                      <span className="font-medium text-gray-700">
                        Interest Earned:
                      </span>{" "}
                      <span className="text-gray-600">
                        ${bond.interestEarned}
                      </span>
                    </div>
                    <div className="mb-2">
                      <span className="font-medium text-gray-700">
                        Maturity Date:
                      </span>{" "}
                      <span className="text-gray-600">{bond.maturityDate}</span>
                    </div>
                    <div className="mb-2">
                      <span className="font-medium text-gray-700">
                        Principal:
                      </span>{" "}
                      <span className="text-gray-600">${bond.principal}</span>
                    </div>
                    <div className="mb-2">
                      <span className="font-medium text-gray-700">
                        Weightage in Portfolio:
                      </span>{" "}
                      <span className="text-gray-600">
                        {bond.weightageInPortfolio}%
                      </span>
                    </div>
                    <div className="mb-2">
                      <span className="font-medium text-gray-700">
                        Yield to Maturity:
                      </span>{" "}
                      <span className="text-gray-600">
                        {bond.yieldToMaturity}%
                      </span>
                    </div>
                  </div>
                ))}
              </section>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default FinancialDashboard;
