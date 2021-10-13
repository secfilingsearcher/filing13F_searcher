function capitalizeWords (phrase) {
  return phrase.trim().toLowerCase().replace(/\w\S*/g, (w) => (w.replace(/^\w/, (c) => c.toUpperCase())))
}

export default capitalizeWords
