import { Link, useLocation } from "react-router-dom";
import {
  BarChart2,
  BookOpen,
  TrendingUp,
  User,
  LineChart,
  LayoutDashboard,
  BriefcaseBusiness,
  MessageSquare,
  Newspaper,
  Calculator,
  HelpCircle,
  Brain,
} from "lucide-react";
import { useUser } from "@clerk/clerk-react";
import { useTour } from "../context/TourContext";
import { Logo } from "../../public/images";

const Sidebar = () => {
  const location = useLocation();
  const { user } = useUser();
  const { openTour } = useTour();

  const menuItems = [
    {
      path: "/dashboard",
      icon: LayoutDashboard,
      label: "Dashboard",
      tourClass: "tour-dashboard",
    },
    {
      path: "/portfolio/my-portfolio",
      icon: BriefcaseBusiness,
      label: "My Portfolio",
      tourClass: "tour-portfolio",
    },
    {
      path: "/portfolio/recommendations",
      icon: TrendingUp,
      label: "Recommendations",
      tourClass: "tour-recommendations",
    },
    {
      path: "/portfolio/learn",
      icon: BookOpen,
      label: "Reports & Insights",
      tourClass: "tour-learn",
    },
    {
      path: "/portfolio/financial-path",
      icon: BarChart2,
      label: "Financial Path",
      tourClass: "tour-financial-path",
    },
    {
      path: "/portfolio/money-calc",
      icon: Calculator,
      label: "Asset Growth Calculator",
      tourClass: "tour-money-calc",
    },
    {
      path: "/portfolio/chatbot",
      icon: MessageSquare,
      label: "AI Assistant",
      tourClass: "tour-ai-assistant",
    },
    {
      path: "/portfolio/money-pulse",
      icon: Newspaper,
      label: "Financial Insights Hub",
      tourClass: "tour-money-pulse",
    },
    {
      path: "/portfolio/stock-analyzer",
      icon: LineChart,
      label: "Stock Analyzer",
      tourClass: "tour-stock-analyzer",
    },
    {
      path: "/portfolio/agents",
      icon: Brain,
      label: "Market Analysis Agents",
      tourClass: "tour-agents",
    },
  ];

  return (
    <div className="fixed left-0 top-0 h-screen w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
      <div className="flex flex-col h-full">
        <div className="p-4">
          <Link to="/" className="flex items-center tour-logo">
            <img src={Logo} alt="Logo" className="h-8 w-auto" />
            <span className="ml-2 text-xl font-bold text-gray-900 dark:text-white">
              Verity Finance
            </span>
          </Link>
        </div>

        <nav className="flex-1 p-4">
          <ul className="space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <li key={item.path}>
                  <Link
                    to={item.path}
                    className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                      isActive
                        ? "bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400"
                        : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                    } ${item.tourClass}`}
                  >
                    <Icon className="h-5 w-5 mr-3" />
                    <span className="font-medium">{item.label}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* User Profile Section */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <Link
            to="/portfolio/profile"
            className="flex items-center space-x-3 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors p-2 rounded-lg group tour-profile"
          >
            {user?.imageUrl ? (
              <img
                src={user.imageUrl}
                alt="Profile"
                className="h-10 w-10 rounded-full object-cover ring-2 ring-primary-500 dark:ring-primary-400"
              />
            ) : (
              <div className="h-10 w-10 rounded-full bg-primary-100 dark:bg-primary-900/50 flex items-center justify-center">
                <User className="h-5 w-5 text-primary-600 dark:text-primary-400" />
              </div>
            )}
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 dark:text-white truncate group-hover:text-primary-600 dark:group-hover:text-primary-400">
                {user?.fullName || "User Name"}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                {user?.primaryEmailAddress?.emailAddress || "email@example.com"}
              </p>
            </div>
          </Link>

          {/* Tutorial Button */}
          <button
            onClick={openTour}
            className="mt-4 w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-primary-600 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20 rounded-lg hover:bg-primary-100 dark:hover:bg-primary-900/30 transition-colors"
          >
            <HelpCircle className="h-4 w-4 mr-2" />
            Take a Tour
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
