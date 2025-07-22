import { useState } from "react";
import axios from 'axios'


export default function RaceForm( {onPredictionReceived} ) {

    const [data, setData] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const handleRaceChange = (e) => {
        setData(e.target.value)
    }

    const predict = async () => {
        if (!data) return
        
        setLoading(true)
        setError(null)
        
        try {
            const response = await axios.post('/predict', {
                race: data
            })
            
          
            const transformedData = response.data.rankings.map(item => ({
                pos: item.position,
                driver: item.driver,
                team: item.team || 'Unknown', 
                points: getPointsForPosition(item.position)
            }))
            
            onPredictionReceived(transformedData)
            
        } catch (err) {
            setError('Failed to get prediction. Please try again.')
            console.error('Prediction error:', err)
        } finally {
            setLoading(false)
        }
    }

    const getPointsForPosition = (position) => {
        const pointsMap = {
            1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
            6: 8, 7: 6, 8: 4, 9: 2, 10: 1
        }
        return pointsMap[position] || 0
    }

    return (
        <>
            <section className="flex flex-col items-center justify-center bg-red-500 rounded-xl shadow-md p-6 w-full max-w-md mx-auto mb-6 space-y-4">
                <h3 className="text-white font-bold text-xl">Select Race Details</h3>

                <div className="flex flex-col w-full">
                    <label htmlFor="race" className="text-white font-semibold mb-1">Race</label>
                    <select 
                        id="race" 
                        value={data}
                        onChange={handleRaceChange}
                        className="rounded-lg p-2 border border-gray-300 bg-white hover:shadow-lg"
                    >
                        
                        <option value="">-- Select a Race --</option>
                        <option value="1">Australian Grand Prix</option>
                        <option value="2">Chinese Grand Prix</option>
                        <option value="3">Japanese Grand Prix</option>
                        <option value="4">Bahrain Grand Prix</option>
                        <option value="5">Saudi Arabian Grand Prix</option>
                        <option value="6">Miami Grand Prix</option>
                        <option value="7">Emilia Romagna Grand Prix</option>
                        <option value="8">Monaco Grand Prix</option>
                        <option value="9">Spanish Grand Prix</option>
                        <option value="10">Canadian Grand Prix</option>
                        <option value="11">Austrian Grand Prix</option>
                        <option value="12">British Grand Prix</option>
                        <option value="13">Belgian Grand Prix</option>
                        <option value="14">Hungarian Grand Prix</option>
                        <option value="15">Dutch Grand Prix</option>
                        <option value="16">Italian Grand Prix</option>
                        <option value="17">Azerbaijan Grand Prix</option>
                        <option value="18">Singapore Grand Prix</option>
                        <option value="19">United States Grand Prix (Austin)</option>
                        <option value="20">Mexican Grand Prix</option>
                        <option value="21">Brazilian Grand Prix</option>
                        <option value="22">Las Vegas Grand Prix</option>
                        <option value="23">Qatar Grand Prix</option>
                        <option value="24">Abu Dhabi Grand Prix</option>
                    </select>
                </div>
            </section>

            <section className="bg-red-700 scale-150 rounded-lg shadow-md hover:bg-red-600 flex items-center justify-center">
                <button 
                    onClick={predict} 
                    disabled={!data || loading}
                    className="scale-75 text-white font-light disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {loading ? 'Predicting...' : 'Predict Ranking'}
                </button>
            </section>

            {error && (
                <section className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded max-w-md mx-auto mt-4">
                    {error}
                </section>
            )}
        </>
  );
    
}