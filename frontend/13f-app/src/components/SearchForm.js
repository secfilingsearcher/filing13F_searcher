import React from 'react'
import { useFormik } from 'formik'
import { useHistory } from 'react-router-dom'
import { InputGroup, Form, Button } from 'react-bootstrap'
import * as Yup from 'yup'


const validationSchema = Yup.object().shape({
    searchname: Yup.string().required('Required'),
    searchStartDate: Yup.date().required('Required'),
    searchEndDate: Yup.date().required('Required')
})

const SearchForm = () => {
  const history = useHistory()
  const formik = useFormik({
    initialValues: {
      searchName: '',
      searchStartDate: '',
      searchEndDate: ''
    },
    validationSchema,
    onSubmit: (values, { setSubmitting }) => {
      const searchLink = `/search?q=${values.searchName}&start_date=${values.searchStartDate}&end_date=${values.searchEndDate}`
      history.push(searchLink, { replace: true })
      setSubmitting(true)
    }
  })
  return (
       <Form onSubmit={formik.handleSubmit}>
         <InputGroup>
          <Form.Control
            id="searchName"
            name="searchName"
            type="text"
            onChange={formik.handleChange}
            value={formik.values.searchName}
            placeholder="Company Name"
          />
          <Form.Control
            id="searchStartDate"
            name="searchStartDate"
            type="date"
            onChange={formik.handleChange}
            value={formik.values.searchStartDate}
          />
          <Form.Control
            id="searchEndDate"
            name="searchEndDate"
            type="date"
            onChange={formik.handleChange}
            value={formik.values.searchEndDate}
          />
       <Button type="submit"><i className="bi bi-search"></i></Button>
       </InputGroup>
    </Form>
  )
}

export default SearchForm
