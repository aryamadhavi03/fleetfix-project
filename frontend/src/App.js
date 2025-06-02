import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import GoogleMapComponent from "./components/GoogleMapComponent";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import NearbyGarages from "./pages/NearbyGarages";
import VehicleManagement from "./pages/VehicleManagement";
import VehicleMaintenance from "./pages/VehicleMaintenance";
import { AuthProvider } from "./context/AuthContext";

function App() {
  return (
    <AuthProvider>
      <Router>
        <ToastContainer position="top-right" autoClose={3000} />
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
          <Routes>
            {/* Home (Dashboard) */}
            <Route path="/" element={<Dashboard />} />
            <Route path="/dashboard" element={<Dashboard />} />  

            {/* Authentication Routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/nearby-garages" element={<NearbyGarages />} />
            <Route path="/vehicle-management" element={<VehicleManagement />} />
            <Route path="/vehicle-maintenance" element={<VehicleMaintenance />} />
            <Route path="/nearby-garages" element={<NearbyGarages />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
