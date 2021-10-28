import React, { useRef, useState } from 'react'
import { useFormik } from 'formik'
import { useHistory } from 'react-router-dom'
import { InputGroup, Form, Button, Overlay, Tooltip } from 'react-bootstrap'
import * as Yup from 'yup'

const validationSchema = Yup.object().shape({
  searchName: Yup.string().required()
})

const SearchForm = () => {
  const history = useHistory()
  const [show, setShow] = useState(false)
  const target = useRef(null)
  const showTooltip = () => {
    if (formik.errors.searchName) {
      setShow(false)
    } else {
      setShow(true)
    }
  }
  const formik = useFormik({
    initialValues: {
      searchName: ''
    },
    validationSchema,
    onSubmit: (values, { setSubmitting }) => {
      const searchLink = `/search?q=${values.searchName}`
      history.push(searchLink, { replace: true })
      setSubmitting(true)
      if (formik.errors.searchName) { setShow(!show) }
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
            ref={target}
          />
          <Overlay target={target.current} show={show} placement='bottom'>
            <Tooltip>Required</Tooltip>
          </Overlay>
       <Button type="submit" onClick={showTooltip}><i className="bi bi-search"></i></Button>
       </InputGroup>
    </Form>
  )
}

export default SearchForm
