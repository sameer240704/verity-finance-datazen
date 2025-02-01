// BondsForm.tsx
import React from "react";

interface BondHolding {
  bondType: string;
  maturityDate: string;
  couponRate: number;
  principal: number;
  yieldToMaturity: number;
  interestEarned: number;
}

interface BondsFormProps {
  formData: BondHolding;
  setFormData: React.Dispatch<React.SetStateAction<BondHolding>>;
}

const BondsForm: React.FC<BondsFormProps> = ({ formData, setFormData }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

    setFormData((prev) => {
      const updatedData = {
        ...prev,
        [name]:
          name === "couponRate" || name === "principal" ? Number(value) : value,
      };

      updatedData.interestEarned =
        (updatedData.couponRate / 100) * updatedData.principal;

      updatedData.yieldToMaturity =
        updatedData.couponRate +
        (updatedData.interestEarned / updatedData.principal) * 100;

      return updatedData;
    });
  };

  return (
    <div className="p-4 bg-white shadow rounded-lg">
      <form className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Bond Type
          </label>
          <input
            type="text"
            name="bondType"
            value={formData.bondType}
            onChange={handleChange}
            placeholder="Government, Corporate, etc."
            className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Maturity Date
          </label>
          <input
            type="date"
            name="maturityDate"
            value={formData.maturityDate}
            onChange={handleChange}
            className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Coupon Rate (%)
          </label>
          <input
            type="number"
            name="couponRate"
            value={formData.couponRate}
            onChange={handleChange}
            placeholder="Enter Coupon Rate"
            className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Principal Amount
          </label>
          <input
            type="number"
            name="principal"
            value={formData.principal}
            onChange={handleChange}
            placeholder="Enter Principal Amount"
            className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Yield To Maturity
          </label>
          <input
            type="number"
            name="yieldToMaturity"
            value={formData.yieldToMaturity}
            onChange={handleChange}
            placeholder="Enter Yield to Maturity"
            className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Interest Earned
          </label>
          <input
            type="number"
            name="interestEarned"
            value={formData.interestEarned}
            onChange={handleChange}
            placeholder="Enter Interest earned"
            className="w-full px-4 py-3 rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-shadow"
          />
        </div>
      </form>
    </div>
  );
};

export default BondsForm;
