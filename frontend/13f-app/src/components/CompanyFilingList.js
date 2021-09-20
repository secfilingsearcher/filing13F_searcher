import React from 'react'
import { Link } from 'react-router-dom'
import './CompanyFilingList.css'

function FilingsList () {
  const result = {
    company_name: 'Dummy Company',
    cik_no: 1234,
    ascension_number: 1234,
    endDate: '12/31/21'
  }

  return (
        <div id='filings-list'>
            <h1>{result.company_name}</h1>

            <table>
              <tbody>
                <tr>
                    <th>Ascension Number</th>
                    <th>Date</th>
                </tr>
                <tr key={result.cik_no}>
                    <td>{result.ascension_number}</td>
                    <td className="filing-date"><Link to={result.cik_no} className="filing-link-style">{result.endDate}</Link></td>
                </tr>
              </tbody>
            </table>
        </div>
  )
}

export default FilingsList
