import React from 'react'
import Navigation from './components/Navbar'
import Footer from './components/Footer'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'
import Home from './components/pages/Home'
import About from './components/pages/AboutPage'
import SearchResults from './components/pages/SearchResults'
import FilingsPage from './components/pages/FilingsListPage'
import DataPage from './components/pages/Datapage'

import './App.css'

function App () {
  return (
    <>
    <Router>
      <Navigation />
      <Switch>
        <Route path='/' exact component= {Home} />
        <Route path='/about' exact component= {About} />
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
