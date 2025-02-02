import React, { useState } from "react";
import axios from "axios";
import DemoReport from "../components/DemoReport";
import { FileText } from "lucide-react";

interface ReportData {
  title: string;
  insights: string[];
  recommendations: string[];
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
      setReport(response.data);
    } catch (error) {
      console.error("Error fetching report:", error);
    } finally {
      setIsGeneratingReport(false);
    }
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

        {isGeneratingReport || !report ? (
          <DemoReport />
        ) : (
          <div className="bg-white p-6 shadow rounded-lg">
            <h1 className="text-2xl font-semibold text-gray-900 mb-4">
              {report.title}
            </h1>
            <h2 className="text-xl font-semibold text-gray-700">Insights:</h2>
            <ul className="list-disc ml-6 text-gray-600">
              {report.insights.map((insight, index) => (
                <li key={index}>{insight}</li>
              ))}
            </ul>

            <h2 className="text-xl font-semibold text-gray-700 mt-4">
              Recommendations:
            </h2>
            <ul className="list-disc ml-6 text-gray-600">
              {report.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default FinancialDashboard;
