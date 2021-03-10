import React from 'react';
import '../App.css';
import { Button } from './Button';
import SearchBox from './SearchBox';
import './MainSection.css';

function MainSection() {
    return (
        <>
            <div className='main-container'>
                <h1>COMPANY FINANCIAL HOLDINGS</h1>
                <p>Search 13F Filings by Company Name and Date</p>
                <SearchBox />
                <input type='date'/>
                <Button buttonStyle='btn--outline' buttonSize='btn--large'>SEARCH</Button>     
            </div>
                     
        </>
    )
}
 
 export default MainSection
