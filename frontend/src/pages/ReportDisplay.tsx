import React, { useEffect, useState } from "react";

const MetricCard = ({
  title,
  value,
  subtitle,
  trend,
  icon,
}: {
  title: string;
  value: string;
  subtitle: string;
  trend: "up" | "down" | null;
  icon?: string;
}) => (
  <div className="bg-white p-4 rounded-lg shadow-sm">
    <div className="flex justify-between items-start mb-2">
      <span className="text-gray-600 text-sm">{title}</span>
      {icon && <span className="text-gray-400">{icon}</span>}
    </div>
    <div className="text-2xl font-bold mb-1">{value}</div>
    <div className="text-sm text-gray-600">{subtitle}</div>
    <div
      className={`text-sm ${
        trend === "up" ? "text-green-600" : "text-red-600"
      }`}
    >
      {trend === "up" ? "↑" : "↓"} vs Industry Average
    </div>
  </div>
);

const ReportDisplay = () => {
  const reportData = localStorage.getItem("report");

  const metrics = [
    {
      title: "P/E Ratio",
      value: "25.4x",
      subtitle: "Price to Earnings Ratio",
      trend: "down",
      icon: "$",
    },
    {
      title: "P/S Ratio",
      value: "3.2x",
      subtitle: "Price to Sales Ratio",
      trend: "up",
      icon: "↗",
    },
    {
      title: "Revenue Growth",
      value: "15%",
      subtitle: "Year over Year Growth",
      trend: "up",
      icon: "↗",
    },
    {
      title: "Earnings Growth",
      value: "22%",
      subtitle: "Year over Year Growth",
      trend: "up",
      icon: "↗",
    },
    {
      title: "Profit Margin",
      value: "18%",
      subtitle: "Net Profit Margin",
      trend: "down",
      icon: "%",
    },
  ];

  const stockRecommendations = [
    {
      symbol: "TSLA",
      name: "Tesla Inc.",
      price: "$180.32",
      peRatio: "45.2x",
      marketCap: "800B",
      sector: "Renewable Energy & EVs",
    },
    {
      symbol: "NEE",
      name: "NextEra Energy Inc.",
      price: "$75.15",
      peRatio: "22.5x",
      marketCap: "150B",
      sector: "Renewable Energy",
    },
    {
      symbol: "ENPH",
      name: "Enphase Energy Inc.",
      price: "$135.27",
      peRatio: "35.8x",
      marketCap: "25B",
      sector: "Solar Energy",
    },
    {
      symbol: "PLUG",
      name: "Plug Power Inc.",
      price: "$12.8",
      peRatio: "-10.4x",
      marketCap: "4.5B",
      sector: "Hydrogen & Fuel Cells",
    },
    {
      symbol: "VWS.CO",
      name: "Vestas Wind Systems",
      price: "$167.2",
      peRatio: "28.7x",
      marketCap: "30B",
      sector: "Wind Energy",
    },
  ];

  const references = [
    {
      author: "IRENA",
      year: "2023",
      title: "Renewable Energy Statistics 2023",
      org: "International Renewable Energy Agency",
      url: "https://www.irena.org/",
    },
    {
      author: "Bloomberg Green",
      year: "2023",
      title: "Green Energy Market Analysis",
      org: "Bloomberg",
      url: "https://www.bloomberg.com/green",
    },
  ];

  const [extractedMetrics, setExtractedMetrics] = useState([]);
  const [textContent, setTextContent] = useState("");
  const [metricData, setMetricData] = useState([]);

  useEffect(() => {
    extractData();
  }, [reportData]);

  const extractData = () => {
    const metricRegex = /"([^"]+)"/g; // Extracts content inside double quotes
    const values = [];
    let match;

    while ((match = metricRegex.exec(reportData)) !== null) {
      values.push(match[1]); // Extracted market metrics
    }

    setExtractedMetrics(values);

    // Remove the extracted metrics from the text content
    const textOnly = extractedMetrics[0];
    setTextContent(textOnly);
    setMetricData(extractedMetrics.slice(0));
  };

  return (
    <div className="max-w-6xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-8">
        Market Analysis: Trends in Green Energy Technologies
      </h1>

      {/* Financial Metrics Overview */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-2">
          Financial Metrics Overview
        </h2>
        <p className="text-sm text-gray-600 mb-4">
          Key performance indicators and valuation metrics
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          {metrics.map((metric, index) => (
            <MetricCard key={index} {...metric} />
          ))}
        </div>
      </div>

      {/* Abstract */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4">Abstract</h2>
        <p className="text-gray-800 leading-relaxed">
          This comprehensive analysis examines current market trends in green
          energy technologies, focusing on growth patterns, technological
          advancements, and market dynamics. The study synthesizes data from
          multiple authoritative sources to provide insights into market
          metrics, competitive landscapes, and future projections.
        </p>
      </div>

      {/* Market Overview */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4">Market Overview</h2>
        <p className="text-gray-800 leading-relaxed mb-4">
          The global green energy market has shown remarkable growth, with solar
          power reaching a valuation of $160 billion in 2022. Industry
          projections suggest a trajectory toward $320 billion by 2027,
          representing a compound annual growth rate (CAGR) of 15%. [
          <a href="#" className="text-blue-600">
            irena2023
          </a>
          ,
          <a href="#" className="text-blue-600">
            bloomberg2023
          </a>
          ]
        </p>
      </div>

      {/* Stock Recommendations */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4">
          <span className="mr-2">$</span>
          Stock Recommendations
        </h2>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white">
            <thead>
              <tr className="bg-gray-50 text-gray-600 text-sm">
                <th className="py-3 px-4 text-left">SYMBOL</th>
                <th className="py-3 px-4 text-left">NAME</th>
                <th className="py-3 px-4 text-right">PRICE</th>
                <th className="py-3 px-4 text-right">P/E RATIO</th>
                <th className="py-3 px-4 text-right">MARKET CAP</th>
                <th className="py-3 px-4 text-left">SECTOR</th>
              </tr>
            </thead>
            <tbody className="text-gray-800">
              {stockRecommendations.map((stock, index) => (
                <tr key={index} className="border-t">
                  <td className="py-3 px-4">{stock.symbol}</td>
                  <td className="py-3 px-4">{stock.name}</td>
                  <td className="py-3 px-4 text-right">{stock.price}</td>
                  <td className="py-3 px-4 text-right">{stock.peRatio}</td>
                  <td className="py-3 px-4 text-right">{stock.marketCap}</td>
                  <td className="py-3 px-4">{stock.sector}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* References */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold mb-4">References</h2>
        <div className="space-y-3">
          {references.map((ref, index) => (
            <div key={index} className="text-sm">
              <p>
                {ref.author} ({ref.year}). {ref.title}. {ref.org}.{" "}
                <a
                  href={ref.url}
                  className="text-blue-600 hover:underline"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {ref.url}
                </a>
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ReportDisplay;
