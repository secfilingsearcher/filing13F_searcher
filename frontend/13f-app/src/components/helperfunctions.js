function capitalizeWords (phrase) {
  return phrase.trim().toLowerCase().replace(/\w\S*/g, (w) => (w.replace(/^\w/, (c) => c.toUpperCase())))
}

function valueFormat (value) {
  value = value * 1000
  const formatter = new Intl.NumberFormat('en-us', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0

  })
  return formatter.format(value)
}

export { capitalizeWords }
export { valueFormat }
