import React, { useContext, useState } from "react";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import "../styles/navbar.css";

function Navbar() {
  const { user, logout } = useContext(AuthContext);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  return (
    <nav className="navbar">
      <div className="logo">
        <Link to="/"><u>Fleet Fix ⛟</u></Link>
      </div>
      <ul className="nav-links">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/nearby-garages">Garages</Link></li>
        <li><Link to="/vehicle-maintenance">Prediction</Link></li>
        <li><Link to="/vehicle-management">Maintain</Link></li>

        {/* Show Profile Dropdown if User is Logged In, Otherwise Show Login Button */}
        {user ? (
          <li className="profile-dropdown">
            <div className="profile-icon" onClick={() => setDropdownOpen(!dropdownOpen)}>
              👤 {/* You can replace this with an actual profile icon */}
            </div>
            {dropdownOpen && (
              <div className="dropdown-menu">
                <p>{user.name}</p> {/* Display User's Name */}
                <button onClick={logout}>Logout</button>
              </div>
            )}
          </li>
        ) : (
          <li><Link to="/login" className="login-btn">Login</Link></li>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;
