sio = io()

sio.on('connect',(msg)=>{
    console.log(['connect',msg])
    $('#localtime').addClass('online').removeClass('offline')
})

sio.on('disconnect',(msg)=>{
    console.log(['disconnect',msg])
    $('#localtime').addClass('offline').removeClass('online')
})

sio.on('localtime',(msg)=>{
    console.log(['localtime',msg])
    $('#localtime').text(msg.date+" | "+msg.time)
})
