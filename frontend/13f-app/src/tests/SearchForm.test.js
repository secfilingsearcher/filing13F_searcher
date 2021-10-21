import React from 'react'
import renderer from 'react-test-renderer'
import SearchForm from '../components/SearchForm'

test('SearchForm renders', ()=> {
    // October 20th, 2021
  const date = (new Date(2021, 10, 20)).toISOString().substr(0, 10)
  const component = renderer.create(
        <SearchForm startDate={date} endDate={date}/>
  )
let tree = component.toJSON()
expect(tree).toMatchSnapshot()
})
