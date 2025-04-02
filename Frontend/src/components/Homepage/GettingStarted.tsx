import './GettingStarted.scss';

function GettingStarted() {
  return (
    <section className="getting-started">
      <h2>Getting Started</h2>
      <ol className="steps">
        <li>
          <h4>01 Upload Your Document</h4>
          <p>Simply drag/drop any legal document you wish to analyze or press the blue button to select the file. LEX will parse your document in seconds.</p>
        </li>
        <li>
          <h4>02 Create Your Flashcards</h4>
          <p>LEX will intelligently propose key topics and allow you to review and approve before generating your custom flashcard set.</p>
        </li>
        <li>
          <h4>03 Train Your Model</h4>
          <p>Train your LEX model with a single click using various methods to enhance its understanding of your document.</p>
        </li>
        <li>
          <h4>04 Track Your Progress</h4>
          <p>Monitor your training and activity with detailed graphs and insights that showcase your study patterns over time.</p>
        </li>
      </ol>
    </section>
  );
}

export default GettingStarted;