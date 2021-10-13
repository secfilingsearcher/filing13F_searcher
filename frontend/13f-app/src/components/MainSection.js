import React from 'react'
import '../App.css'

import SearchBar from './SearchBar.js'
import './MainSection.css'

function MainSection () {
  return (
        <>
            <div className='main-container'>
                <h1>COMPANY FINANCIAL HOLDINGS</h1>
                <p>Search 13F Filings by Company Name and Date</p>
                <SearchBar />
            </div>

        </>
  )
}

export default MainSection
