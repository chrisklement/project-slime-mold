# add the needed libs
add_library('video')
add_library('opencv_processing')

# setup global objects
video = None
opencv = None
points = []

lastLocation = None
o = 0
m = 0
n = 0

def setup():
    
    # reference global objects
    global video
    global opencv
    global font
    global lastLocation
    global n
    global o
    global m
    
    # sketh size like video
    size(1280, 720, P2D)
    
    # load the video you want to track
    video = Movie(this, "sample.mp4")
    
    # init openCV
    opencv = OpenCV(this, 1280, 720)
    
    # setup background subtraction
    # see http://atduskgreg.github.io/opencv-processing/reference/
    opencv.startBackgroundSubtraction(5, 4, 0.5)
    
    # play the video
    video.play()

def draw():
    
    #### CAPTURE ####
    opencv.loadImage(video)
    
    #### FILTER ####
    opencv.updateBackground()
    opencv.contrast(1)
    contrast_image = opencv.getSnapshot()
    opencv.dilate()
    opencv.erode()
    
    #### Set global Variable ####
    global lastLocation
    global o
    global n
    global m
    
    #### Style ####
    smooth();
    noFill()
    noStroke()
    strokeWeight(0)
    
    # if there are contours get the biggest one
    contours = opencv.findContours(False, True)
    if contours.size() > 25:
        r = contours.get(0).getBoundingBox()
        s = contours.size()
        for i in range(2):
            d = random(s, s * 1.5)
            noStroke()
            fill (96, 109, 128, random(s, s * 2))
            ellipse(r.x, r.y, d, d)
            points.append([r.x, r.y])
            
            for i in range(i < 40):
                if (lastLocation is not None):
                    distance = dist(r.x, r.y, lastLocation.x, lastLocation.y)
                    if distance < 400:
                        stroke (255)
                        strokeWeight (1)
                        line(r.x, r.y, lastLocation.x, lastLocation.y)
                        
                lastLocation = r
    # loop all points
    fill(255,255,255, random(10, 255))
    for i in range(0,len(points)):
        ellipse(points[i][0], points[i][1], 2, 2)

    # simple draw all contours
    stroke(255,255,255, random(10, 255))
    for contour in contours:
        contour.draw()
 
    # display contrast video
    image(contrast_image, 0, 0, video.width / 6, contrast_image.height / 6)

def movieEvent(m):
    m.read()
