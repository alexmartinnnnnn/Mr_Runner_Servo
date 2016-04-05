//servo mounts have been moved down 1mm and each 0.5 mm further from each other

$fn=64;

//front extension
difference(){
translate([-1.5,-25,0])     cube([60,25,5]);
    
translate([-5,-26,3])  rotate([0,45,0])     cube([4,26,8]); 
}
  
//back extension
difference(){
translate([-1.5,95,0])     cube([60,25,5]);
    
translate([-5,95,3])   rotate([0,45,0])     cube([4,26,8]); 
}
//main body
difference(){
translate([-1.5,0,0])      cube([60,95,5]);  
    
translate([-5,-1,3])    rotate([0,45,0])     cube([4,97,8]); 
}

//front hip servo mounts
difference(){
translate([-1.5,-17,-19.8]) cube([10,8,20.8]);
    
translate([4.3,-2,-4.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([4.3,-2,-14.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
}

difference(){
translate([48.5,-17,-19.8]) cube([10,8,20.8]);

translate([52.7,-2,-4.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([52.7,-2,-14.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
}

//rear hip servo mounts
difference(){
translate([-1.5,104,-19.8]) cube([10,8,20.8]);
    
translate([4.3,120,-4.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([4.3,115,-14.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
}

difference(){
translate([48.5,104,-19.8]) cube([10,8,20.8]);

translate([52.7,115,-4.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
    
translate([52.7,115,-14.9])rotate([90,0,0]) cylinder(20,1.8,1.8);
}

