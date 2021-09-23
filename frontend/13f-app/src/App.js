import React from 'react'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Home from './components/pages/home'
import SearchResults from './components/pages/searchResults'
import FilingsPage from './components/pages/filinglistpage'
import DataPage from './components/pages/datapage'

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
        <Route path='/company/:companyId/edgarfiling/' exact component= {FilingsPage} />
        <Route path='/company/:companyId/edgarfiling/:filingId/data/' exact component= {DataPage} />
      </Switch>
      <Footer />
    </Router>
    </>
  )
}

export default App
