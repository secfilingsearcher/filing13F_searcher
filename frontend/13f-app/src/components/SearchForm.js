import React, { useState } from 'react'
import '../App.css'
import { Button } from './Button'
import './MainSection.css'

const divStyle = { float: 'left', padding: '20px', margin: '20px' }
const date = new Date()
const today = date.toISOString().substr(0, 10)

function SearchForm () {
  const [searchName, setSearchName] = useState('')
  const handleClick = event => { setSearchName(event.target.value) }
  return (
        <>
              <div style={divStyle}>
                <input type='text' placeholder='Company Name' className='search' value={searchName}></input>
                <input type='date' className='date' defaultValue={today}></input>
                <input type='date' className='date' defaultValue={today}></input>
              </div>
              <Button buttonStyle='btn--outline' buttonSize='btn--large' onClick={handleClick}>SEARCH</Button>
        </>
  )
}

export default SearchForm
