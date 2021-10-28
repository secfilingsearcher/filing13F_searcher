import React from 'react'
import renderer from 'react-test-renderer'
import SearchForm from '../components/SearchForm'

test('SearchForm renders', ()=> {
  const component = renderer.create(
        <SearchForm />
  )
let tree = component.toJSON()
expect(tree).toMatchSnapshot()
})
