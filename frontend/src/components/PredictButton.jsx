import React from 'react'

export default function PredictButton( {onClick} ) {
    return (
        <section>
            <button onClick={onClick} className="bg-blue-500">Predict Ranking</button>
        </section>
    )
}