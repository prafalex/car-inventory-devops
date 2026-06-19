function CarTable({ cars, onDelete }) {
  if (cars.length === 0) return <p className="empty">No cars found.</p>

  return (
    <div className="table-wrapper">
      <table className="car-table">
        <thead>
          <tr>
            <th>Brand</th><th>Model</th><th>Year</th>
            <th>Fuel</th><th>Mileage</th><th>Price</th><th></th>
          </tr>
        </thead>
        <tbody>
          {cars.map(car => (
            <tr key={car.id}>
              <td><strong>{car.brand}</strong></td>
              <td>{car.model}</td>
              <td>{car.year}</td>
              <td><span className={`badge fuel-${car.fuel}`}>{car.fuel}</span></td>
              <td>{car.mileage.toLocaleString()} km</td>
              <td>€{car.price.toLocaleString()}</td>
              <td>
                <button className="btn-delete" onClick={() => onDelete(car.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default CarTable
