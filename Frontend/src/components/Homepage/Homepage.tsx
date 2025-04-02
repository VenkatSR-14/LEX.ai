import Footer from '../Common/Footer';
import Navbar from '../Common/Navbar';
import Content from './Content';
import './Homepage.scss';
import Modal from './Modal';
import { RootState } from '../../store';
import { useSelector } from 'react-redux';
import { isTokenExpired } from '../../middleware/tokenExpired';
import { useEffect } from 'react';

function Homepage() {
  const modalState = useSelector((state: RootState) => state.counter.value);
  const token = localStorage.getItem('usertoken');
  const showModal = modalState && (!token || isTokenExpired(token));

  useEffect(() => {
    document.body.style.overflow = showModal ? 'hidden' : 'auto';
    return () => {
      document.body.style.overflow = 'auto';
    };
  }, [showModal]);
  

  return (
    <div className="homepage">
      <Navbar />
      <Content />
      {showModal && <Modal />}
      <Footer />
    </div>
  );
}

export default Homepage;
