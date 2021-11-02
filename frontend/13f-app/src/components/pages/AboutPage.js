import React from 'react'
import '../AboutPage.css'

function About () {
  return (
        <>
            <div className='container' id='about-main'>
                <br></br>
                <div className='bg-dark text-white col-md-8' id='story-panel'>
                    <h3>About 13F Filing Searcher</h3>
                    <p>This site was created through the collaboration of two aspiring software engineers, Rose Altianas (<a>www.github.com</a>) and Edward Harley (<a>www.github.com</a>), under the mentorship and supervision of two industry professionals.</p>
                </div>
                <div id='image-panel'></div>
            </div>
        </>
  )
}

export default About
