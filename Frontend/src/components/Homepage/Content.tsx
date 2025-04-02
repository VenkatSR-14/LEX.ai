import './Content.scss';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { update } from '../../Slices/loginSlice';
import Testimonial from './Testimonial';
import GettingStarted from './GettingStarted';

function Content() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleNavigation = () => {
    const token = localStorage.getItem("usertoken");
    if (!token) {
      dispatch(update());
    } else {
      navigate("/flashcard");
    }
  };

  return (
    <section className="cta-section">
      <section className="hero">
        <h1>Unlock Your Learning Potential</h1>
        <p>Discover new skills and knowledge to achieve your goals.</p>
        <button className="get-started">Get Started</button>
      </section>

      <section className="features">
        <h2>Features</h2>
        <div className="feature-grid">
          <div className="feature-box">
            <div className="feature-icon blue"></div>
            <h4>Document Upload</h4>
            <p className="sub">File Management</p>
            <p className="desc">Easily upload documents to create personalized study material.</p>
            <span className="arrow">←</span>
          </div>
          <div className="feature-box">
            <div className="feature-icon green">
              <img src="" alt="" />
            </div>
            <h4>Flashcard Creation</h4>
            <p className="sub">Study Tools</p>
            <p className="desc">Transform your notes into interactive flashcards for efficient learning.</p>
            <span className="arrow" onClick={handleNavigation}>← Generate Flash Cards</span>
          </div>
          <div className="feature-box">
            <div className="feature-icon pink"></div>
            <h4>Progress Tracking</h4>
            <p className="sub">Performance Insights</p>
            <p className="desc">Monitor your learning progress with detailed analytics and reports.</p>
            <span className="arrow">←</span>
          </div>
        </div>
        <button className="explore">Explore Features</button>
      </section>

      <GettingStarted />
      <Testimonial />
    </section>
  );
}

export default Content;
