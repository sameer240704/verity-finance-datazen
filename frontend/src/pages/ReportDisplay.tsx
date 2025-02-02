import React from "react";

interface MarketMetric {
  title: string;
  value: string;
  details?: string[];
}

interface StockPerformance {
  name: string;
  ticker?: string;
  performance: string;
  justification: string;
}

interface ResearchCitation {
  title: string;
  url: string;
}

interface ParsedReport {
  metrics: MarketMetric[];
  analysis: Record<string, string[]>;
  citations: ResearchCitation[];
  topStocks: StockPerformance[];
}

const parseReport = (reportText: string | null): ParsedReport => {
  if (!reportText) {
    return { metrics: [], analysis: {}, citations: [], topStocks: [] };
  }

  const report: ParsedReport = {
    metrics: [],
    analysis: {},
    citations: [],
    topStocks: [],
  };

  // Helper function for extracting sections
  const extractSection = (regex: RegExp) => reportText.match(regex)?.[1] || "";

  // Parse Market Metrics
  const metricsSection = extractSection(
    /## 1\. Market Metrics([\s\S]*?)(?=## 2\.|$)/
  );
  if (metricsSection) {
    report.metrics = metricsSection
      .split("### ")
      .slice(1)
      .map((block) => {
        const lines = block.split("\n").filter(Boolean);
        return {
          title: lines[0]?.replace(/\*\*/g, "").trim() || "",
          value:
            lines
              .find((line) => line.includes("**"))
              ?.replace(/\*\*/g, "")
              .trim() || "",
          details: lines
            .filter((line) => line.startsWith("- "))
            .map((line) => line.replace(/^- /, "").trim()),
        };
      });
  }

  // Parse Analysis Report
  const analysisSection = extractSection(
    /## 2\. Analysis Report([\s\S]*?)(?=## 3\.|$)/
  );
  if (analysisSection) {
    const topics = [
      "trends",
      "technology",
      "regulations",
      "competition",
      "opportunities",
      "risks",
      "sentiment",
    ];
    topics.forEach((topic) => {
      const match = analysisSection.match(
        new RegExp(
          `${topic.replace(/([A-Z])/g, " $1")}([\s\S]*?)(?=###|$)`,
          "i"
        )
      );
      report.analysis[topic] =
        match?.[1]
          ?.split("\n")
          .filter((line) => line.startsWith("- "))
          .map((line) => line.replace(/^- /, "").trim()) || [];
    });
  }

  // Parse Research Citations
  const citationsSection = extractSection(
    /## 3\. Sources([\s\S]*?)(?=## 4\.|$)/
  );
  report.citations = citationsSection
    .split("\n")
    .filter((line) => line.includes("http"))
    .map((line) => {
      const [title, url] = line.split("(");
      return {
        title: title.replace(/^- /, "").trim(),
        url: url?.replace(")", "").trim() || "",
      };
    });

  // Parse Top Stocks
  const stocksSection = extractSection(
    /## 4\. Top 5 Performing Stocks([\s\S]*?)(?=---|$)/
  );
  if (stocksSection) {
    report.topStocks = stocksSection
      .split(/\d+\. \*\*/)
      .slice(1)
      .map((block) => {
        const lines = block.split("\n").filter(Boolean);
        return {
          name: lines[0]?.replace(/\*\*/g, "").trim() || "",
          ticker: lines[0]?.match(/\((.*?)\)/)?.[1] || "",
          performance:
            lines
              .find((line) => /Performance:/i.test(line))
              ?.replace(/Performance:/i, "")
              .trim() || "",
          justification:
            lines
              .find((line) => /Justification:/i.test(line))
              ?.replace(/Justification:/i, "")
              .trim() || "",
        };
      });
  }

  return report;
};

const ReportDisplay = () => {
  const reportText = localStorage.getItem("report");
  const parsedReport = parseReport(reportText);

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Market Metrics */}
      {reportText}
    </div>
  );
};

export default ReportDisplay;
