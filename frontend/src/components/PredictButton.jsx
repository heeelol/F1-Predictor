import React from 'react'

export default function PredictButton( {onClick} ) {
    return (
        <section>
            <button onClick={onClick} className="hover:bg-neutral-700" >Predict Ranking</button>
        </section>
    )
}