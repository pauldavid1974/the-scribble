// The Scribble v8 ROTARY-SWITCH REAL-CAD FIT PROTOTYPE -- mechanical clearance revision.
// Dimensions in mm; print-fit prototype, NOT production-certified.
// Part selector: print_layout | rear | bezel | side_caps | fit_mockup
// Authoritative solid source for prototype STL generation; no decorative fake holes.
part = "print_layout";
$fn = 48;

// PCB outline from Elecrow Eagle board.brd layer 20: 31.2 x 63.2, R1.
board_w = 31.2;
board_l = 63.2;
board_t = 1.6;
board_r = 1.0;
case_w = 46.0;
case_l = 82.0;
case_r = 4.0;
case_wall = 1.8;
rear_h = 14.4;
bezel_h = 5.6;
floor_t = 1.8;
split_z = rear_h;
front_z = rear_h + bezel_h;
// CrowPanel real STEP: assembly installed envelope z7.20 to17.85 after board lift.
board_clear = 0.4;
board_shift_y = 7.0; // entire Elecrow STEP, including rotary and switch tips // total x/y clearance, 0.2 per side

battery_xy = [0, -2.5];       // Adafruit #1578 physical envelope 29x36x4.75
mic_xy = [-3.8, 23.5];        // INMP441 breakout modeled as 16x14 (not Ø14)
motor_xy = [-7, -31.5];       // 1027 motor Ø10x2.7 and holder
motor_driver_xy = [8, -31.8];// driver PCB envelope 12.36x13
snap_x = 18.2;
snap_y = 33.5;

