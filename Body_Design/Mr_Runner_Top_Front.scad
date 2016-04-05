//servo mounts have been moved further from each other by an additional 0.5 mm each

$fn=64;

//main body
difference(){
translate([-1.5,0,0])      cube([60.6,95,5]);  
    
translate([152,15,-2.5])    cube([7,63,10]);
    
translate([-5,-1,3])    rotate([0,45,0])     cube([4,97,8]); 
}


//front shoulder servo mounts
difference(){
translate([-1.5,8,-19.8])   cube([10,8,19.8]);
    
translate([4.6,25,-4.9])  rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([4.6,25,-14.9]) rotate([90,0,0]) cylinder(20,1.8,1.8);
}

difference(){
translate([49.1,8,-19.8])   cube([10,8,19.8]);
    
translate([53,25,-4.9])  rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([53,25,-14.9]) rotate([90,0,0]) cylinder(20,1.8,1.8);
}

//rear shoulder servo mount
difference(){
translate([-1.5,79,-19.8])   cube([10,8,19.8]);
    
translate([4.6,89,-4.9])  rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([4.6,89,-14.9]) rotate([90,0,0]) cylinder(20,1.8,1.8);
}

difference(){
translate([49.1,79,-19.8])   cube([10,8,19.8]);
    
translate([53,90,-4.9])  rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([53,90,-14.9]) rotate([90,0,0]) cylinder(20,1.8,1.8);
}