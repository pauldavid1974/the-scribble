// ============================================================================
// The Scribble v5.0 — Official STEP-CAD Enclosure (Elecrow 00-2-13_view_asm.stp)
// - Exact PCB Cavity: 31.60 x 63.60 mm R=1.2mm (for 31.20 x 63.20 mm R=1.0mm PCB)
// - Outer Case: 35.20 x 68.80 x 12.20 mm with R=2.60 mm Corners
// - Flat Top Wall spans X = -15.00 .. +15.00 mm -> 0.00 mm Button Overhang!
// - Top Edge Recessed Slots: EXIT (X=-11.15mm), XB-TM-2024A (X=0.00mm), MENU (X=+11.15mm)
// - Right Long Edge (+X): USB Type-C Cutout at Y = -0.60 mm
// - Back Face (-Z): Recessed Pinholes for Vertical BOOT (X=-11.9, Y=-15.2) & RESET (X=-11.9, Y=-25.67)
// ============================================================================
$fn = 64;

case_w = 35.20;
case_l = 68.80;
bot_h  = 9.10;
top_h  = 3.10;
wall   = 1.80;
rad    = 2.60;

module scribble_blank(w, l, h, r, ch_bot, ch_top) {
  hull() {
    if (ch_bot > 0)
      translate([0, 0, 0])
        linear_extrude(height = 0.01)
          offset(r = r - ch_bot) square([w - 2*r, l - 2*r], center = true);
    translate([0, 0, ch_bot])
      linear_extrude(height = h - ch_bot - ch_top)
        offset(r = r) square([w - 2*r, l - 2*r], center = true);
    if (ch_top > 0)
      translate([0, 0, h - 0.01])
        linear_extrude(height = 0.01)
          offset(r = r - ch_top) square([w - 2*r, l - 2*r], center = true);
  }
}

module bottom_cradle() {
  difference() {
    scribble_blank(case_w, case_l, bot_h, rad, 1.4, 0);
    translate([0, 0, 1.8])
      scribble_blank(31.60, 63.60, bot_h, 1.2, 0, 0);
    // Right-edge (+X) USB Type-C cutout at Y = -0.60mm
    translate([case_w/2 - wall - 0.5, -0.60 - 4.9, bot_h - 3.4])
      cube([wall + 1, 9.8, 3.5]);
    // Top-edge (+Y) Recessed Slots inside the flat X = [-15..+15mm] wall
    translate([-5.2, case_l/2 - wall - 0.5, bot_h - 2.3])
      cube([10.4, wall + 1, 1.9]);
    translate([-11.15 - 2.3, case_l/2 - wall - 0.5, bot_h - 2.3])
      cube([4.6, wall + 1, 1.9]);
    translate([ 11.15 - 2.3, case_l/2 - wall - 0.5, bot_h - 2.3])
      cube([4.6, wall + 1, 1.9]);
    // Back-face (-Z) Pinholes for vertical BOOT & RESET switches
    for (py = [-15.20, -25.67])
      translate([-11.90, py, -0.5])
        cylinder(d = 2.4, h = 2.5);
    // Back-face (-Z) acoustic port for the INMP441 bottom-port mic (X=-3.8, Y=+23.5)
    for (dx = [-2.3, 0, 2.3])
      translate([-3.80 + dx, 23.50, -0.5])
        cylinder(d = (dx == 0) ? 1.7 : 1.4, h = 2.5);
    // Bottom-edge pry slot at the split line
    translate([-5.0, -case_l/2 - 0.5, bot_h - 0.65])
      cube([10.0, wall + 1, 0.70]);
  }
  // 4-corner Ø3.6mm snap pins with spherical heads (from Printables 1566902)
  for (p = [[-13.8, 30.8], [13.8, 30.8], [-13.8, -30.8], [13.8, -30.8]])
    translate([p[0], p[1], 1.8]) {
      cylinder(d = 3.6, h = bot_h - 1.8 + 1.15);
      translate([0, 0, bot_h - 1.8 + 1.15]) sphere(d = 3.7);
    }
  // INMP441 acoustic seal ring (seat a foam gasket here)
  translate([-3.80, 23.50, 1.8])
    difference() { cylinder(d = 7.4, h = 2.35); cylinder(d = 5.2, h = 2.5); }
  // 10mm VC1027B200N Vibration Motor C-Clip Ring
  translate([-4.2, -24.0, 1.8])
    difference() { cylinder(d = 12.2, h = 2.5); cylinder(d = 10.1, h = 2.6); }
}

module flush_top_bezel() {
  difference() {
    scribble_blank(case_w, case_l, top_h, rad, 0, 0.7);
    translate([0, 0, -0.05])
      scribble_blank(31.60, 63.60, 1.65, 1.2, 0, 0);
    translate([-29.40/2, -59.40/2, 1.55])
      cube([29.40, 59.40, 0.98]);
    // Active display window centered at Y = +2.625mm (from 00-2-13_view_asm.stp)
    hull() {
      translate([0, 2.625, top_h - 0.60]) cube([23.71, 48.55, 0.02], center = true);
      translate([0, 2.625, top_h + 0.05]) cube([24.90, 49.75, 0.02], center = true);
    }
    // Snap sockets (0.25mm tolerance) for the 4 corner pins
    for (p = [[-13.8, 30.8], [13.8, 30.8], [-13.8, -30.8], [13.8, -30.8]])
      translate([p[0], p[1], -0.1]) cylinder(d = 3.6 + 0.25, h = 1.7);
  }
}

bottom_cradle();
translate([42, 0, top_h]) rotate([0, 180, 0]) flush_top_bezel();