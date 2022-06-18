# Coordman

**Coordman** is a simple yet powerful waypoint and map manager for Minecraft.

[![example](images/example.png?raw=true)](example-user-data.js)

# Features
 - JourneyMap map import
 - Overworld, Nether, and The End dimensions
 - Nether and Overworld combo-view
 - Various overlays
 - Zoom-out far (all the way to the worldborder!)
 - Extremely customizable waypoints
 - Separately toggleable waypoint groups
 - Fast and responsive
 - Semi-offline (no data is sent to a server)

# How to use
1. Download this project somewhere on your computer.
2. Make sure the code you downloaded is safe and doesn't send coords to a weird server hosted in Narva.
3. Install Python3
4. Install Pillow (`pip3 install Pillow`) and TQDM (`pip install tqdm`)
5. Run `generateTiles.py` or `generateTiles.py [pathToFolderWithJMFiles]`to generate the map from your JourneyMap data.
6. Copy [`example-user-data.js`](example-user-data.js) to `user-data.js` and edit it with your own data to add waypoints.
7. Run `coordman.html` in your web browser.

## Example `user-data.js`
```js
window.userdata = {
  "groups": [
    {
      "name": "Sample Waypoints",
      "default": true,
      "markers": [
        {
          "coords": [0,0],
          "dimension": "DIM0",
          "name": "2b2t Spawn",
          "icon": "red",
          "data": [
            "<a href=\"https://upload.wikimedia.org/wikipedia/commons/9/9c/IronException_2b2t_Spawn_Render_June_2019.png\"><img style=\"width: 100%\" src=\"images/iron-spawn.png\" /></a>",
            "<i>2b2t Spawn Render by IronException</i>",
            "<b>Visited:</b> 2021-01-01",
            "<b>Coords:</b> 0,0",
            "<b>WDL:</b> example-spawn-wdl.zip",
            "You can put whatever HTML you want here, so you can have any information, not just predefined stuff!",
            "This includes things like images, <a href=\"https://youtu.be/yPxJnvSZrU0?t=36\">links</a> and <span style=\"font-family: 'Comic Sans MS'; color: red\">styling</span>.",
            "<b>⚠ This also means that JavaScript code can be added. DO NOT trust user-data.js files from other people.</b>"
          ]
        }
      ]
    }
  ]
}
```