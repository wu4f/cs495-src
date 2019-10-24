var express = require('express')
var app = express()
function sendResponse(req, res, header) {
	res.setHeader('X-XSS-Protection', header);
	res.send(`<h1>Hello, ${req.query.user || 'anonymous'}</h1>X-XSS-Protection: ${header}`);
}

app.use('/xss-0', (req, res) => { sendResponse(req,res,'0'); })
app.use('/xss-1', (req, res) => { sendResponse(req,res,'1'); })
app.use('/xss-1-block', (req, res) => { sendResponse(req,res,'1; mode=block');})
app.use('/xss-1-report', (req, res) => {
  sendResponse(req,res, '1; report=http://localhost:1234/report');
 })

app.post('/report', (req, res) => {
  console.log("---\nXSS report received from %O \n---\n", req.headers.referer);
})

app.listen(1234)
