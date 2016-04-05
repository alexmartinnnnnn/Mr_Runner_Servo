//spring hole has been moved down
//by 6
//hull to foot instead of cylinder
$fn=64;

difference(){
  hull(){
    intersection()
      cylinder(4,d=32,d=32);
    translate([39,5,0])
      cylinder(4,d=5,d=5);
    translate([-65,18,0])
      cylinder(4,d=5,d=5);
    }
  //passive joint hole
  translate([0,0,-1])
    cylinder(6,d=5,d=5);
  //spring hole
  translate([38.5,5.7,-1])
    cylinder(6,d=2,d=2);
  //front spring side contour
  translate([34,-20,-1])
    scale([1,1,1])
     cylinder(6,d=48,d=48);
  //foot side contour
  translate([-28,31,-1])
    scale([3,1.67,1])
      rotate([0,0,0])
        cylinder(6,d=25,d=25);
  //back spring side contour
  translate([12,25,-1])
    scale([3.7,1,1])
      cylinder(6,d=15,d=15);
  //remove edges from passive top
  difference(){
  translate([11,-13,5])
    rotate([0,180,0])
      cylinder(6,d=15,d=15,$fn=3);
  cylinder(6,d=32,d=32);
  }
  //remove edges from passive bottom
  difference(){
  translate([-4,11,5])
    rotate([0,180,0])
      cylinder(6,d=15,d=15,$fn=3);
  cylinder(6,d=32,d=32);
  }
  /*difference(){
  translate([3,11,5])
    rotate([0,180,0])
      cylinder(6,d=15,d=15,$fn=3);
  cylinder(6,d=32,d=32);
  }*/

}
//foot
difference(){
union(){
translate([-60,16,2])
  rotate([0,90,150])
    cylinder(12.7,d=12.7,d=12.7);
translate([-70.4,22,2])
  rotate([0,90,150])
    sphere(d=12.7);
}
translate([-80,5,-5])
    cube([25,25,5]);
}
//maintain passive cylinder
difference(){
cylinder(4,d=32,d=32);
translate([0,0,-1])
    cylinder(6,d=5,d=5);
}
