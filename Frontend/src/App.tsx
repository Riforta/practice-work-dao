import './App.css'
import { BrowserRouter } from 'react-router-dom'
import Navbar from './components/navbar/Navbar'
import Sidebar from './components/sidebar/Sidebar.tsx'
function App() {

  return (
    <BrowserRouter>
      <div>
        
            <Navbar />
            <Sidebar />
        
      </div>
      </BrowserRouter>
  );
}

export default App
