import React from 'react'

export default function PredictButton( {onClick} ) {
    return (
        <section>
            <button onClick={onClick}>Predict Ranking</button>
        </section>
    )
}