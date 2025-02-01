// StockHoldingsForm.tsx
import React from "react";

interface StockHolding {
  stockName: string;
  tickerSymbol: string;
  numberOfShares: number;
  purchasePrice: number;
  purchaseDate: string;
}

interface StockHoldingsFormProps {
  formData: StockHolding;
  setFormData: React.Dispatch<React.SetStateAction<StockHolding>>;
}

const StockHoldingsForm: React.FC<StockHoldingsFormProps> = ({
  formData,
  setFormData,
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        name === "numberOfShares" || name === "purchasePrice"
          ? Number(value)
          : value,
    }));
  };

  return (
    <div className="p-4 bg-white shadow rounded-lg">
      <form className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Stock Name
          </label>
          <input
            type="text"
            name="stockName"
            value={formData.stockName}
            onChange={handleChange}
            placeholder="Stock Name"
            className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Ticker Symbol
          </label>
          <input
            type="text"
            name="tickerSymbol"
            value={formData.tickerSymbol}
            onChange={handleChange}
            placeholder="Ticker Symbol"
            className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Number of Shares
          </label>
          <input
            type="number"
            name="numberOfShares"
            value={formData.numberOfShares}
            onChange={handleChange}
            placeholder="Number of Shares"
            className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Purchase Price
          </label>
          <input
            type="number"
            name="purchasePrice"
            value={formData.purchasePrice}
            onChange={handleChange}
            placeholder="Purchase Price"
            className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Purchase Date
          </label>
          <input
            type="date"
            name="purchaseDate"
            value={formData.purchaseDate}
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
          />
        </div>
      </form>
    </div>
  );
};

export default StockHoldingsForm;
