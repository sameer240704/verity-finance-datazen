import React, { useState, useEffect } from "react";
import {
  ExternalLink,
  TrendingUp,
  FileText,
  Link as LinkIcon,
  PieChart,
  BarChart as BarChartIcon,
  TrendingDown,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface Source {
  name: string;
  url: string;
}

interface Stock {
  stock_name: string;
  ticker: string;
  justification: string;
  market_performance: string;
}

interface ParsedData {
  textual: string[];
  sources: Source[];
  top5Stocks: Stock[];
}

const Card = ({ children, className = "" }) => (
  <div
    className={`bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden ${className}`}
  >
    {children}
  </div>
);

const MetricCard = ({ title, value, trend, subtitle }) => (
  <div className="p-4 border rounded-lg">
    <div className="flex items-center justify-between mb-2">
      <h3 className="text-sm text-gray-600">{title}</h3>
      {trend === "up" ? (
        <TrendingUp className="w-4 h-4 text-green-500" />
      ) : trend === "down" ? (
        <TrendingDown className="w-4 h-4 text-red-500" />
      ) : null}
    </div>
    <div className="text-2xl font-bold mb-1">{value}</div>
    {subtitle && <div className="text-xs text-gray-500">{subtitle}</div>}
  </div>
);

const StockCard = ({ stock }: { stock: Stock }) => (
  <tr className="border-b border-gray-200">
    <td className="px-4 py-3">{stock.stock_name}</td>
    <td className="px-4 py-3">{stock.ticker}</td>
    <td className="px-4 py-3">{stock.market_performance}</td>
    <td className="px-4 py-3">{stock.justification}</td>
  </tr>
);

const SourcesList = ({ sources }: { sources: Source[] }) => (
  <div className="space-y-2">
    {sources.map((source, index) => (
      <div key={index} className="flex items-center gap-2">
        <LinkIcon className="w-4 h-4 text-blue-500" />
        <a
          href={source.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-500 hover:text-blue-700"
        >
          {source.name}
        </a>
      </div>
    ))}
  </div>
);

const TextualContent = ({ content }: { content: string[] }) => (
  <div className="space-y-6">
    {content.map((section, index) => (
      <div key={index} className="prose max-w-none">
        <div
          dangerouslySetInnerHTML={{
            __html: section
              .replace(/^#+ /gm, "")
              .replace(/\n- /g, "\n")
              .replace(/\n/g, "<br />")
              .replace(/\*\*/g, "")
              .replace(/\*/g, ""),
          }}
        />
      </div>
    ))}
  </div>
);

const MarketMetrics = () => {
  const growthData = [
    { name: "Healthcare IT", rate: 25.6 },
    { name: "Telehealth", rate: 19.5 },
    { name: "Genomics", rate: 8.5 },
    { name: "Sterilization", rate: 6.2 },
  ];

  return (
    <Card className="p-6">
      <h2 className="text-lg font-semibold mb-6">Key Market Metrics</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <MetricCard
          title="Healthcare IT Market"
          value="$350B"
          trend="up"
          subtitle="Global market size"
        />
        <MetricCard
          title="Telehealth Market"
          value="$455B"
          trend="up"
          subtitle="Projected by 2032"
        />
        <MetricCard
          title="Genomic Testing"
          value="45%"
          trend="up"
          subtitle="Oncology market share"
        />
        <MetricCard
          title="Cloud Market Share"
          value="70%"
          trend="up"
          subtitle="Major providers control"
        />
      </div>
      <div className="h-64">
        <h3 className="text-md font-semibold mb-4">Growth Rates (CAGR %)</h3>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={growthData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="rate" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
};

const HealthcareReportParser = () => {
  const [parsedData, setParsedData] = useState<ParsedData>({
    textual: [],
    sources: [],
    top5Stocks: [],
  });

  const data = localStorage.getItem("report") || "";

  useEffect(() => {
    const parseData = () => {
      const textualData: string[] = [];
      const sourcesData: Source[] = [];
      const top5StocksData: Stock[] = [];

      const sections = data.split("---").filter((section) => section.trim());

      sections.forEach((section) => {
        if (
          !section.includes("Sources") &&
          !section.includes("Top 5 Performing Stocks")
        ) {
          const cleanedSection = section
            .replace(/^#+ /gm, "")
            .replace(/\n- /g, "\n")
            .replace(/\*\*/g, "")
            .replace(/\*/g, "")
            .trim();
          if (cleanedSection) {
            textualData.push(cleanedSection);
          }
        }
      });

      // Parse sources and stocks as before...
      const sourcesSection = sections.find((section) =>
        section.includes("Sources")
      );
      if (sourcesSection) {
        const sourceLines = sourcesSection
          .split("\n")
          .filter((line) => line.includes("-"));
        sourceLines.forEach((line) => {
          const [name, url] = line.replace(/^-\s*/, "").split(": ");
          if (name && url) {
            sourcesData.push({
              name: name.trim().replace(/\*\*/g, "").replace(/\*/g, ""),
              url: url.trim(),
            });
          }
        });
      }

      const stocksSection = sections.find((section) =>
        section.includes("Top 5 Performing Stocks")
      );
      if (stocksSection) {
        const stockEntries = stocksSection
          .split(/\d\./)
          .filter((entry) => entry.trim());
        stockEntries.forEach((entry) => {
          const lines = entry
            .split("\n")
            .map((line) => line.replace(/^-\s*/, ""))
            .filter((line) => line.trim());
          if (lines.length >= 3) {
            const nameMatch = lines[0].match(/(.*?)\((.*?)\):/);
            if (nameMatch) {
              const stock: Stock = {
                stock_name: nameMatch[1]
                  .trim()
                  .replace(/\*\*/g, "")
                  .replace(/\*/g, ""),
                ticker: nameMatch[2].trim(),
                market_performance: lines[1]
                  .replace("Market Performance:", "")
                  .replace(/\*\*/g, "")
                  .replace(/\*/g, "")
                  .trim(),
                justification: lines[2]
                  .replace("Justification:", "")
                  .replace(/\*\*/g, "")
                  .replace(/\*/g, "")
                  .trim(),
              };
              top5StocksData.push(stock);
            }
          }
        });
      }

      setParsedData({
        textual: textualData,
        sources: sourcesData,
        top5Stocks: top5StocksData,
      });
    };

    parseData();
  }, [data]);

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      <h1 className="text-4xl font-bold mb-8">
        <TextualContent content={parsedData.textual.slice(0, 1)} />
      </h1>

      <div className="space-y-8">
        <MarketMetrics />

        <Card>
          <div className="p-6">
            <h2 className="text-lg font-semibold mb-4">Market Overview</h2>
            <TextualContent content={parsedData.textual.slice(2, 3)} />
          </div>
        </Card>

        <Card>
          <div className="p-6">
            <h2 className="text-lg font-semibold mb-4">
              Competitive Landscape
            </h2>
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 text-left">
                  <th className="px-4 py-3 font-semibold">Company</th>
                  <th className="px-4 py-3 font-semibold">Symbol</th>
                  <th className="px-4 py-3 font-semibold">Performance</th>
                  <th className="px-4 py-3 font-semibold">Notes</th>
                </tr>
              </thead>
              <tbody>
                {parsedData.top5Stocks.map((stock, index) => (
                  <StockCard key={index} stock={stock} />
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        <Card>
          <div className="p-6">
            <h2 className="text-lg font-semibold mb-4">References</h2>
            <SourcesList sources={parsedData.sources} />
          </div>
        </Card>
      </div>
    </div>
  );
};

export default HealthcareReportParser;
