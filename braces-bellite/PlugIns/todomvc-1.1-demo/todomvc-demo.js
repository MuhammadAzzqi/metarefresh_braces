"use strict";
var connect = require('connect')
var gui = require('bellite').Bellite()

var port=3098,
  webapp = connect()
  .use(connect.logger('dev'))
  .use(connect.static('vanillajs/'))
  .listen(port, "127.0.0.1"); // prefer a known port

webapp.on('error', function(err) {
    if (err.syscall=='listen' && err.code == 'EADDRINUSE') {
        if (3098==port)
            webapp = this.listen(port=0, "127.0.0.1") // port in use — pick a random one
        else gui.perform(0, 'terminate')
    }
})

webapp.on('listening', function() {
    var addr=this.address(),
        url='http://'+addr.address+':'+addr.port+'/index.html';

    console.log('Serving TodoMVC Demo in Bellite at:', url)
    gui.ready.then(
        function() { gui.perform(0, 'navigateNew', {url:url, usePageTitle:false, center:0.5, width:740, height:600}) },
        function() { webapp.shutdown() })
})

