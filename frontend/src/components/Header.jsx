import React from 'react'
import logo from '../assets/f1Logo.png'


export default function Header() {
    return (
        <>
            <header>
                <div className="relative min-w-screen h-30 bg-zinc-900 flex items-center justify-center rounded-lg shadow-xl z-1">
                    <div className="relative left-30 flex items-center justify-center text-red-500 text-6xl font-extrabold font-serif">
                        F1 Predictor
                    </div>
                    <div className="relative top-0 right-150 w-50 h-50 flex items-center justify-center animate-pulse">
                        <img src={logo} />
                    </div>
                </div>
            </header>
        </>
    )
}

