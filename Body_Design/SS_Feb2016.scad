$fn=64;

difference(){ 
  //main body 
  hull(){  
    cylinder(4,d=24,d=24);
    translate([67,0,0])
      cylinder(4,d=10,d=10);
  }
  //spline hole
  translate([0,0,-1])
    cylinder(6,d=8.5,d=8.5);
  //4 horn holes
  translate([0,8.6,-1])
    cylinder(6,d=2.5,d=2.5);
  translate([0,-8.6,-1])
    cylinder(6,d=2.5,d=2.5);
  translate([7.1,0,-1])
    cylinder(6,d=2.5,d=2.5);
  translate([-7.1,0,-1])
    cylinder(6,d=2.5,d=2.5);
  //passive hole
  translate([67,0,-1])
    cylinder(6,d=5,d=5);
  //contours
  translate([35,-10,-1])
    rotate([0,0,6])
      scale([5.8,1,1])
        cylinder(6,d=12,d=12);
  translate([35,10,-1])
    rotate([0,0,-6])
      scale([5.8,1,1])
        cylinder(6,d=12,d=12);
}
//overlay horn cylinder to maintan
//shape
difference(){
cylinder(4,d=24,d=24);
//spline hole
translate([0,0,-1])    
  cylinder(6,d=8.5,d=8.5);
//4 horn holes
translate([0,8.6,-1])
  cylinder(6,d=2.5,d=2.5);
translate([0,-8.6,-1])
  cylinder(6,d=2.5,d=2.5);
translate([7.1,0,-1])
  cylinder(6,d=2.5,d=2.5);
translate([-7.1,0,-1])
  cylinder(6,d=2.5,d=2.5);
}
//overlay passive cylinder to maintain
//shape
difference(){
  translate([67,0,0])
      cylinder(4,d=10,d=10);
  translate([67,0,-1])
    cylinder(6,d=5,d=5);
}