import React, { useState } from 'react'
// import { Link } from 'react-router-dom'
import './SearchBar.css'
import './Button.css'
import { InputGroup, FormControl, Button } from 'react-bootstrap'

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
                <form id="bar-search" onSubmit={() => { console.log('hello') }} >
                    <InputGroup>
                      <FormControl value={searchName} onChange={handleNameChange} placeholder='Company Name' />
                      <FormControl type="date" value={searchStartDate} onChange={handleStartDateChange} placeholder='Company Name' />
                      <FormControl type="date" value={searchEndDate} onChange={handleEndDateChange} placeholder='Company Name' />
                      <Button variant="primary" href={searchLink}><i className="bi bi-search"></i></Button>
                    </InputGroup>
                </form>
          </>)
}

export default SearchBar
