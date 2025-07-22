import React from "react";

export default function Instruction() {
    return (
      <div className="bg-white shadow-md rounded-2xl p-6 mb-6 max-w-3xl mx-auto text-gray-800 z-1">
        <h2 className="text-2xl font-bold mb-4 text-center">
            🏎️ Welcome to the F1 Race Predictor!
        </h2>

        <p className="mb-4 text-center">
            Enter a <span className="font-semibold text-blue-600">race</span> to predict the final race standings based on qualifying data in <span className="font-semibold text-blue-600">2025</span> and a trained machine learning model.
        </p>

        <ul className="list-disc list-inside space-y-1 text-center sm:text-left">
            <li>📅 Supports recent F1 seasons</li>
            <li>🗺️ Choose a Grand Prix like Bahrain or Silverstone</li>
            <li>🧠 ML-based predictions using historical patterns</li>
        </ul>
    </div>
  );
}