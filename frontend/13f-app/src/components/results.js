import React, { useState, useEffect } from 'react'
import { useLocation, Link } from 'react-router-dom'
import { ListGroup } from 'react-bootstrap'
import { capitalizeWords } from './HelperFunctions.js'
import LoadingSpinner from './LoadingSpinner.js'
import axios from 'axios'
import './ResultsList.css'

function Results () {
  const [results, setResults] = useState([])
  const [done, setDone] = useState(undefined)
  const location = useLocation()
  const params = new URLSearchParams(location.search)
  const q = params.get('q')
  const resultClassName = (count) => { return count > 0 ? 'bg-primary' : 'bg-danger' }

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_SERVER}/company/search?q=${q}`)
      .then(res => {
        const companies = res.data.sort((companyA, companyB) => {
          return companyA.filing_count < companyB.filing_count
        })
        setResults(companies)
        setDone(true)
      })
  }, [location.key])
  return (
        <div id="table-container">
          {!done && <LoadingSpinner/>}
          <p className="lead">
            <i className="bi bi-search"></i>
            &nbsp;
            {results.length} Results Found
          </p>
          <ListGroup>
                {results.map(result => (
                    <Link
                      to={{ pathname: `/company/${result.cik_no}/edgar-filing/`, state: result }}
                      className="result-item-link list-group-item" key={result.cik_no}>
                        {capitalizeWords(result.company_name)}
                    <br/>
                    <span className={`badge rounded-pill result-item-count ${resultClassName(result.filing_count)}`}>
                      <i className="bi bi-file-earmark-text"></i>
                      &nbsp;
                      {result.filing_count} {(() => { return result.filing_count > 1 || result.filing_count === 0 ? 'filings' : 'filing' })()}
                     </span>
                    </Link>
                ))}
          </ListGroup>
        </div>
  )
}

export default Results
