import React from 'react'
import { useFormik } from 'formik'
import { useHistory } from 'react-router-dom'

const SearchForm = () => {
  const history = useHistory()
  const formik = useFormik({
    initialValues: {
      searchName: '',
      searchStartDate: '',
      searchEndDate: ''
    },
    onSubmit: values => {
      const searchLink = `/search?q=${values.searchName}&startDate=${values.searchStartDate}&endDate=${values.searchEndDate}`
      history.push({ searchLink })
    }
  })
  return (
       <form onSubmit={formik.handleSubmit}>
       <input
         id="searchName"
         name="searchName"
         type="text"
         onChange={formik.handleChange}
         value={formik.values.searchName}
       />
       <input
         id="searchStartDate"
         name="searchStartDate"
         type="text"
         onChange={formik.handleChange}
         value={formik.values.searchStartDate}
       />
       <input
         id="searchEndDate"
         name="searchEndDate"
         type="text"
         onChange={formik.handleChange}
         value={formik.values.searchEndDate}
       />
       <button type="submit">Submit</button>
    </form>
  )
}

export default SearchForm
