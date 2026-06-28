// Charging dock funnel — guides Scout backward onto contacts
// Export: openscad -o dock-funnel.stl dock-funnel.scad

$fn = 60;

funnel_width = 200;
funnel_depth = 180;
wall = 3;
contact_gap = 40;

module funnel() {
  difference() {
    translate([-funnel_width / 2, 0, 0])
      cube([funnel_width, funnel_depth, 40]);
    // V-shaped guide
    translate([0, funnel_depth - 10, 5])
      rotate([0, 0, 0])
        linear_extrude(height = 50)
          polygon(points = [
            [-funnel_width / 2 + wall, 0],
            [funnel_width / 2 - wall, 0],
            [contact_gap / 2, funnel_depth - 30],
            [-contact_gap / 2, funnel_depth - 30]
          ]);
    // contact strip slots
    for (x = [-contact_gap / 2, contact_gap / 2])
      translate([x, funnel_depth - 5, 0])
        cube([12, 8, 15], center = true);
  }
}

funnel();
