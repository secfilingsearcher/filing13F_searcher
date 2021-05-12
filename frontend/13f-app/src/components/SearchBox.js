import React, { Component } from 'react'
import ReactSearchBox from 'react-search-box'

class SearchBox extends Component {
  render () {
    return (
      <ReactSearchBox
        placeholder="Company Name"
        value=""
        data={[]}
        callback={record => console.log(record)}
      />
    )
  }
}

export default SearchBox
