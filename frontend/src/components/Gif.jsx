import React from 'react'
import gif from '../assets/GStQ.gif'

export default function Gif() {
    return (
        <div className="absolute max-w-screen">
            <img className="opacity-10 min-w-screen min-h-screen h-auto w-auto z0" src={gif} alt="loading..." />
        </div>
    )
}