const express = require("express")
const pug = require("pug")
const path = require("path")
const app = express()
const port = 3000

app.set("view engine", "pug")

app.use(express.static("node_modules/axios/dist"));
app.use(express.static("node_modules/chart.js/dist"));
app.use(express.static("node_modules/normalize.css"));
app.use(express.static("node_modules/bulma"));
app.use(express.static("node_modules/xterm/lib"));
app.use(express.static("node_modules/xterm/css"));
app.use(express.static("node_modules/xterm-addon-fit/lib"));
app.use("/js", express.static("js"));
app.use("/css", express.static("css"));
app.use("/img", express.static("img"));

app.get("/", (req, res) => {
  res.render("bgui");
})

app.listen(port, () => {
  console.log(`BrainGenix UI front-end server is listening at http://localhost:${port}`)
})