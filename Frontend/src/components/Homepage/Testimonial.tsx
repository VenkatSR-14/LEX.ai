import './Testimonial.scss';

function Testimonial() {
  return (
    <section className="testimonial">
      <div className="card">
        <img src="https://randomuser.me/api/portraits/women/44.jpg" alt="Emily Carter" className="avatar" />
        <div className="content">
          <div className="stars">★★★★★</div>
          <p className="quote">
            LEX has completely streamlined my workflow. I can't imagine going back to how I worked before.
          </p>
          <p className="author">Emily Carter</p>
          <p className="role">Product Manager at InnovateTech</p>
        </div>
      </div>
    </section>
  );
}

export default Testimonial;
