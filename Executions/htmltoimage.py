from htmlwebshot import WebShot
shot = WebShot()
shot.quality = 100

image = shot.create_pic(html="file.html")
