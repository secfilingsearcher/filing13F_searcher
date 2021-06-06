import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import SearchBar from 'SearchBar.js'
import './Navbar.css'

function Navbar () {
  const [click, setClick] = useState(false)
  const handleClick = () => setClick(!click)
  const closeMobileMenu = () => setClick(false)

  return (
        <>
         <nav className="navbar">
             <div className="navbar-container">
                <SearchBar/>
                <Link to="/" className="navbar-logo">
                    13F   <i className="fas fa-file-archive"></i>
                </Link>
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

             </div>
         </nav>
        </>

  )
}

export default Navbar
