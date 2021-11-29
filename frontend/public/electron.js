const electron = require('electron'),
  app = electron.app,
  BrowserWindow = electron.BrowserWindow;

const { spawn } = require('child_process');

const path = require('path'),
  isDev = require('electron-is-dev');

let mainWindow;

const createWindow = () => {
  mainWindow = new BrowserWindow({ width: 480, height: 320 })
  mainWindow.setIcon(path.join(app.getAppPath(), 'public/box.png').replace('app.asar', 'app.asar.unpacked')); // From: https://www.freepik.com/?_gl=1*ggevjl*test_ga*MTA5NDM0NTczLjE2MzU1Mzk3ODA.*test_ga_523JXC6VL7*MTYzNTUzOTc3OS4xLjEuMTYzNTUzOTgyMC4xOQ..
  // mainWindow.setMenu(null); removed navigation stuff but we need to change defaults on navigation
  const appUrl = isDev ? 'http://localhost:3000' :
    `file://${path.join(__dirname, '../build/index.html')}`
  mainWindow.loadURL(appUrl)
  mainWindow.maximize()
  mainWindow.setFullScreen(false)
  mainWindow.on('closed', () => mainWindow = null)
}

var child = spawn('python', [path.join(app.getAppPath(), 'backend/parsing/fileParse.py').replace('app.asar', 'app.asar.unpacked')]);

app.on('ready', createWindow);
app.on('window-all-closed', () => {
  // Follow OS convention on whether to quit app when
  // all windows are closed.
  child.kill();
  if (process.platform !== 'darwin') { app.quit() }
})
app.on('activate', () => {
  // If the app is still open, but no windows are open,
  // create one when the app comes into focus.
  if (mainWindow === null) { createWindow() }
})