import React, { useState } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

// Types
interface MarketMetrics {
  sector: string;
  marketSize: number;
  growthRate: number;
  marketShare: {
    company: string;
    share: number;
  }[];
  profitMargin: {
    min: number;
    max: number;
  };
  roi: {
    min: number;
    max: number;
  };
}

interface StockPerformance {
  ticker: string;
  name: string;
  ytdGain: number;
  justification: string;
}

// Sample data
const marketMetrics: MarketMetrics[] = [
  {
    sector: "Solar Power",
    marketSize: 160,
    growthRate: 15,
    marketShare: [
      { company: "JinkoSolar", share: 15 },
      { company: "First Solar", share: 11 },
      { company: "Canadian Solar", share: 9 },
      { company: "SunPower", share: 5 }
    ],
    profitMargin: { min: 10, max: 15 },
    roi: { min: 12, max: 18 }
  },
  {
    sector: "Wind Power",
    marketSize: 100,
    growthRate: 10,
    marketShare: [
      { company: "Vestas", share: 17 },
      { company: "GE Renewable", share: 14 },
      { company: "Siemens Gamesa", share: 15 },
      { company: "Goldwind", share: 13 },
      { company: "Envision", share: 9 }
    ],
    profitMargin: { min: 7, max: 12 },
    roi: { min: 10, max: 15 }
  }
];

const stockPerformance: StockPerformance[] = [
  {
    ticker: "JKS",
    name: "JinkoSolar",
    ytdGain: 50,
    justification: "Global leadership in solar PV manufacturing"
  },
  {
    ticker: "FSLR",
    name: "First Solar",
    ytdGain: 45,
    justification: "Beneficiary of U.S. Inflation Reduction Act"
  },
  {
    ticker: "VWS.CO",
    name: "Vestas",
    ytdGain: 30,
    justification: "Strong pipeline in Europe"
  },
  {
    ticker: "GE",
    name: "GE Renewable Energy",
    ytdGain: 40,
    justification: "Expansion in offshore wind"
  },
  {
    ticker: "SGREN",
    name: "Siemens Gamesa",
    ytdGain: 25,
    justification: "Dominance in offshore wind"
  }
];

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const MarketAnalysisDashboard: React.FC = () => {
  const [selectedSector, setSelectedSector] = useState<string>("Solar Power");

  const selectedMetrics = marketMetrics.find(m => m.sector === selectedSector);

  return (
    <div className="max-w-7xl mx-auto p-6 bg-gray-50">
      <h1 className="text-3xl font-bold mb-8">Green Energy Market Analysis</h1>
      
      <div className="mb-6">
        <select 
          className="p-2 border rounded"
          value={selectedSector}
          onChange={(e) => setSelectedSector(e.target.value)}
        >
          {marketMetrics.map(metric => (
            <option key={metric.sector} value={metric.sector}>
              {metric.sector}
            </option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Market Size and Growth */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Market Overview</h2>
          <div className="mb-4">
            <p className="text-gray-600">Market Size</p>
            <p className="text-2xl font-bold">${selectedMetrics?.marketSize}B</p>
          </div>
          <div>
            <p className="text-gray-600">Growth Rate</p>
            <p className="text-2xl font-bold">{selectedMetrics?.growthRate}%</p>
          </div>
        </div>

        {/* Market Share Pie Chart */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Market Share</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={selectedMetrics?.marketShare}
                dataKey="share"
                nameKey="company"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
              >
                {selectedMetrics?.marketShare.map((entry, index) => (
                  <Cell key={entry.company} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Financial Performance */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Financial Metrics</h2>
          <div className="mb-4">
            <p className="text-gray-600">Profit Margin Range</p>
            <p className="text-xl font-bold">
              {selectedMetrics?.profitMargin.min}% - {selectedMetrics?.profitMargin.max}%
            </p>
          </div>
          <div>
            <p className="text-gray-600">ROI Range</p>
            <p className="text-xl font-bold">
              {selectedMetrics?.roi.min}% - {selectedMetrics?.roi.max}%
            </p>
          </div>
        </div>

        {/* Top Performing Stocks */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Top Performing Stocks</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stockPerformance}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ticker" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="ytdGain" name="YTD Gain %" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Stock Details Table */}
      <div className="mt-6 bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Stock Performance Details</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="bg-gray-100">
                <th className="p-4 text-left">Ticker</th>
                <th className="p-4 text-left">Company</th>
                <th className="p-4 text-left">YTD Gain</th>
                <th className="p-4 text-left">Justification</th>
              </tr>
            </thead>
            <tbody>
              {stockPerformance.map((stock) => (
                <tr key={stock.ticker} className="border-b">
                  <td className="p-4">{stock.ticker}</td>
                  <td className="p-4">{stock.name}</td>
                  <td className="p-4">{stock.ytdGain}%</td>
                  <td className="p-4">{stock.justification}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default MarketAnalysisDashboard;