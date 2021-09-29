import React from 'react'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Home from './components/pages/Home'
import SearchResults from './components/pages/SearchResults'
import FilingsPage from './components/pages/FilingsListPage'
import DataPage from './components/pages/DataPage'

import './App.css'

function App () {
  return (
    <>
    <Router>
      <Navbar />
      <Switch>
        <Route path='/' exact component= {Home} />
        <Route path='/search' exact component= {SearchResults} />
        <Route path='/company/:companyId' exact component= {SearchResults} />
        <Route path='/company/:companyId/edgar-filing' exact component= {FilingsPage} />
        <Route path='/company/:companyId/edgar-filing/:filingId/data' exact component= {DataPage} />
      </Switch>
      <Footer />
    </Router>
    </>
  )
}

export default App
