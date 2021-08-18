import React from 'react'
import renderer from 'react-test-renderer'
import { BrowserRouter } from 'react-router-dom'
import SearchBar from '../components/SearchBar'

test('SearchBar renders', ()=> {
  const component = renderer.create(
        <BrowserRouter><SearchBar/></BrowserRouter>
  )
let tree = component.toJSON()
expect(tree).toMatchSnapshot()
})