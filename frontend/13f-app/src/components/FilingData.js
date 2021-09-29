import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import './FilingData.css'

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
        <div id='filing-data'>
            <h1>{company.company_name}: {filingId}</h1>

            <table id='filing-data-table'>
              <thead>
                <tr>
                    <th>Name of Issuer</th>
                    <th>Title of Class</th>
                    <th>CUSIP</th>
                    <th>Value</th>
                    <th>Share Principal Amount</th>
                    <th>Share Type</th>
                    <th>Put Call</th>
                    <th>Investment Discretion</th>
                    <th>Other Manager</th>
                    <th>Voting Authority Sole</th>
                    <th>Voting Authority Shared</th>
                    <th>Voting Authority None</th>
                </tr>
                </thead>
                <tbody>
                {results.length === 0 && <tr><td colSpan='12'><h3>No Data to Display</h3></td></tr>}
                {results.map(result => (
                    <tr key={result.accession_no}>
                      <td>{result.name_of_issuer}</td>
                      <td>{result.title_of_class}</td>
                      <td>{result.cusip}</td>
                      <td>{result.value}</td>
                      <td>{result.ssh_prnamt}</td>
                      <td>{result.ssh_prnamt_type}</td>
                      <td>{result.put_call}</td>
                      <td>{result.investment_discretion}</td>
                      <td>{result.other_manager}</td>
                      <td>{result.voting_authority_sole}</td>
                      <td>{result.voting_authority_shared}</td>
                      <td>{result.voting_authority_none}</td>
                    </tr>
                ))}
              </tbody>
            </table>
        </div>
  )
}

export default FilingData
