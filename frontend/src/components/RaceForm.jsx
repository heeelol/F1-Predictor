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
                        <option value="bahrain">Bahrain Grand Prix</option>
                        <option value="saudi_arabia">Saudi Arabian Grand Prix</option>
                        <option value="australia">Australian Grand Prix</option>
                        <option value="japan">Japanese Grand Prix</option>
                        <option value="china">Chinese Grand Prix</option>
                        <option value="miami">Miami Grand Prix</option>
                        <option value="emilia_romagna">Emilia Romagna Grand Prix</option>
                        <option value="monaco">Monaco Grand Prix</option>
                        <option value="canada">Canadian Grand Prix</option>
                        <option value="spain">Spanish Grand Prix</option>
                        <option value="austria">Austrian Grand Prix</option>
                        <option value="great_britain">British Grand Prix</option>
                        <option value="hungary">Hungarian Grand Prix</option>
                        <option value="belgium">Belgian Grand Prix</option>
                        <option value="netherlands">Dutch Grand Prix</option>
                        <option value="italy">Italian Grand Prix</option>
                        <option value="azerbaijan">Azerbaijan Grand Prix</option>
                        <option value="singapore">Singapore Grand Prix</option>
                        <option value="usa">United States Grand Prix (Austin)</option>
                        <option value="mexico">Mexican Grand Prix</option>
                        <option value="brazil">Brazilian Grand Prix</option>
                        <option value="las_vegas">Las Vegas Grand Prix</option>
                        <option value="qatar">Qatar Grand Prix</option>
                        <option value="abu_dhabi">Abu Dhabi Grand Prix</option>
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