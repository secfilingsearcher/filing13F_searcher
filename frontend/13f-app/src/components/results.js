import React, { useState, useEffect } from 'react'
import { useLocation, Link } from 'react-router-dom'
import Table from 'react-bootstrap/Table'
import axios from 'axios'
import './resultstable.css'

function Results () {
  const [results, setResults] = useState([])
  const location = useLocation()
  const params = new URLSearchParams(location.search)
  const { q, startDate, endDate } = { q: params.get('q'), startDate: params.get('startDate'), endDate: params.get('endDate') }

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_SERVER}/company/search?q=${q}&start_date=${startDate}&end_date=${endDate}`)
      .then(res => {
        const companies = res.data
        setResults(companies)
      })
  }, [])
  return (
        <div id="table-container">
          <h2>{results.length} Results Found</h2>
            <Table borderless>
              <thead>
              <tr>
                    <th>Company Name</th>
                    <th>Number of Filings</th>
                </tr>
              </thead>
              <tbody>
                {results.map(result => (
                    <tr key={result.cik_no}>
                        <td className="company-name"><Link to={{ pathname: `/company/${result.cik_no}/edgar-filing/`, state: result }} className="company-page-link-style">{result.company_name}</Link></td>
                        <td className="filing-count">{result.filing_count}</td>
                    </tr>
                ))}
              </tbody>
            </Table>
        </div>
  )
}

export default Results
