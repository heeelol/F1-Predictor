import React from 'react'

//to be replaced with data from backend
const sampleData = [
    {pos: 1, driver: 'Lewis Hamilton', team: 'Mercedes', points: 25},
    {pos: 2, driver: 'Max Verstappen', team: 'Red Bull', points: 18},
    {pos: 3, driver: 'Charles Leclerc', team: 'Ferrari', points: 15},
]

export default function PredictionTable( { data = sampleData }) {
    return (
        <section>
            <h2>Prediction Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Position</th>
                        <th>Driver</th>
                        <th>Team</th>
                        <th>Points</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item) => (
                        <tr key={item.pos}>
                            <td>{item.pos}</td>
                            <td>{item.driver}</td>
                            <td>{item.team}</td>
                            <td>{item.points}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </section>
    )
}