import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import CarTable from '../CarTable'

describe('CarTable', () => {
  it('shows empty message when no cars', () => {
    render(<CarTable cars={[]} onDelete={vi.fn()} />)
    expect(screen.getByText(/no cars found/i)).toBeInTheDocument()
  })

  it('renders a car row', () => {
    const cars = [{ id: 1, brand: 'BMW', model: '3 Series', year: 2022, fuel: 'petrol', mileage: 1000, price: 40000 }]
    render(<CarTable cars={cars} onDelete={vi.fn()} />)
    expect(screen.getByText('BMW')).toBeInTheDocument()
    expect(screen.getByText('3 Series')).toBeInTheDocument()
  })
})