//horizontal horn holes have been moved out 0.25 mm each (Mar 25)


$fn=64;
difference(){
translate([17.7,-13.1,0])
  cube([6,5,4]);
translate([20.5,-11.1,-1])
    cylinder(6,d=2,d=2);
}
difference(){  
  //main body
  hull(){  
    cylinder(4,d=24,d=24);
    translate([65,0,0])
      cylinder(4,d=24,d=24);
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
  //spring hole
  translate([20.5,-11.1,-1])
    cylinder(6,d=2,d=2);
  //main servo hole
  translate([24.5,-10,-1])
    cube([41,20,6]);
  //servo top slit
  translate([18.5,-1,-1])
    cube([6.5,2,6]);
  //top servo screws
  translate([21,5,-1])
    cylinder(6,d=3.5,d=3.5);
  translate([21,-5,-1])
    cylinder(6,d=3.5,d=3.5);
  //servo bottom slit
  translate([65,-1,-1])
    cube([6.5,2,6]);
  //bottom servo screws
  translate([69,5,-1])
    cylinder(6,d=3.5,d=3.5);
  translate([69,-5,-1])
    cylinder(6,d=3.5,d=3.5);
  //contours
  //horn side
  difference(){
    translate([7,11,-1])
      rotate([0,0,180])
        scale([1,0.8,1])
          cylinder(6,d=20,d=20,$fn=3);
    cylinder(6,d=24,d=24); 
  }
  difference(){
    translate([7,-11,-1])
      rotate([0,0,-180])
        scale([1,0.8,1])
          cylinder(6,d=20,d=20,$fn=3);
    cylinder(6,d=24,d=24); 
  }
  //body side 
  mirror([-1,0,0]){
  translate([-23.95,0,-1])  
    difference(){
      translate([7,-11,0])
        rotate([0,0,180])
          scale([1,0.8,1])
            cylinder(6,d=20,d=20,$fn=3);
      cylinder(6,d=24,d=24); 
    }
  }
  mirror([0,-1,0]){
  mirror([-1,0,0]){
  translate([-23.95,0,-1])  
    difference(){
      translate([7,-11,0])
        rotate([0,0,180])
          scale([1,0.8,1])
            cylinder(6,d=20,d=20,$fn=3);
      cylinder(6,d=24,d=24); 
    }
  }
}
}
