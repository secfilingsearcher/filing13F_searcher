import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import './Button.css'

const date = new Date()
const today = date.toISOString().substr(0, 10)

function SearchBar () {
  const [searchName, setSearchName] = useState('')
  const [searchStartDate, setSearchStartDate] = useState(today)
  const [searchEndDate, setSearchEndDate] = useState(today)
  const handleNameChange = event => { setSearchName(event.target.value) }
  const handleStartDateChange = event => { setSearchStartDate(event.target.value) }
  const handleEndDateChange = event => { setSearchEndDate(event.target.value) }
  const searchLink = `/search?q=${searchName}&startDate=${searchStartDate}&endDate=${searchEndDate}`
  return (
          <>
                <form>
                  <div>
                    <input type='text' placeholder='Company Name' className='search' value={searchName} onChange={handleNameChange}></input>
                    <input type='date' className='date' value={searchStartDate} onChange={handleStartDateChange}></input>
                    <input type='date' className='date' value={searchEndDate} onChange={handleEndDateChange}></input>
                    <Link to={searchLink}><button className="bar_button" type="submit">SEARCH</button></Link>
                  </div>
                </form>
          </>)
}

export default SearchBar