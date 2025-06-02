import { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) {
            // Auto-login if token exists
            const storedName = localStorage.getItem("userName");
            if (storedName) {
                setUser({ name: storedName });
            }
        }
    }, []);

    const login = (token, name) => {
        localStorage.setItem("token", token);
        localStorage.setItem("userName", name);
        setUser({ name });
    };

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("userName");
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};
