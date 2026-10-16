// --- ESPECIFICAÇÕES DA PLACA (BOARD) ---
pcb_w = 66.0;        
pcb_d = 31.0;        
pcb_h = 12.5;        

// --- MOLDURA FRONTAL (BORDAS DA TELA) ---
bezel_l = 6.0;         // Borda esquerda (Left)
bezel_r = 8.0;         // Borda direita (Right)
bezel_tb = 2.5;        // Borda em cima/baixo (Top/Bottom)
bezel_thickness = 0.8; // Espessura da parede frontal

// --- POSIÇÃO DA USB-C ---
// A posição X agora é calculada a partir da borda esquerda (bezel_l)
usb_x_pos = 32.0 + bezel_tb;   
usb_from_top = 5.0;  
usb_w = 11.0;        
usb_h = 4.5;         

// --- PARÂMETROS DE AJUSTE (ENCAIXE FIRME) ---
wall = 2.0;          
gap = 0.8;           // Folga interna total (placa justa)
corner_r = 4.0;      
pin_dia = 3.6;       
pin_h = 5.5;
tolerance = 0.25;    // Tolerância para os pinos (ajuste se necessário)

$fn = 60;

// Dimensões Totais Externas
total_w = pcb_w + 2*wall + gap;
total_d = pcb_d + 2*wall + gap;
total_h = pcb_h + bezel_thickness + 1.0; 

module corners(offset_val = 2.2) {
    inset = wall + offset_val;
    translate([inset, inset, 0]) children();
    translate([total_w - inset, inset, 0]) children();
    translate([total_w - inset, total_d - inset, 0]) children();
    translate([inset, total_d - inset, 0]) children();
}

// --- CORPO PRINCIPAL ---
module main_body() {
    difference() {
        // Bloco Externo
        hull() {
            translate([corner_r, corner_r, 0]) cylinder(total_h, r=corner_r);
            translate([total_w-corner_r, corner_r, 0]) cylinder(total_h, r=corner_r);
            translate([total_w-corner_r, total_d-corner_r, 0]) cylinder(total_h, r=corner_r);
            translate([corner_r, total_d-corner_r, 0]) cylinder(total_h, r=corner_r);
        }

        // Cavidade da Placa
        translate([wall, wall, -1])
            cube([pcb_w + gap, pcb_d + gap, total_h - bezel_thickness + 1]);

        // Janela da Tela (Ajustada para L e R)
        // Largura da janela = PCB_W - (borda esquerda + borda direita)
        translate([wall + bezel_l, wall + bezel_tb, total_h - bezel_thickness - 1])
            cube([pcb_w - (bezel_l + bezel_r), pcb_d - 2*bezel_tb, bezel_thickness + 2]);

        // Recorte USB-C
        translate([wall + usb_x_pos - usb_w/2, total_d - wall - 1, total_h - bezel_thickness - usb_from_top - usb_h/2])
            cube([usb_w, wall + 2, usb_h]);
            
        // Furos para pinos
        translate([0, 0, -0.1])
            corners(1.8) cylinder(pin_h + 0.5, d=pin_dia + tolerance);
            
        // Rebaixo de alinhamento (para a tampa não sambar)
        translate([wall/2, wall/2, -0.1])
            cube([total_w - wall, total_d - wall, 1.2]);
    }
}

// --- TAMPA TRASEIRA ---
module back_cover() {
    union() {
        // Base
        hull() {
            translate([corner_r, corner_r, 0]) cylinder(wall, r=corner_r);
            translate([total_w-corner_r, corner_r, 0]) cylinder(wall, r=corner_r);
            translate([total_w-corner_r, total_d-corner_r, 0]) cylinder(wall, r=corner_r);
            translate([corner_r, total_d-corner_r, 0]) cylinder(wall, r=corner_r);
        }
        
        // Degrau de travamento (Macho)
        translate([wall/2 + tolerance, wall/2 + tolerance, wall])
            cube([total_w - wall - 2*tolerance, total_d - wall - 2*tolerance, 1.0]);

        // Pinos com trava esférica
        translate([0, 0, wall])
            corners(1.8) {
                cylinder(pin_h, d=pin_dia);
                translate([0,0, pin_h]) sphere(d=pin_dia + 0.1); 
            }
    }
}

// --- RENDER ---
color("RoyalBlue") main_body();

translate([0, -total_d - 10, 0]) 
    color("DimGray") back_cover();