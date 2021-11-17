import React from 'react'
import '../AboutPage.css'
import wallStreetImage from 'images/chris-li-6Y6OnwBKk-o-unsplash.jpg'

function About () {
  return (
        <>
            <div className='container' id='about-main'>
                <br />
                <div className='bg-dark text-white col-md-8' id='story-panel'>
                    <div id='bio-contents'>
                    <h3>About 13F Filing Searcher</h3>
                    <hr />
                    <p>This site was created through the collaboration of two aspiring software engineers,  <a className="link-light" href="https://github.com/rosealti">Rose Altianas</a> and <a className="link-light" href="https://github.com/eharley19">Edward Harley</a>, under the mentorship and supervision of two industry professionals.</p>
                    <p>Built with:</p>
                    <ul className="list-group list-group-flush">
                        <li className="list-group-item"><h4><span className="badge bg-secondary">Python</span></h4></li>
                        <li className="list-group-item"><h4><span className="badge bg-secondary">Flask</span></h4></li>
                        <li className="list-group-item"><h4><span className="badge bg-secondary">Flask-SQLAlchemy</span></h4></li>
                        <li className="list-group-item"><h4><span className="badge bg-secondary">JavaScript</span></h4></li>
                        <li className="list-group-item"><h4><span className="badge bg-secondary">React</span></h4></li>
                        <li className="list-group-item"><h4><span className="badge bg-secondary">Bootstrap</span></h4></li>
                    </ul>
                    </div>
                    <img id="wall-street-image" src={wallStreetImage} alt="wall street sign" />
                </div>
            </div>
        </>
  )
}

export default About
