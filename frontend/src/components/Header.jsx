import React from 'react'
import logo from '../assets/f1Logo.png'
import gif from '../assets/GStQ.gif'

export default function Header() {
    return (
        <>
            <header>
                <div className="relative h-30 bg-zinc-900 flex items-center justify-center rounded-lg">
                    <div className="relative left-30 flex items-center justify-center text-red-500 text-6xl font-bold ">
                        F1 Predictor
                    </div>
                    <div className="relative top-0 right-150 w-50 h-50 flex items-center justify-center hover:scale-105">
                        <img src={logo} />
                    </div>
                </div>
            </header>

            <div className="flex items-center justify-center mt-4 h-50">
                <img src={gif} alt="loading..." />
            </div>
        </>
    )
}

