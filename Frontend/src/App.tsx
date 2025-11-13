import './App.css'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Navbar from './components/navbar/Navbar'
import Sidebar from './components/sidebar/Sidebar.tsx'
import Inicio from './components/inicio/Inicio.tsx'
function App() {

  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col">
        <Navbar />

        <div className="flex flex-1">
          {/* Sidebar */}
          <aside className="hidden lg:block">
            <Sidebar />
          </aside>

          {/* Main content area */}
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Inicio />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App
