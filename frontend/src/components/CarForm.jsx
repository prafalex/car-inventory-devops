import { useState } from "react"
import axios from "axios"

const FUELS = ["petrol", "diesel", "hybrid", "electric"]

function CarForm({ api, onSaved }) {
  const [form, setForm] = useState({
    brand: "", model: "", year: 2024,
    price: "", fuel: "petrol", mileage: "", color: ""
  })

  const handle = e => setForm({ ...form, [e.target.name]: e.target.value })

  const submit = async () => {
    if (!form.brand || !form.model || !form.price || !form.mileage) {
      alert("Please fill in all required fields.")
      return
    }
    await axios.post(`${api}/cars/`, {
      ...form, year: +form.year, price: +form.price, mileage: +form.mileage
    })
    onSaved()
  }

  return (
    <div className="car-form">
      <h2>Add a car</h2>
      <div className="form-grid">
        {["brand", "model", "color"].map(f => (
          <input key={f} name={f} placeholder={f.charAt(0).toUpperCase()+f.slice(1)}
            value={form[f]} onChange={handle} className="form-input" />
        ))}
        <input name="year"    type="number" placeholder="Year"    value={form.year}    onChange={handle} className="form-input" />
        <input name="price"   type="number" placeholder="Price €" value={form.price}   onChange={handle} className="form-input" />
        <input name="mileage" type="number" placeholder="Mileage" value={form.mileage} onChange={handle} className="form-input" />
        <select name="fuel" value={form.fuel} onChange={handle} className="form-input">
          {FUELS.map(f => <option key={f} value={f}>{f}</option>)}
        </select>
      </div>
      <button className="btn-primary" onClick={submit}>Save car</button>
    </div>
  )
}

export default CarForm
