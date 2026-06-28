// Scout assistive robot enclosure — parametric OpenSCAD
// Export: openscad -o scout-body-shell.stl scout-body.scad
// Adjust variables below for your chassis

$fn = 80;

// --- parameters ---
body_diameter = 180;
shell_height = 120;
wall = 3;
base_thick = 4;
speaker_d = 50;
mic_d = 8;
pi_len = 90;
pi_wid = 60;

// --- main shell (upper) ---
module shell() {
  difference() {
    cylinder(h = shell_height, d = body_diameter);
    translate([0, 0, base_thick])
      cylinder(h = shell_height, d = body_diameter - wall * 2);
    // speaker grille (front)
    translate([body_diameter / 2 - wall - 5, 0, shell_height / 2])
      rotate([0, 90, 0])
        cylinder(h = wall + 2, d = speaker_d, center = true);
    // mic hole (top)
    translate([0, 0, shell_height - 5])
      cylinder(h = 10, d = mic_d, center = true);
    // pi bay
    translate([0, 0, base_thick + 2])
      cube([pi_len, pi_wid, 30], center = true);
  }
}

// --- base plate ---
module base_plate() {
  difference() {
    cylinder(h = base_thick, d = body_diameter);
    // motor wire notch
    translate([0, -body_diameter / 2 + 10, 0])
      cube([30, 20, base_thick + 1], center = true);
    // mounting holes (M3)
    for (a = [45, 135, 225, 315])
      rotate([0, 0, a])
        translate([body_diameter / 2 - 15, 0, 0])
          cylinder(h = base_thick + 1, d = 3.2, center = false);
  }
}

// --- front bumper clip ---
module bumper() {
  difference() {
    translate([-40, -5, 0])
      cube([80, 10, 15]);
    translate([0, 0, 3])
      cube([70, 12, 10], center = true);
  }
}

// Default export: shell only (change module call for other parts)
shell();

// Uncomment to preview other parts:
// base_plate();
// bumper();
