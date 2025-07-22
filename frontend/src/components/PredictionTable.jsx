import {useEffect, useState} from 'react'
import axios from 'axios'


// Sample data to be replaced with backend
const sampleData = [
  { pos: 1, driver: 'Lewis Hamilton', team: 'Mercedes', points: 25 },
  { pos: 2, driver: 'Max Verstappen', team: 'Red Bull', points: 18 },
  { pos: 3, driver: 'Charles Leclerc', team: 'Ferrari', points: 15 },
]



export default function PredictionTable({ data }) {

  const teamColors = {
    "Mercedes": "text-cyan-300",
    "Red Bull": "text-blue-400",
    "Ferrari": "text-red-400",
    "McLaren": "text-orange-500",
    "Alpine": "text-blue-500",
    "Aston Martin": "text-green-500",
    "Racing Bulls": "text-blue-300",
    "Haas": "text-gray-500",
    "Williams": "text-blue-700",
    "Kick Sauber": "text-green-300",
}

  return (
    <div className="p-6 sm:p-10">
      <h1 className="font-serif text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-red-400 via-red-500 to-stone-500 mb-12 drop-shadow-2xl tracking-wide text-center">
        Prediction Results
      </h1>

      <div className="overflow-x-auto min-w-4xl rounded-2xl shadow-2xl border border-stone-700 bg-black bg-opacity-60 backdrop-blur-md">
        <table className="w-full text-left text-white text-lg sm:text-xl">
          <thead className="bg-stone-800 text-red-300 uppercase tracking-wider">
            <tr>
              <th className="px-6 py-4 border-b border-stone-700">Position</th>
              <th className="px-6 py-4 border-b border-stone-700">Driver</th>
              <th className="px-6 py-4 border-b border-stone-700">Team</th>
              <th className="px-6 py-4 border-b border-stone-700">Points</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr
                key={item.pos}
                className={`${
                  index % 2 === 0 ? "bg-stone-800" : "bg-stone-700"
                } hover:bg-stone-600 transition-colors duration-200`}
              >
                <td className="px-6 py-4">{item.pos}</td>
                <td className="px-6 py-4">{item.driver}</td>
                <td className={`px-6 py-4 ${teamColors[item.team] || ''}`}>
                  {item.team}
                </td>
                <td className="px-6 py-4">{item.points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}