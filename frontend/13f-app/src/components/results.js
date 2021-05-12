import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Results () {
  const [results, setResults] = useState([])
  useEffect(() => {
    axios.get('http://localhost:5000/company/search?q=t')
      .then(res => {
        const companies = res.data
        setResults(companies)
      })
  }, [])
  return (
        <div>
            <table>
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
            </table>
        </div>
  )
}

export default Results
