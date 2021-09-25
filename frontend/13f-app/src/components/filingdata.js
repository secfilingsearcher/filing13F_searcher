import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import './filingdata.css'

function FilingData () {
  const [results, setResults] = useState([])
  const [company, setCompany] = useState([])
  const { companyId, filingId } = useParams()
  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_SERVER}/edgarfiling/${filingId}/data/`)
      .then(res => {
        const data = res.data
        setResults(data)
      })
    axios.get(`${process.env.REACT_APP_API_SERVER}/company/${companyId}`)
      .then(res => {
        const data = res.data
        setCompany(data)
      })
  }, [])
  return (
        <div className='filing-data'>
            <h1>{company.company_name}: {filingId}</h1>

            <table>
              <tbody>
                <tr>
                    <th>Name of Issuer</th>
                    <th>Title of Class</th>
                    <th>CUSIP</th>
                    <th>Value</th>
                </tr>
                {results.map(result => (
                    <tr key={result.accession_no}>
                      <td>{result.name_of_issuer}</td>
                      <td>{result.title_of_class}</td>
                      <td>{result.cusip}</td>
                      <td>{result.value}</td>
                    </tr>
                ))}
              </tbody>
            </table>
        </div>
  )
}

export default FilingData
