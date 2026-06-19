import { useState, useEffect } from "react"
import axios from "axios"
import CarTable from "./components/CarTable"
import CarForm from "./components/CarForm"
import "./App.css"

const API = import.meta.env.VITE_API_URL || "/api"

function App() {
  const [cars, setCars]       = useState([])
  const [search, setSearch]   = useState("")
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [refreshKey, setRefreshKey] = useState(0)


 useEffect(() => {
    let ignore = false

    async function fetchCars() {
      setLoading(true)
      try {
        const params = search ? { brand: search } : {}
        const res = await axios.get(`${API}/cars/`, { params })
        if (!ignore) setCars(res.data)
      } catch (e) {
        console.error(e)
      } finally {
        if (!ignore) setLoading(false)
      }
    }

    fetchCars()

    return () => { ignore = true }
  }, [search, refreshKey])

  const handleDelete = async (id) => {
    await axios.delete(`${API}/cars/${id}`)
    setRefreshKey(k => k + 1)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🚗 Car Inventory</h1>
        <p className="subtitle">Manage your vehicle catalog!</p>
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
          <CarForm api={API} onSaved={() => { setShowForm(false); setRefreshKey(k => k + 1) }} />
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
