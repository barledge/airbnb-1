/*
 * Assumes we've already loaded raw JSON data,
 * which is stored in data.js and assigned to
 * the global variable <data>
 */

const LS_CURRENT_ROOM = 'current_room'
let currentRoom = {latlng: [0, 0]} // default

function getRandom() {
  const n = data.length
  const i = Math.floor(Math.random() * n)
  const room = data[i]

  localStorage.setItem(LS_CURRENT_ROOM, JSON.stringify(room))

  return room
}

function getCurrent() {
  let current = localStorage.getItem(LS_CURRENT_ROOM)
  if (!current)
    return null
  return JSON.parse(current)
}

function main() {
  currentRoom = getCurrent()
  const nextRoom = getRandom()

  if (!currentRoom)
    return main()

  // load current photo info
  document.getElementById('img-current').setAttribute('src', currentRoom.img)
  document.getElementById('title-current').innerHTML = currentRoom.title
  document.getElementById('title-current')
    .setAttribute('href', 'https://airbnb.com'+currentRoom.id)
  document.getElementById('price-current').innerHTML = currentRoom.price
  // preload next photo in background
  document.getElementById('img-next').setAttribute('src', nextRoom.img)
  console.log(currentRoom)
  console.log(nextRoom)
}

main()
