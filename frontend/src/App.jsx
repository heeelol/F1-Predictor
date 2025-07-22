import './App.css'
import { useState } from 'react'
import axios from 'axios'
import Header from './components/Header'
import Instruction from './components/Instruction'
import RaceForm from './components/RaceForm'
import PredictionTable from './components/PredictionTable'

axios.defaults.baseURL = 'http://localhost:5000';

function App() {
  const [predictionData, setPredictionData] = useState(null);

  const handlePredictionReceived = (data) => {
        setPredictionData(data);
    };

  return (
    <div className="relative min-h-screen bg-gradient-to-b from-red-600 to-neutral-300 flex flex-col items-center">
      <Header />
      <Instruction />
      <RaceForm onPredictionReceived={handlePredictionReceived} />
      {predictionData && (
                    <PredictionTable data={predictionData} />
                )}
    </div>
  )
 
}

export default App
