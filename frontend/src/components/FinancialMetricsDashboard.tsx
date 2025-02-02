import React from "react";
import {
  TrendingUp,
  DollarSign,
  Percent,
  LineChart as LineChartIcon,
} from "lucide-react";

interface FinancialMetrics {
  peRatio: number;
  psRatio: number;
  revenueGrowth: number;
  earningsGrowth: number;
  profitMargin: number;
}

interface MetricCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  description: string;
  trend?: "positive" | "negative";
}

const MetricCard = ({
  title,
  value,
  icon,
  description,
  trend,
}: MetricCardProps) => {
  const isPercentage = title.includes("Growth") || title.includes("Margin");
  const displayValue = isPercentage ? value * 100 : value;

  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-sm font-medium text-gray-500">{title}</h3>
        <div className="text-gray-600">{icon}</div>
      </div>
      <div className="text-2xl font-bold">
        {displayValue}
        {isPercentage ? "%" : "x"}
      </div>
      <p className="text-xs text-gray-500 mt-1">{description}</p>
      {trend && (
        <div
          className={`text-xs mt-2 ${
            trend === "positive" ? "text-green-600" : "text-red-600"
          }`}
        >
          {trend === "positive" ? "↑" : "↓"} vs Industry Average
        </div>
      )}
    </div>
  );
};

const FinancialMetricsDashboard = ({
  metrics,
}: {
  metrics: FinancialMetrics;
}) => {
  console.log(metrics);

  return (
    <div className="p-6 bg-gray-50">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-800">
          Financial Metrics Overview
        </h2>
        <p className="text-gray-600">
          Key performance indicators and valuation metrics
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <MetricCard
          title="P/E Ratio"
          value={metrics.peRatio}
          icon={<DollarSign size={20} />}
          description="Price to Earnings Ratio"
          trend={metrics.peRatio < 25 ? "positive" : "negative"}
        />

        <MetricCard
          title="P/S Ratio"
          value={metrics.psRatio}
          icon={<LineChartIcon size={20} />}
          description="Price to Sales Ratio"
          trend={metrics.psRatio < 5 ? "positive" : "negative"}
        />

        <MetricCard
          title="Revenue Growth"
          value={metrics.revenueGrowth}
          icon={<TrendingUp size={20} />}
          description="Year over Year Growth"
          trend={metrics.revenueGrowth > 0.1 ? "positive" : "negative"}
        />

        <MetricCard
          title="Earnings Growth"
          value={metrics.earningsGrowth}
          icon={<LineChartIcon size={20} />}
          description="Year over Year Growth"
          trend={metrics.earningsGrowth > 0.15 ? "positive" : "negative"}
        />

        <MetricCard
          title="Profit Margin"
          value={metrics.profitMargin}
          icon={<Percent size={20} />}
          description="Net Profit Margin"
          trend={metrics.profitMargin > 0.2 ? "positive" : "negative"}
        />
      </div>
    </div>
  );
};

export default FinancialMetricsDashboard;
