import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import axios from 'axios'

function Company () {
  const [company, setCompany] = useState()
  const location = useLocation()
  const param = new URLSearchParams(location.search)
  const name = param.get('name')

  useEffect(() => {
    axios.get(`http://localhost:5000/company/${name}`)
      .then(res => {
        const companydata = res.data
        setCompany(companydata)
      })
  }, [])
  return (
        <div>
            <h1>{companydata.company_name}</h1>
        </div>
  )
}

export default Company
