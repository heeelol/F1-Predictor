import React from 'react'

export default function RaceForm() {
    return (
        <section className="flex flex-col items-center justify-center h-20 bg-red-500 rounded-lg shadow-md p-15">
            <label className="font-bold scale-150">Select Race:</label>
            <select className="mt-2 bg-white border border-gray-300 rounded-lg p-2 hover:shadow-lg">
                <option>Race 1</option>
                <option>Race 2</option>
                <option>Race 3</option>
            </select>
        </section>
    )
}