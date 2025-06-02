import React, { useState, useContext } from "react";
import ReCAPTCHA from "react-google-recaptcha";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { AuthContext } from "../context/AuthContext";
import "../styles/login.css";

const Login = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({ email: "", password: "" });
  const [recaptchaValue, setRecaptchaValue] = useState(null);
  const [isFormValid, setIsFormValid] = useState(false);
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  // Email regex pattern
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  // Password regex pattern (Min 8 chars, 1 uppercase, 1 number, 1 special char)
  const passwordPattern = /^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

  const validateInput = (name, value) => {
    let errorMessage = "";
    if (name === "email" && !emailPattern.test(value)) {
      errorMessage = "Invalid email format!";
    }
    if (name === "password" && !passwordPattern.test(value)) {
      errorMessage = "Password must be at least 8 characters, contain 1 uppercase, 1 number, and 1 special character!";
    }
    setErrors((prevErrors) => ({ ...prevErrors, [name]: errorMessage }));
    setIsFormValid(emailPattern.test(formData.email) && passwordPattern.test(formData.password));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    validateInput(name, value);
  };

  const handleRecaptcha = (value) => setRecaptchaValue(value);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!recaptchaValue) {
      alert("Please verify the reCAPTCHA!");
      return;
    }
    if (!isFormValid) {
      alert("Please fix validation errors before submitting.");
      return;
    }
    try {
      const res = await axios.post("http://localhost:5000/login", formData);
      login(res.data.access_token, res.data.name);
      navigate("/dashboard");
    } catch (error) {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Login</h2>
        <form className="login-form" onSubmit={handleSubmit}>
          <input type="email" name="email" placeholder="Email Address" value={formData.email} onChange={handleChange} required />
          {errors.email && <p className="error-text">{errors.email}</p>}
          <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
          {errors.password && <p className="error-text">{errors.password}</p>}
          <div className="recaptcha-container">
            <ReCAPTCHA sitekey="6LcS1dgqAAAAAF35MuCR273nNw3yVx8f7K6PjgNT" onChange={handleRecaptcha} />
          </div>
          <button type="submit" className="login-btn" disabled={!isFormValid}>Login</button>
        </form>
        <p className="register-link">Don't have an account? <Link to="/Register">Register here</Link></p>
      </div>
    </div>
  );
};

export default Login;
