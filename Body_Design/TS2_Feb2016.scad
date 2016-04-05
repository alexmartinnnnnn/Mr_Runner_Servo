$fn=64;

difference(){
union(){
translate([-60,16,2])
  rotate([0,90,150])
    cylinder(12.7,d=12.7,d=12.7);
translate([-70.4,22,2])
  rotate([0,90,150])
    sphere(d=12.7);
}
translate([-80,5,0])
  //rotate([0,90,150])
    cube([25,25,15]);
}

    