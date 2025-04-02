import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Homepage from './components/Homepage/Homepage';
import Dashboard from './components/Dashboard/Dashboard';
import RouteTracker from './components/Common/RouteTracker'; 
import FlashCard from './components/Flashcard/Flashcard'; 

function App() {
  return (
    <BrowserRouter>
      <RouteTracker /> 
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/flashcard" element={<FlashCard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;