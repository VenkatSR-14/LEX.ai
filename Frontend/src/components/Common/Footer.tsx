import './Footer.scss';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="footer-brand">
          <img src="/logo.png" alt="LEX Logo" className="logo" />
          <h3>LEX</h3>
          <p>Subscribe to our newsletter</p>
          <form className="newsletter">
            <input type="email" placeholder="Enter your email" />
            <button type="submit">Subscribe</button>
          </form>
        </div>

        <div className="footer-links">
          <div className="column">
            <h4>Product</h4>
            <ul>
              <li>Features</li>
              <li>Pricing</li>
            </ul>
          </div>
          <div className="column">
            <h4>Resources</h4>
            <ul>
              <li>Blog</li>
              <li>User Guides</li>
              <li>Webinars</li>
            </ul>
          </div>
          <div className="column">
            <h4>Company</h4>
            <ul>
              <li>About</li>
              <li>Contact Us</li>
            </ul>
          </div>
          <div className="column">
            <h4>Plans & Pricing</h4>
            <ul>
              <li>Personal</li>
              <li>Startup</li>
              <li>Organization</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="footer-bottom">
        <select className="language">
          <option>English</option>
        </select>
        <p>© 2024 Brand, Inc. · Privacy · Terms · Sitemap</p>
        <div className="social-icons">
          <span>🌐</span>
          <span>🐦</span>
          <span>📘</span>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
