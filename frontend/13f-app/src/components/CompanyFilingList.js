import React, { useState, useEffect } from 'react'
import { useLocation, useParams, Link } from 'react-router-dom'
import Table from 'react-bootstrap/Table'
import axios from 'axios'
import './CompanyFilingList.css'

function FilingsList () {
  const [results, setResults] = useState([])
  const { state } = useLocation()
  const { companyId } = useParams()
  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_SERVER}/company/${companyId}/edgar-filing/`)
      .then(res => {
        const filings = res.data
        setResults(filings)
      })
  }, [])
  return (
        <div id='filings-list'>
            <h1>{state.company_name}</h1>
            <div id="table-container">
              <Table borderless hover>
                <thead>
                  <tr>
                      <th>Accession Number</th>
                      <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map(result => (
                      <tr key={result.accession_no}>
                        <td><Link to={{ pathname: `/company/${companyId}/edgar-filing/${result.accession_no}/data/` }} className="link-style">{result.accession_no}</Link></td>
                        <td className="filing-date">{result.filing_date}</td>
                      </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          </div>
  )
}

export default FilingsList
