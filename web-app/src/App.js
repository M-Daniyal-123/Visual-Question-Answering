import logo from './logo.svg';
import './App.css';
import Navbar from './components/Navbar';
import Card from './components/Card';


function App() {

  const data =  new Date();

  return (
    <div className="App">

      
      <Navbar/>
      {/* <Hero/> */}

      <Card />
      

    </div>
  );
}

export default App;
