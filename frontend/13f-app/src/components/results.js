import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import axios from 'axios'

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
        <div>
            <table>
              <tbody>
                <tr>
                    <th>Company Name</th>
                    <th>Number of Filings</th>
                </tr>
                {results.map(result => (
                    <tr key={result.cik_no}>
                        <td><a href={}>{result.company_name}</a></td>
                        <td>{result.filing_count}</td>
                    </tr>
                ))}
              </tbody>
            </table>
        </div>
  )
}

export default Results
