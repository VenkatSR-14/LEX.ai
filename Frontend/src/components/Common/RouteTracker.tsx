import { useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';

const RouteTracker = () => {
  const location = useLocation();
  const isFirstLoad = useRef(true);

  useEffect(() => {
    if (isFirstLoad.current) {
      isFirstLoad.current = false;
      return;
    }

    const { pathname } = location;
    const exclude = ['/', '/login', '/signup'];
    if (!exclude.includes(pathname)) {
      localStorage.setItem('lastVisited', pathname);
      console.log("✅ Stored:", pathname);
    }
  }, [location]);

  return null; 
};

export default RouteTracker;
