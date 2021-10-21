import React, { useState } from 'react'
import { useLocation, Link } from 'react-router-dom'
import Navbar from 'react-bootstrap/Navbar'
import SearchForm from './SearchForm'
import logo from '../images/favicon-32x32.png'
import './Navbar.css'

function Navigation () {
  const [click, setClick] = useState(false)
  const handleClick = () => setClick(!click)
  const closeMobileMenu = () => setClick(false)
  const path = useLocation().pathname

  return (
        <>
         <Navbar bg="dark" className="navbar">
                <Link to="/" className="navbar-logo">
                    <img src={logo}></img>
                </Link>
                {path !== '/' && <div className='searchbar'><SearchForm/></div>}
                <div className="menu-icon" onClick={handleClick}>
                    <i className={click ? 'fas fa-times' : 'fas fa-bars'} />
                </div>
                <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                    <li className="nav-item">
                        <Link to='/' className='nav-links' onClick={closeMobileMenu}>
                            Home
                        </Link>
                    </li>
                    <li className="nav-item">
                        <Link to='/search' className='nav-links' onClick={closeMobileMenu}>
                            Search
                        </Link>
                    </li>
                    <li className="nav-item">
                        <Link to='/about' className='nav-links' onClick={closeMobileMenu}>
                            About
                        </Link>
                    </li>
                </ul>
         </Navbar>
        </>

  )
}

export default Navigation
