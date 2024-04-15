import React, { useEffect, useState } from 'react'
import '../styles/SearchView.css'

const SearchView = () => {

  const api = 'https://dummyjson.com/products/search?q='

  const [searchresult, setsearchresult] = useState([])

  const updateSearchResult = (param) => {

    setsearchresult(param.products)
  }

  return (
    <div className='flex flex-justify-center flex-column flex-align-center'>
      {/* <div>SearchView</div> */}
      <SearchBox updateSearchResult={updateSearchResult} />
      <SearchResult searchresult={searchresult} />
    </div>
  )
}

export default SearchView


const SearchResult = ({ searchresult }) => {
  return (
    <div className='search-result'>
      {searchresult && searchresult.map((item, index) => (
        <div key={index} className='products'>

          <div className='flex flex-row flex-justify-space-between flex-align-center'>
            <div className='title'>{item.title}</div>
            <div className='rating'>
           {startRating(item.rating)}
            </div>
          </div>
          <div className="description">{item.description}</div>
        </div>
      ))}
    </div>
  )
}

const SearchBox = ({ updateSearchResult }) => {

  const [inputValue, setInputvalue] = useState('')

  useEffect(() => {

    async function fetchData(inputValue) {
      const response = await fetch(`https://dummyjson.com/products/search?q=${inputValue}`)
      const data = await response.json()
      updateSearchResult(data)
    }

    if (inputValue.length) {
      fetchData(inputValue)
    }
  }, [inputValue])


  const handleChange = (e) => {
    setInputvalue(e.target.value)
  }

  return (
    <div className='search-box '>
      <input type='text' placeholder='Search...' onChange={handleChange} />
    </div>
  )
}

const startRating = (rating) => {
  let stars = []
  for (let i = 0; i < Math.floor(rating); i++) {
    stars.push(<i className="fas fa-star"></i>)
  }
  if (rating % 1 !== 0) {
    stars.push(<i className="fas fa-star-half"></i>)
  }
  return stars
}