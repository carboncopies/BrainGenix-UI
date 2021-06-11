const express = require('express')
const pug = require('pug')
const path = require('path')
const app = express()
const port = 3000

app.set('view engine', 'pug')

app.use(express.static('node_modules/axios/dist'));
app.use('/js', express.static('js'));
app.use('/css', express.static('css'));
app.use('/img', express.static('img'));

app.get('/', (req, res) => {
  res.render('dashboard');
})

app.listen(port, () => {
  console.log(`BrainGenix UI front-end server is listening at http://localhost:${port}`)
})