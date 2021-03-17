import React from 'react';
import '../App.css';
import { Button } from './Button';
import { SearchBox } from './SearchBox';
import './MainSection.css';

const divStyle = { float: 'left', padding: '20px', margin: '20px'};
const date = new Date();
const today = date.toISOString().substr(0, 10);

function SearchForm() {
    return (
        <>
            <SearchBox />
            <div style={divStyle}>
            <input type='date' className='date' defaultValue={today}></input>
            <input type='date' className='date' defaultValue={today}></input>
            </div>
            <Button buttonStyle='btn--outline' buttonSize='btn--large'>SEARCH</Button> 
        </>
    )
}

export default SearchForm
