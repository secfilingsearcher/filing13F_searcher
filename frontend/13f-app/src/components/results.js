import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import axios from 'axios'

function Results () {
  const [results, setResults] = useState([])
  const location = useLocation()
  const params = new URLSearchParams(location.search)
  const { q, startDate, endDate } = { companyName: params.get('company_name'), { nameOfIssuer: params.get('name_of_issuer'), startDate: params.get('startDate'), endDate: params.get('endDate') }

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
                    <th>CIK_NO</th>
                </tr>
                {results.map(result => (
                    <tr key={result.cik_no}>
                        <td>{result.company_name}</td>
                        <td>{result.cik_no}</td>
                    </tr>
                ))}
              </tbody>
            </table>
        </div>
  )
}

export default Results
