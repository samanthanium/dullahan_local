window.addEventListener("load", () => {
  const deviceID = document.getElementById("device-id").textContent

  const socket = new WebSocket(
    "ws://" + window.location.host + "/devices/" + deviceID + "/ws/console/"
  )

  socket.onmessage = (e) => {
    const commandHistory = document.querySelector(".command-history")
    const data = JSON.parse(JSON.parse(e.data).message)
    let output = ""
	  console.log(data)
    for (key in data) {
      let valueList = data[key].split("\n")
      valueList.pop()
      valueList.forEach((value) => {
        output += key + ": " + value + "\n"
      })
    }
    commandHistory.textContent = output
    outputBox = document.querySelector(".output")
    outputBox.scrollTop = outputBox.scrollHeight
  }

  socket.onclose = (e) => {
    console.error("Chat socket closed unexpectedly")
  }
  
  // Listens for command submit, and sends it via socket
  commandForm = document.querySelector(".command-form")
  commandForm.addEventListener('submit', e => {
    e.preventDefault()
    const message = commandForm.command.value
    if (message.length > 0) {
	    socket.send(
	      JSON.stringify({
		message: message,
		device: deviceID,
	      })
	    )
    commandForm.reset()
    }
  })
})
