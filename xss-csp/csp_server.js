"use strict"
var express = require('express')

for (let port of [1234, 4321]) {
  var app = express()
  app.use('/script.js', (req, res) => {
    res.send(`document.querySelector('#${req.query.id}').innerHTML = 'changed by ${req.query.id} script'`)
    console.log(req.url)
  })
  app.use((req, res) => {
    var csp = req.query.csp
    if (csp) res.header('Content-Security-Policy', csp)
    res.send(`
      <html>
      <body>
        <h1>Hello, ${req.query.user || 'anonymous'}</h1>
        <p id="inline">is this going to be changed by inline script?</p>
        <p id="origin">is this going to be changed by origin script?</p>
        <p id="remote">is this going to be changed by remote script?</p>
        <script>document.querySelector('#inline').innerHTML = 'changed by inline script'</script>
        <script src="/script.js?id=origin"></script>
        <script src="http://${req.hostname}:1234/script.js?id=remote"></script>
      </body>
      </html>
      `)
    console.log(req.url)
  })
  app.listen(port)
}
