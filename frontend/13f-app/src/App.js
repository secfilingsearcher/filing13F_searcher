import React from 'react'
import Navbar from './components/Navbar'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Home from './components/pages/home'
import SearchResults from './components/pages/searchResults'
import './App.css'

function App () {
  return (
    <>
    <Router>
      <Navbar />
      <Switch>
        <Route path='/' exact component= {Home} />
        <Route path='/search' exact component= {SearchResults} />
      </Switch>
    </Router>
    </>
  )
}

export default App
