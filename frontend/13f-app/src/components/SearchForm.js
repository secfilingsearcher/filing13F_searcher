import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import '../App.css'
import './Button.css'
import './MainSection.css'

const divStyle = { float: 'left', padding: '20px', margin: '20px' }
const date = new Date()
const today = date.toISOString().substr(0, 10)

function SearchForm () {
  const [searchName, setSearchName] = useState('')
  const [searchStartDate, setSearchStartDate] = useState(today)
  const [searchEndDate, setSearchEndDate] = useState(today)
  const handleNameChange = event => { setSearchName(event.target.value) }
  const handleStartDateChange = event => { setSearchStartDate(event.target.value) }
  const handleEndDateChange = event => { setSearchEndDate(
  const searchLink = `/search?q=${searchName}&startDate=${searchStartDate}&endDate=${searchEndDate}`

  return (
        <>
              <form>
                <div style={divStyle}>
                  <input type='text' placeholder='Company Name' className='search' value={searchName} onChange={handleNameChange}></input>
                  <input type='date' className='date' value={searchStartDate} onChange={handleStartDateChange}></input>
                  <input type='date' className='date' value={searchEndDate} onChange={handleEndDateChange}></input>
                </div>
                <Link to={searchLink}><button className="button" type="submit">SEARCH</button></Link>
              </form>
        </>
  )
}

export default SearchForm
