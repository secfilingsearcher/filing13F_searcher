import React from 'react'
import '../App.css'

import SearchForm from './Search.js'
import './MainSection.css'

function MainSection () {
  return (
        <>
            <div className='main-container'>
                <h1>COMPANY FINANCIAL HOLDINGS</h1>
                <p>Search 13F Filings by Company Name and Date</p>
                <SearchForm />
            </div>

        </>
  )
}

export default MainSection
