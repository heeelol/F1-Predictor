import React from 'react'

export default function PredictButton( {onClick} ) {
    return (
        <section className="bg-red-700 scale-150 rounded-lg shadow-md hover:bg-red-600 flex items-center justify-center">
            <button onClick={onClick} className="scale-75 text-white font-light">Predict Ranking</button>
        </section>
    )
}