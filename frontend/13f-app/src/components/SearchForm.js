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
  const formik = useFormik({
    initialValues: {
      searchName: ''
    },
    validationSchema,
    validate: () => {
      if (!formik.values.searchName) {
        setShow(true)
      } else {
        setShow(false)
      }
    },
    onSubmit: (values, { setSubmitting }) => {
      const searchLink = `/search?q=${values.searchName}`
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
            ref={target}
          />
          <Overlay target={target.current} show={show} placement='bottom'>
            <Tooltip>Required</Tooltip>
          </Overlay>
       <Button type="submit"><i className="bi bi-search"></i></Button>
       </InputGroup>
    </Form>
  )
}

export default SearchForm
