//ALL SERVO HOLE WIDTHS ARE APPROPRIATE. ADJUST SERVO MOUNTS FOR PROPER CLEARANCE

//ROUND EXTENSION BOTTOM FRONT CORNERS

$fn=64;

//front extension
difference(){
translate([172,-25,0])     cube([59,25,5]);
    
translate([168,-26,3]) rotate([0,45,0])     cube([4,26,8]); 
}
  
//back extension
difference(){
translate([172,95,0])     cube([59,25,5]);
    
translate([168,95,3])  rotate([0,45,0])     cube([4,26,8]); 
}
//main body
difference(){
translate([-1,0,0])      cube([232,95,5]);  
    
translate([152,15,-2.5])    cube([7,63,10]);
    
translate([-5,-1,3])    rotate([0,45,0])     cube([4,97,8]); 
}

//front hip servo mounts
difference(){
translate([172,-25,-19.8]) cube([10,8,19.8]);
    
translate([177.3,-10,-4.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([177.3,-10,-14.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
}

difference(){
translate([221,-25,-19.8]) cube([10,8,19.8]);

translate([225.7,-10,-4.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([225.7,-10,-14.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
}

//rear hip servo mounts
difference(){
translate([172,112,-19.8]) cube([10,8,19.8]);
    
translate([177.3,128,-4.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([177.3,123,-14.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
}

difference(){
translate([221,112,-19.8]) cube([10,8,19.8]);

translate([225.7,123,-4.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([225.7,120,-14.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
}

//front shoulder servo mounts
difference(){
translate([-1,0,-19.8])   cube([10,8,19.8]);
    
translate([4.6,17,-4.9])  rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([4.6,17,-14.9]) rotate([90,0,0]) cylinder(20,1.8,1.8);
}

difference(){
translate([48.6,0,-19.8])   cube([10,8,19.8]);
    
translate([53,17,-4.9])  rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([53,17,-14.9]) rotate([90,0,0]) cylinder(20,1.8,1.8);
}

//rear shoulder servo mount
difference(){
translate([-1,87,-19.8])   cube([10,8,19.8]);
    
translate([4.6,97,-4.9])  rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([4.6,97,-14.9]) rotate([90,0,0]) cylinder(20,1.8,1.8);
}

difference(){
translate([48.6,87,-19.8])   cube([10,8,19.8]);
    
translate([53,98,-4.9])  rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([53,98,-14.9]) rotate([90,0,0]) cylinder(20,1.8,1.8);
}