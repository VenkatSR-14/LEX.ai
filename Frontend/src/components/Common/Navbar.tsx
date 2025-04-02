import './Navbar.scss';
import { useDispatch } from 'react-redux';
import { AppDispatch } from '../../store';
import { update } from '../../Slices/loginSlice';
import { useEffect, useState } from 'react';
import api from '../../middleware/api';

function Navbar() {
  const dispatch = useDispatch<AppDispatch>();
  const [userToken, setUserToken] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("usertoken");
    setUserToken(token);
  }, []);

  const handleLogout = async () => {
    const token = localStorage.getItem("usertoken");

    try {
      await api.post(
        "/logout",
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      localStorage.removeItem("usertoken");
      setUserToken(null);
      window.location.href = "/";
    } catch (error) {
      console.error("Logout failed:", error);
    }
  };

  return (
    <nav className="navbar">
      <div className="logo">LEX</div>
      <ul className="nav-links">
        <li>Features</li>
        <li>About</li>
        <li>Blog</li>
        {userToken ? (
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        ) : (
          <button className="login-btn" onClick={() => dispatch(update())}>Login</button>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;