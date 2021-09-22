import React, { useState, useEffect } from 'react'
import { useLocation, Link } from 'react-router-dom'
import axios from 'axios'
import './CompanyFilingList.css'

function FilingsList () {
  const [results, setResults] = useState([])
  const { state } = useLocation()
  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_SERVER}/company/${state.cik_no}/edgarfiling/`)
      .then(res => {
        const filings = res.data
        setResults(filings)
      })
  }, [])
  return (
        <div id='filings-list'>
            <h1>{state.company_name}</h1>

            <table>
              <tbody>
                <tr>
                    <th>Ascension Number</th>
                    <th>Date</th>
                </tr>
                {results.map(result => (
                    <tr key={result.accession_no}>
                      <td><Link to={{ pathname: `/edgarfiling/${result.accession_no}/data/`, state: result }}>{result.accession_no}</Link></td>
                      <td className="filing-date">{result.filing_date}</td>
                    </tr>
                ))}
              </tbody>
            </table>
        </div>
  )
}

export default FilingsList
