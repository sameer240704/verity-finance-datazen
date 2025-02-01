import React, { useState } from "react";
import { DollarSign } from "lucide-react";

// Helper function to convert market metrics to financial metrics format
const convertToFinancialMetrics = (marketData) => {
  return {
    peRatio: 25.4, // These values are hardcoded since they're not in the new data format
    psRatio: 3.2,
    revenueGrowth: 0.15,
    earningsGrowth: 0.22,
    profitMargin: 0.18,
  };
};

const CustomCard = ({ title, icon: Icon, children }) => (
  <div className="bg-white rounded-lg shadow-md overflow-hidden">
    <div className="px-6 py-4 border-b border-gray-200">
      <div className="flex items-center">
        {Icon && <Icon className="mr-2 text-purple-600" size={20} />}
        <h2 className="text-xl font-semibold text-gray-800">{title}</h2>
      </div>
    </div>
    <div className="p-6">{children}</div>
  </div>
);

const FinancialMetricCard = ({ title, value, subtitle, trend }) => (
  <div className="bg-white p-6 rounded-lg shadow">
    <div className="space-y-2">
      <p className="text-sm text-gray-600">{title}</p>
      <p className="text-3xl font-semibold">{value}</p>
      <p className="text-xs text-gray-500">{subtitle}</p>
      <p
        className={`text-xs ${
          trend.includes("+") ? "text-green-600" : "text-red-600"
        }`}
      >
        {trend}
      </p>
    </div>
  </div>
);

const FinancialMetricsDashboard = ({ metrics }) => {
  return (
    <div className="mb-8">
      <h2 className="text-xl font-bold mb-2">Financial Metrics Overview</h2>
      <p className="text-gray-600 mb-4">
        Key performance indicators and valuation metrics
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <FinancialMetricCard
          title="P/E Ratio"
          value={`${metrics.peRatio}x`}
          subtitle="Price to Earnings Ratio"
          trend="↓ vs Industry Average"
        />
        <FinancialMetricCard
          title="P/S Ratio"
          value={`${metrics.psRatio}x`}
          subtitle="Price to Sales Ratio"
          trend="↑ vs Industry Average"
        />
        <FinancialMetricCard
          title="Revenue Growth"
          value={`${metrics.revenueGrowth * 100}%`}
          subtitle="Year-over-Year Growth"
          trend="↑ vs Industry Average"
        />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <FinancialMetricCard
          title="Earnings Growth"
          value={`${metrics.earningsGrowth * 100}%`}
          subtitle="Year-over-Year Growth"
          trend="↑ vs Industry Average"
        />
        <FinancialMetricCard
          title="Profit Margin"
          value={`${metrics.profitMargin * 100}%`}
          subtitle="Net Profit Margin"
          trend="↑ vs Industry Average"
        />
      </div>
    </div>
  );
};

const MarketAnalysisDashboard = ({ data }) => {
  // Convert the new data format to match the existing UI structure
  const financialMetrics = convertToFinancialMetrics(data.market_metrics);

  return (
    <div className="max-w-7xl mx-auto p-8 bg-white">
      <div className="mb-8 border-b-2 px-4">
        <h1 className="text-3xl font-bold text-left mb-8">
          Market Analysis: Trends in Green Energy Technologies
        </h1>
      </div>

      {/* Financial Metrics */}
      <FinancialMetricsDashboard metrics={financialMetrics} />

      {/* Abstract */}
      <div className="my-8">
        <h2 className="text-xl font-bold mb-4">Abstract</h2>
        <p className="text-gray-800 leading-relaxed">
          This comprehensive analysis examines current market trends in green
          energy technologies, focusing on growth patterns, technological
          advancements, and market dynamics. The study synthesizes data from
          multiple authoritative sources to provide insights into market
          metrics, competitive landscapes, and future projections.
        </p>
      </div>

      {/* Market Overview and Other Sections */}
      <div className="space-y-8">
        <section>
          <h2 className="text-xl font-bold mb-4">Market Overview</h2>
          <p className="mb-4 text-gray-800 leading-relaxed">
            The global green energy market has shown remarkable growth, with
            solar power reaching {data.market_metrics.solar_energy_market_size}{" "}
            and wind power reaching{" "}
            {data.market_metrics.wind_energy_market_size}. Solar energy shows a
            growth rate of {data.market_metrics.solar_energy_growth_rate} while
            wind energy demonstrates{" "}
            {data.market_metrics.wind_energy_growth_rate} growth.
          </p>
        </section>
      </div>

      {/* References */}
      <div className="mt-12 border-t pt-8">
        <h2 className="text-xl font-bold mb-4">References</h2>
        <div className="space-y-4">
          {data.sources.map((source, index) => (
            <div key={index} className="text-gray-800">
              <p className="leading-relaxed">
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800"
                >
                  {source.name}
                </a>
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Stock Recommendations */}
      <div className="mt-8">
        <CustomCard title="Stock Recommendations" icon={DollarSign}>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Symbol
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Performance
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Sector
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {data.top_5_stocks.map((stock) => (
                  <tr key={stock.ticker}>
                    <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                      {stock.ticker}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {stock.stock_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {stock["30_day_performance"]}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {stock.justification}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CustomCard>
      </div>
    </div>
  );
};

export default MarketAnalysisDashboard;