module roundrect2d(w, l, r) {
    offset(r = r) square([w-2*r, l-2*r], center = true);
}
module roundbox(w,l,h,r){ linear_extrude(height=h) roundrect2d(w,l,r); }
module snap_tower(x,y) {
    // Floor-anchored tower, shank and spherical catch.
    translate([x,y,floor_t-0.2]) cylinder(d=5.4,h=10.7);
    translate([x,y,12.3]) cylinder(d=3.3,h=3.1);
    translate([x,y,15.4]) sphere(d=3.7);
}
module board_supports(){
    // Four board-edge tabs mechanically joined to side walls.
    for(xsign=[-1,1], y=[-20,23]) {
      // Each rail rises from a floor-anchored, sloped printable buttress.
      hull(){
        translate([xsign*20.1,y,2.05]) cube([2.4,3.2,0.5],center=true);
        translate([xsign*18.15,y,14.1]) cube([7.5,3.2,0.6],center=true);
      }
    }
}
module acoustic_seal_seat(){
    translate([mic_xy[0],mic_xy[1],floor_t-0.2])
      difference(){
        cylinder(d=7.4,h=1.3);
        translate([0,0,-0.1]) cylinder(d=5.2,h=1.5);
      }
}
module motor_holder(){
    translate([motor_xy[0],motor_xy[1],floor_t-0.2])
      difference(){
        // Refit to the actual LCM1027A2445F STEP: >10.8mm across external features.
        // 11.6mm opening; thickened rim prevents printing a fragile thin ring.
        cylinder(d=13.8,h=2.5);
        translate([0,0,-0.1]) cylinder(d=11.6,h=2.7);
        // Wire exit for LEADER LCM1027A2445F leaded motor.
        translate([-2.0,4.5,-0.1]) cube([4,4,2.7]);
      }
}
module driver_lip(){
    // Open-top frame, no hard compression on electronics.
    translate([motor_driver_xy[0],motor_driver_xy[1],floor_t-0.2])
      difference(){
        linear_extrude(height=1.1) roundrect2d(14.0,14.5,1.1);
        translate([0,0,-0.1]) linear_extrude(height=1.3) roundrect2d(12.9,13.5,0.8);
      }
}
// Genuine CrowPanel TM_2024A toothed dial (official STEP solid, not a proxy):
// original X=-6.582..6.582 Y=23.988..32.981 Z=13.152..15.952;
// whole-board +7 mm move puts wheel face near top edge Y39.981.
module rotary_thumb_notch(){
  translate([-7.10,36.7,12.20]) cube([14.20,case_l/2-36.7+0.8,front_z-12.2+0.5]);
}
module key_stem_openings(){
  for(x=[-11.15,11.15]) translate([x-1.68,38.9,12.6]) cube([3.36,3.0,2.1]);
}
module rear_shell(){
    difference(){
        union(){
            difference(){
                roundbox(case_w,case_l,rear_h,case_r);
                // Genuine interior hollow, not viewer-colored surface patches.
                translate([0,0,floor_t])
                  roundbox(case_w-2*case_wall,case_l-2*case_wall,rear_h+1,case_r-case_wall);
            }
            for(x=[-snap_x,snap_x],y=[-snap_y,snap_y]) snap_tower(x,y);
            board_supports();
            acoustic_seal_seat();
            motor_holder();
            driver_lip();
        }
        // Cut the *actual shell* for a molded USB-C plug collar.
        translate([case_w/2-2.9,board_shift_y-0.6-7.75,9.0]) cube([4.0,15.5,5.5]);
        // Genuine BOOT and RESET access holes through rear floor.
        for(py=[-15.2+board_shift_y,-25.67+board_shift_y])
          translate([-11.9,py,-0.1]) cylinder(d=2.4,h=2.1);
        // One sealed acoustic through-bore, 2mm diameter.
        // Single centered acoustic bore preserves foam-gasket sealing circumference.
        translate([mic_xy[0],mic_xy[1],-0.1]) cylinder(d=2.0,h=3.6);
        // Bottom pry notch at parting plane.
        translate([-5,-case_l/2-0.1,rear_h-0.9]) cube([10,3,1.2]);
        key_stem_openings();
        rotary_thumb_notch();
    }
}
module snap_socket(x,y){
   // 3.55mm shank throat with 4.02mm head pocket; roof ~1.29mm.
   translate([x,y,split_z-0.15]) cylinder(d=3.55,h=1.3);
   translate([x,y,15.4]) sphere(d=4.02);
}
module front_bezel(){
    difference(){
       translate([0,0,split_z]) roundbox(case_w,case_l,bezel_h,case_r);
       translate([0,6.35,split_z-0.10])
          roundbox(32.0,65.3,4.35,1.2);
       translate([0,board_shift_y,15.95]) roundbox(29.7,59.7,1.12,0.8);
       // Wider than 23.71x48.55 active display area, centered Y+2.625.
       translate([0,board_shift_y+2.625,16.97]) roundbox(24.9,49.75,3.5,0.6);
       for(x=[-snap_x,snap_x],y=[-snap_y,snap_y]) snap_socket(x,y);
       translate([case_w/2-2.9,board_shift_y-0.6-7.75,split_z-0.1]) cube([4.0,15.5,2.3]);
       key_stem_openings();
       rotary_thumb_notch();
    }
}
module side_button_cap(x){
  // Genuine K3/K4 plunger, 0.11mm nominal gap to official button tip;
  // outermost point Y40.85 behind the Y41 case outline (no overhang).
  union(){
    translate([x,39.5,13.61]) cube([2.80,2.70,1.40],center=true);
    translate([x,38.42,13.61]) cube([4.70,0.65,2.10],center=true);
  }
}
module preview_component_envelopes(){
   color("gainsboro") translate([0,board_shift_y,split_z]) roundbox(board_w,board_l,board_t,board_r);
   color("slategray") translate([0,board_shift_y,16.0]) roundbox(29.2,59.2,0.9,0.5);
   color("orange") translate([battery_xy[0]-14.5,battery_xy[1]-18,floor_t+0.05])
     cube([29,36,4.75]);
   color("gold") translate([mic_xy[0]-8,mic_xy[1]-7,floor_t+0.25])
     cube([16,14,2.02]);
   color("grey") translate([motor_xy[0],motor_xy[1],floor_t+0.15])
     cylinder(d=10,h=2.7);
   color("magenta") translate([motor_driver_xy[0]-6.18,motor_driver_xy[1]-6.5,floor_t+0.2])
     cube([12.36,13,2.4]);
}
if(part=="side_caps"){
  // Print two captured side-button plungers only; do not replace rotary dial.
  translate([0,-36,-12.56]) {side_button_cap(-11.15); side_button_cap(11.15);}
}
else if(part=="rear") rear_shell();
else if(part=="bezel") front_bezel();
else if(part=="fit_mockup"){
    color("dimgray",0.7) rear_shell();
    color("silver",0.7) front_bezel();
    preview_component_envelopes();
}
else if(part=="buttons_clash")
    intersection(){rear_shell(); union(){side_button_cap(-11.15); side_button_cap(11.15);}}
else if(part=="rear_clash") intersection(){rear_shell(); preview_component_envelopes();}
else if(part=="bezel_clash") intersection(){front_bezel(); preview_component_envelopes();}
else {
    // Bed-separated printable bodies, bezel inverted face-down.
    rear_shell();
    translate([case_w+9,0,front_z]) rotate([0,180,0]) front_bezel();
}
