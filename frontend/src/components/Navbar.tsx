import { Link } from "react-router-dom";
import { useUser } from "@clerk/clerk-react";
import { Logo } from "../../public/images";

const Navbar = () => {
  const { isSignedIn } = useUser();

  return (
    <nav className="bg-white  shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              <img src={Logo} alt="Logo" className="h-8 w-auto" />
              <span className="ml-2 mt-1 text-2xl font-bold text-gray-900">
                Verity Finance
              </span>
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            {isSignedIn ? (
              <Link to="/dashboard" className="btn-primary">
                Go to Dashboard
              </Link>
            ) : (
              <>
                <Link to="/sign-in" className="btn-primary">
                  Sign In
                </Link>
                <Link to="/sign-up" className="btn-secondary">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
