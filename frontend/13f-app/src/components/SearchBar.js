import React, { useState } from 'react'
// import { Link } from 'react-router-dom'
import './SearchBar.css'
import './Button.css'
import { InputGroup, Form, Button } from 'react-bootstrap'
import { useHistory, useLocation } from 'react-router-dom'

function SearchBar () {
  const location = useLocation()
  const params = new URLSearchParams(location.search)
  const searchParam = params.get('q') || ''
  const startDateParam = params.get('startDate') || ''
  const endDateParam = params.get('endDate') || ''

  const [searchName, setSearchName] = useState(searchParam)
  const [searchStartDate, setSearchStartDate] = useState(startDateParam)
  const [searchEndDate, setSearchEndDate] = useState(endDateParam)
  const handleNameChange = event => { setSearchName(event.target.value) }
  const handleStartDateChange = event => { console.log(event.target.value); setSearchStartDate(event.target.value) }
  const handleEndDateChange = event => { setSearchEndDate(event.target.value) }
  const searchLink = `/search?q=${searchName}&start_date=${searchStartDate}&end_date=${searchEndDate}`

  const history = useHistory()
  const onSubmit = (event) => {
    event.preventDefault()
    history.push(searchLink, { replace: true })
  }

  return (
          <>
                <Form onSubmit={onSubmit}>
                    <InputGroup>
                      <Form.Control value={searchName} onChange={handleNameChange} placeholder='Company Name' />
                      <Form.Control type="date" value={searchStartDate} onChange={handleStartDateChange} />
                      <Form.Control type="date" value={searchEndDate} onChange={handleEndDateChange} />
                      <Button variant="primary" href={searchLink} type='submit' onClick={onSubmit}><i className="bi bi-search"></i></Button>
                    </InputGroup>
                </Form>
          </>)
}

export default SearchBar
