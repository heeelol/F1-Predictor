import './App.css'
import Header from './components/Header'
import RaceForm from './components/RaceForm'
import PredictButton from './components/PredictButton'
import PredictionTable from './components/PredictionTable'

function App() {
  return (
    <div className="relative min-h-screen bg-gradient-to-b from-red-600 to-neutral-300">
      <Header />
      <RaceForm />
      <PredictButton />
      <PredictionTable />
    </div>
  )
 
}

export default App
