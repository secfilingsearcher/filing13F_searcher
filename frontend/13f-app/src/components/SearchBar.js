import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import './Button.css'

function SearchBar () {
  const [searchName, setSearchName] = useState('')
  const handleNameChange = event => { setSearchName(event.target.value) }
  const searchLink = `/search?q=${searchName}`
  return (
          <>
                <form>
                  <div>
                    <input type='text' placeholder='Company Name' className='search' value={searchName} onChange={handleNameChange}></input>
                   <Link to={searchLink}><button className="button" type="submit">SEARCH</button></Link>
                  </div>
                </form>
          </>)
}

export default SearchBar
