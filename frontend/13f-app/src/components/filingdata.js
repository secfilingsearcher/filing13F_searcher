import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import axios from 'axios'
import './filingdata.css'

function FilingData () {
  const [result, setResults] = useState([])
  const { state } = useLocation()
  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_SERVER}/edgarfiling/${state.accession_no}/data/`)
      .then(res => {
        const data = res.data
        setResults(data)
        console.log(data)
      })
  }, [])
  return (
        <div className='filing-data'>
            <h1>{state.accession_no}</h1>

            <table>
              <tbody>
                <tr>
                    <th>Name of Issuer</th>
                    <th>Title of Class</th>
                    <th>Value</th>
                </tr>
                    <tr key={result.accession_no}>
                      <td>{result.name_of_issuer}</td>
                      <td>{result.title_of_class}</td>
                      <td>{result.value}</td>
                    </tr>
              </tbody>
            </table>
        </div>
  )
}

export default FilingData
