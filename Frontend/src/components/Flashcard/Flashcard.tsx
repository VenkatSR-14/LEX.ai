// FlashCard.tsx
import './FlashCard.scss';
import { useState } from 'react';
import FileUpload from './FileUpload';
import axios from 'axios';
import JSZip from 'jszip';
import * as pdfjsLib from 'pdfjs-dist/build/pdf';

pdfjsLib.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.js`;

async function extractTextFromPptx(arrayBuffer: ArrayBuffer): Promise<string> {
  const zip = await JSZip.loadAsync(arrayBuffer);
  let textContent = "";
  const slideFiles = Object.keys(zip.files).filter(filename => filename.startsWith("ppt/slides/slide"));
  for (const slideFile of slideFiles) {
    const fileData = await zip.file(slideFile)?.async("string");
    if (fileData) {
      const regex = /<a:t>(.*?)<\/a:t>/g;
      let match;
      while ((match = regex.exec(fileData)) !== null) {
        textContent += match[1] + " ";
      }
    }
  }
  return textContent;
}

async function extractTextFromPdf(file: File): Promise<string> {
  const arrayBuffer = await file.arrayBuffer();
  const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
  let textContent = "";
  for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
    const page = await pdf.getPage(pageNum);
    const content = await page.getTextContent();
    const strings = content.items.map((item: any) => item.str);
    textContent += strings.join(" ") + "\n";
  }
  return textContent;
}


function FlashCard() {
  const openaiKey = import.meta.env.VITE_OPEN_AI_KEY;;
  const [file, setFile] = useState<File | null>(null);
  const [studyCards, setStudyCards] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (file: File) => {
    setFile(file);
    setMessage(`Selected file: ${file.name}`);
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file first.');
      return;
    }

    let extractedContent = "";
    setIsLoading(true);
    setMessage('Generating study cards...');

    try {
      if (file.type === "application/pdf" || file.name.endsWith(".pdf")) {
        extractedContent = await extractTextFromPdf(file);
      } else if (
        file.type === "application/vnd.openxmlformats-officedocument.presentationml.presentation" ||
        file.name.endsWith(".pptx")
      ) {
        extractedContent = await extractTextFromPptx(await file.arrayBuffer());
      } else if (file.type.startsWith('text/')) {
        extractedContent = await file.text();
      } else {
        setMessage("Unsupported file type.");
        setIsLoading(false);
        return;
      }
    } catch (err) {
      setMessage("Error extracting file content.");
      setIsLoading(false);
      return;
    }

    const maxCharacters = 2000;
    if (extractedContent.length > maxCharacters) {
      extractedContent = extractedContent.slice(0, maxCharacters) + "\n... [truncated]";
    }

    const prompt = `Based solely on the file content provided below, generate exactly 5 study cards in a strict question-and-answer format. Do not include any extra commentary or text beyond the study cards.\n\nStudy Card 1:\nQ: [Question derived from the content]\nA: [Answer derived from the content]\n\n...\n\nFile Content:\n${extractedContent}`;

    try {
      const response = await axios.post(
        'https://api.openai.com/v1/chat/completions',
        {
          model: 'gpt-3.5-turbo',
          messages: [{ role: 'user', content: prompt }],
        },
        {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${openaiKey}`,
          },
        }
      );
      setStudyCards(response.data.choices[0].message.content);
      setMessage('Study cards generated!');
    } catch (err) {
      setMessage('Failed to generate study cards.');
    } finally {
      setIsLoading(false);
    }
  };

  const cards = studyCards
    .split(/Study Card \d+:/)
    .slice(1)
    .map((card, idx) => {
      const questionMatch = card.match(/Q:\s*(.*?)\s*A:/s);
      const answerMatch = card.match(/A:\s*(.*)/s);
      return {
        question: questionMatch ? questionMatch[1].trim() : '',
        answer: answerMatch ? answerMatch[1].trim() : '',
        id: idx,
      };
    });

  return (
    <div className="flashcard-container">
      <div className="left">
        <h1>AI Flashcard Generator</h1>
        <p>
          Upload PDFs, presentations, notes, images, and more.<br />
          Generate a comprehensive deck of flashcards in seconds.
        </p>
        <div className="cards">
          {cards.map(({ question, answer, id }) => (
            <div className="flashcard" key={id}>
              <div className="flashcard-inner">
                <div className="flashcard-front">
                  <p>{question}</p>
                </div>
                <div className="flashcard-back">
                  <p>{answer}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="right">
        <FileUpload onFileChange={handleFileChange} onUpload={handleUpload} />
        {file && <p className="file-name">📎 {file.name}</p>}
        <p className="supported">Supported Files:</p>
        <div className="file-icons">
          <span>📄</span><span>🧾</span><span>📘</span><span>📥</span>
        </div>
        <hr />
        <p className="or">or try</p>
        <div className="sources">
          <button className="source-btn">🎥 YouTube</button>
          <button className="source-btn">🌐 Wikipedia</button>
        </div>
        {message && <p className="message">{message}</p>}
        {isLoading && <div className="loader">Generating...</div>}
      </div>
    </div>
  );
}

export default FlashCard;
