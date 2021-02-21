const https = require('http')

const data = JSON.stringify({
  name: 'Sensor_1',
  tempF: '80',
  Hum: '38'
})

const options = {
  hostname: '127.0.0.1',
  port: 3000,
  path: '/',
  method: 'POST'
}

const req = https.request(options, res => {
  console.log(`statusCode: ${res.statusCode}`)

  res.on('data', d => {
    process.stdout.write(d)
  })
})

req.on('error', error => {
  console.error(error)
})

req.write(data)
req.end()
