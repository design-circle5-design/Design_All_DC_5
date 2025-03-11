class khal_xsection:
    def __init__(self,sec_no,x,y,cl,B,ls,rs,dl):
        self.sec_no=sec_no
        self.x=x
        self.y=y
        self.cl=cl
        self.B=B
        self.ls=ls
        self.rs=rs
        self.dl=dl 
        self.top_rl=max(self.y)+5
        self.h=self.top_rl-self.dl
        self.B2=self.B/2.0
        self.draw_design_profile()
        #self.draw_existing_bed_profile()
        self.draw_existing_bed_profile()
        pass
        
    def find_left_intersection(self):
        x1=self.cl-self.B/2.0
        # Initialize an empty list to store indexes
        indexes = []
        # Loop through the list and find indexes
        for index, value in enumerate(self.x):
            if value<x1:
                indexes.append(index) 
        print(indexes)
        
    def draw_design_profile(self):
        cl=self.cl
        B2=self.B2
        h=self.h
        ls=self.ls
        rs=self.rs
        top_rl=self.top_rl
        dl=self.dl
        A=(cl-B2-h*ls,top_rl)
        B=(cl-B2,dl)
        C=(cl+B2,dl)
        D=(cl+B2+h*rs,top_rl)
        design_profile=LineString([A,B,C,D])
        self.design_profile=design_profile
        #return design_profile
        pass
        
    def draw_existing_bed_profile(self):
        x=self.x
        y=self.y
        mypoints=[]
        for i,t in enumerate(x):
            p=(x[i],y[i])
            mypoints.append(p)
        existing_profile=LineString(mypoints)
        print(existing_profile.geom_type)
        self.existing_bed_profile=existing_profile
        #return existing_profile
    
    def extend_existing_bed_profile(self,m): 
        existing_profile=self.existing_bed_profile
        # Get the last two points of the polyline
        last_point = list(existing_profile.coords)[-1]
        second_last_point = list(existing_profile.coords)[-2]
        # Calculate the direction vector of the last segment
        dx = last_point[0] - second_last_point[0]
        dy = last_point[1] - second_last_point[1]
        R=math.sqrt(dx**2+dy**2)
        i=dx/R
        j=dy/R
        logger.debug("R={} i={} j={}")
        logger.debug("last_poin{}".format(last_point))
        logger.debug("second_last_poin{}".format(second_last_point))
        logger.debug("dx={} dy={}".format(dx,dy))
        logger.debug("R={} i={} j={}".format(R,i,j))
        # Define the extension length (e.g., extend by 2 units to the right)
        extension_length = m
        logger.debug("extension length={}".format(m))
        # Calculate the new point to extend the polyline
        new_point = (last_point[0] + i * extension_length, last_point[1] + j * extension_length)
        # Create a new polyline by appending the new point
        new_polyline = LineString(list(existing_profile.coords) + [new_point])
        
        # Print the original and extended polylines
        logger.debug("Original Polyline:{}".format(existing_profile) )
        logger.debug("Extended Polyline:{}".format(new_polyline) )
        self.existing_bed_profile=new_polyline
        #update h values
        logger.debug("Updating Design Profile.................................")
        y_coordinates = [y for x, y in new_polyline.coords]
        logger.debug(y_coordinates)
        val1=self.top_rl
        val2=max( y_coordinates)+5
        self.top_rl=max(val1,val2)
        self.h=self.top_rl-self.dl
        self.draw_design_profile()

    def shift_cl(self,m):
        self.cl=self.cl+m
        self.draw_design_profile()
        
        
    def find_right_intersection(self):
        x1=self.cl+self.B/2.0
        # Initialize an empty list to store indexes
        indexes = []
        # Loop through the list and find indexes
        for index, value in enumerate(self.x):
            if value>x1:
                indexes.append(index) 
        print(indexes)
        
        
    def display(self):
        logger.debug("\n\n\n\n dispalying {}".format(self.sec_no))
        logger.debug(self.x)
        logger.debug(self.y)
        logger.debug("cl at {}".format(self.cl))
    