import { Link } from "react-router-dom";
import { TrendingUp, Shield, Brain, BarChart as ChartBar } from "lucide-react";

const features = [
  {
    icon: <TrendingUp className="h-6 w-6 text-white" />,
    title: "Investment Strategy Building",
    description:
      "Personalized investment strategies based on risk tolerance.",
  },
  {
    icon: <Shield className="h-6 w-6 text-white" />,
    title: "Smart Portfolio Management",
    description:
      "Personal suggestions for handling and optimizing your portfolio",
  },
  {
    icon: <Brain className="h-6 w-6 text-white" />,
    title: "AI-powered assistance",
    description:
      "AI Agent Market Analysis for stocks of sectors and advice assistant.",
  },
  {
    icon: <ChartBar className="h-6 w-6 text-white" />,
    title: "Market Analysis",
    description:
      "Stay ahead with AI-powered analysis of Indian stock market trends and predictions.",
  },
];

const Home = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative bg-white overflow-hidden">
        <div className="max-w-7xl mx-auto">
          <div className="relative z-10 pb-8 bg-white sm:pb-16 md:pb-20 lg:max-w-2xl lg:w-full lg:pb-28 xl:pb-32">
            <main className="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28">
              <div className="sm:text-center lg:text-left">
                <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                  <span className="block">AI-Driven Financial Insights:</span>
                  <span className="block text-primary-600">
                    Accurate, Reliable, and Data-Powered Reports!
                  </span>
                </h1>
                <p className="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                  Leverage AI-powered financial narrative generation with
                  probabilistic consistency. Analyze market trends, historical
                  data, and real-time insights to produce coherent, data-driven
                  reports, reducing misinformation and enhancing investment
                  decision-making for financial firms.
                </p>
                <div className="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                  <div className="rounded-md shadow">
                    <Link
                      to="/sign-up"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 md:py-4 md:text-lg md:px-10"
                    >
                      Get Started
                    </Link>
                  </div>
                  <div className="mt-3 sm:mt-0 sm:ml-3">
                    <Link
                      to="/portfolio/learn"
                      className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-700 bg-primary-100 hover:bg-primary-200 md:py-4 md:text-lg md:px-10"
                    >
                      Learn More
                    </Link>
                  </div>
                </div>
              </div>
            </main>
          </div>
        </div>
        <div className="lg:absolute lg:inset-y-0 lg:right-0 lg:w-1/2">
          <img
            className="h-56 w-full object-cover sm:h-72 md:h-96 lg:w-full lg:h-full"
            src="https://images.unsplash.com/photo-1551434678-e076c223a692?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2850&q=80"
            alt="Analytics Dashboard"
          />
        </div>
      </div>

      {/* Features Section */}
      <div className="py-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
              Powerful Features for Smart Investing
            </h2>
            <p className="mt-4 max-w-2xl text-xl text-gray-500 mx-auto">
              Everything you need to make informed investment decisions and grow
              your wealth.
            </p>
          </div>

          <div className="mt-10">
            <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {features.map((feature, index) => (
                <div key={index} className="pt-6">
                  <div className="flow-root bg-white rounded-lg px-6 pb-8">
                    <div className="-mt-6">
                      <div className="inline-flex items-center justify-center p-3 bg-primary-500 rounded-md shadow-lg">
                        {feature.icon}
                      </div>
                      <h3 className="mt-8 text-lg font-medium text-gray-900 tracking-tight">
                        {feature.title}
                      </h3>
                      <p className="mt-5 text-base text-gray-500">
                        {feature.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
