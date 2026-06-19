import { useState, useEffect } from "react"
import axios from "axios"
import CarTable from "./components/CarTable"
import CarForm from "./components/CarForm"
import "./App.css"

const API = import.meta.env.VITE_API_URL || "http://localhost:8000/api"

function App() {
  const [cars, setCars]       = useState([])
  const [search, setSearch]   = useState("")
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)

  const fetchCars = async () => {
    setLoading(true)
    try {
      const params = search ? { brand: search } : {}
      const res = await axios.get(`${API}/cars/`, { params })
      setCars(res.data)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchCars() }, [search])

  const handleDelete = async (id) => {
    await axios.delete(`${API}/cars/${id}`)
    fetchCars()
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🚗 Car Inventory</h1>
        <p className="subtitle">Manage your vehicle catalog</p>
      </header>

      <main className="app-main">
        <div className="toolbar">
          <input
            className="search-input"
            placeholder="Search by brand..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
            {showForm ? "Close" : "+ Add Car"}
          </button>
        </div>

        {showForm && (
          <CarForm api={API} onSaved={() => { setShowForm(false); fetchCars() }} />
        )}

        {loading ? (
          <p className="loading">Loading...</p>
        ) : (
          <CarTable cars={cars} onDelete={handleDelete} />
        )}
      </main>
    </div>
  )
}

export default App
